# Copyright (C) 2020-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import cast
from typing import Any

import aorta

import cbra.core as cbra
from cbra.core import MessageRunner
from cbra.types import CommandFailed
from .eventarcendpoint import EventarcEndpoint
from .messagediscarded import MessageDiscarded
from .pubsubmessage import PubsubMessage


class AortaEndpoint(EventarcEndpoint):
    __module__: str = 'cbra.ext.google'
    runner: MessageRunner = MessageRunner.depends()

    async def put(self, dto: dict[str, Any]):
        envelope = aorta.parse(dto)
        if envelope is None:
            self.logger.warning("Could not parse the request body as a known Aorta message type.")
            return
        self.logger.debug("Received message %s", envelope.kind)

    async def run_command(self, envelope: aorta.types.Envelope[Any]):
        success, *_ = await self.runner.run(envelope)
        if not success:
            self.logger.critical(
                "Refusing to acknowledge message (id: %s, kind: %s)",
                envelope.metadata.uid, envelope.kind
            )
            raise CommandFailed

    async def on_message(self, message: PubsubMessage) -> None:
        try:
            data = message.get_data()
        except ValueError:
            self.logger.critical("Data could not be interpreted as JSON.")
            raise MessageDiscarded
        if data is None:
            raise MessageDiscarded
        envelope = aorta.parse(data)
        if envelope is None:
            self.logger.critical("Message is not an Aorta message type.")
            raise MessageDiscarded
        envelope = cast(aorta.types.Envelope[Any], envelope)
        if envelope.is_command():
            await self.run_command(envelope)
        elif envelope.is_event():
            _, retry = await self.runner.run(envelope)
            for m in retry:
                self.logger.critical(
                    "Handler failure (handler: %s, message: %s)",
                    m.metadata.handler, m.metadata.uid
                )
        else:
            self.logger.warning(
                "Received Aorta message of unknown type (id: %s, type: %s)",
                envelope.metadata.uid, envelope.type
            )