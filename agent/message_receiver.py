import json
from typing import Optional

from spade.behaviour import CyclicBehaviour


class MessageReceiverBehaviour(CyclicBehaviour):
    async def run(self) -> None:
        msg = await self.receive(timeout=9999)
        if msg is not None and msg.body is not None:
            try:
                data = json.loads(msg.body)
                await self.process_message(data)
            except json.JSONDecodeError:
                return

    async def process_message(self, msg: dict):
        msg_type: Optional[str] = msg.get("type")
        if msg_type is None:
            return

        match msg_type:
            case "bot-img":
                pass
