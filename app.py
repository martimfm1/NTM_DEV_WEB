import os
import asyncio
from dotenv import load_dotenv
from quart import Quart
from backend.routes import routes
from backend.bots.ntm_dev import bot as ntmdev
from backend.bots.ntm_ticket import bot as ntmticket

load_dotenv()
ntmdev_token = os.getenv("ntmdev")
ntmticket_token = os.getenv("ntmticket")

app = Quart(__name__, static_folder='site/static', template_folder='site/templates')
app.secret_key = 'bananaazul'
app.register_blueprint(routes)

async def main():
    await asyncio.gather(
        app.run_task(host="0.0.0.0", port=5000),
        ntmdev.start(ntmdev_token),
        ntmticket.start(ntmticket_token),
    )

if __name__ == "__main__":
    asyncio.run(main())
