import asyncio
import logging

import spade

from agent.logger import LoggerAgent

logging.basicConfig(level=logging.DEBUG)

# Enable SPADE and XMPP specific logging
for log_name in ["spade", "aioxmpp", "xmpp"]:
    log = logging.getLogger(log_name)
    log.setLevel(logging.DEBUG)
    log.propagate = True


async def main():
    print("Hello from main")
    agent = LoggerAgent("logger@localhost", "plsnohack")
    await agent.start()
    print("Agent started")

    try:
        while agent.is_alive():
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        await agent.stop()


if __name__ == "__main__":
    spade.run(main())
