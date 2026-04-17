from pathlib import Path

from aiohttp import web
from spade.agent import Agent

from agent.message_receiver import MessageReceiverBehaviour
from agent.sender import SenderBehaviour


class LoggerAgent(Agent):
    PUBLIC_DIR = Path(__file__).parent.parent / "public"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ws_clients: set[web.WebSocketResponse] = set()

    async def setup(self):
        self.web.app.middlewares.append(self.index_middleware)
        self.web.app.router.add_static("/", self.PUBLIC_DIR, name="public")
        self.web.app.router.add_get("/api/status", self.handle_api_status)
        self.web.app.router.add_get("/ws", self.handle_websocket)

        self.web.start(hostname="127.0.0.1", port=10000)

        receiver = MessageReceiverBehaviour()
        self.add_behaviour(receiver)

    @web.middleware
    async def index_middleware(self, request, handler):
        rel_path = Path(request.path).relative_to("/")
        full_path = self.PUBLIC_DIR / rel_path
        if not full_path.exists():
            return web.HTTPNotFound()
        if full_path.is_dir():
            full_path /= "index.html"
            if not full_path.exists():
                return web.HTTPNotFound()
        return web.FileResponse(full_path)

    async def handle_api_status(self, request):
        data = {
            "status": "running",
            "jid": str(self.jid),
            "behaviours": len(self.behaviours),
        }
        return web.json_response(data)

    async def handle_websocket(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        self.ws_clients.add(ws)

        try:
            async for msg in ws:
                if msg.type == web.WSMsgType.TEXT:
                    await self.handle_ws_msg(msg.json())
                    await ws.send_str(f"Server received: {msg.data}")
                elif msg.type == web.WSMsgType.ERROR:
                    print(f"WS connection closed with exception {ws.exception()}")
        finally:
            self.ws_clients.remove(ws)

        return ws

    async def handle_ws_msg(self, msg: dict):
        match msg["type"]:
            case "send":
                self.add_behaviour(SenderBehaviour(msg["msg"], msg["to"]))
