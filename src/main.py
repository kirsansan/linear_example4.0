import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.ethtracker.eth_tracker import main_process, Prediction

from config.config import VERBOSE_MODE

queue = asyncio.Queue()
prediction = Prediction()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Before yield

    asyncio.create_task(main_processor(queue))
    asyncio.create_task(check_processor())
    yield
    # Put under this line something what we need to do on shutdown


app = FastAPI(lifespan=lifespan,
              title="ETHEREUM tracker"
              )


@app.get("/")
async def root():
    return {"message": "ETHEREUM tracker"}


@app.get("/status")
async def status(session: AsyncSession = Depends(get_async_session)):
    # data = await queue.get()
    data = prediction.status

    return {"message": "I'm still working.", "data": data}


async def consumer():
    while True:
        data = queue.get()
        print(f"Consumer received: {data}")
        yield data
        await asyncio.sleep(1)


async def main_processor(session: AsyncSession = Depends(get_async_session)):
    # prediction = Prediction()
    while True:
        prediction.current_handler()
        # await queue.put(prediction.status)
        await asyncio.sleep(1)


async def check_processor():
    """ preparation for feature to recalculating models in background """
    while True:
        # data = await queue.get()
        await asyncio.sleep(59)
        if VERBOSE_MODE:
            print("1 minute left.")
        prediction.rebuild_models()
        await asyncio.sleep(1)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
