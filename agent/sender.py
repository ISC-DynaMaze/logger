import json

from spade.behaviour import Message, OneShotBehaviour

class SenderBehaviour(OneShotBehaviour):
    def __init__(self, message: dict, recipient_jid: str):
        super().__init__()
        self.message: dict = message
        self.recipient_jid = recipient_jid
    
    async def run(self) -> None:
        msg: Message = Message(
            to=self.recipient_jid,
            body=json.dumps(self.message),
            metadata={"performative": "inform"}
        )
        await self.send(msg)
