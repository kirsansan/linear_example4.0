import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn


from src.ethtracker.eth_tracker import Prediction
from config.config import VERBOSE_MODE, REBUILD_MODELS_TIME


queue = asyncio.Queue()
prediction = Prediction()


async def main_processor():
    """main application thread  """
    # prediction = Prediction()
    prediction.get_data()
    while True:
        prediction.current_handler()
        # await queue.put(prediction.status)
        await asyncio.sleep(1)


async def check_processor():
    """ preparation for feature to recalculating models in background (async mode)"""
    # prediction2 = Prediction()
    if REBUILD_MODELS_TIME:
        while True:
            # data = await queue.get()
            await asyncio.sleep(REBUILD_MODELS_TIME)
            if VERBOSE_MODE:
                print(f"{REBUILD_MODELS_TIME} seconds left. We have to Rebuild our models")
            prediction.rebuild_models()
    else:
        if VERBOSE_MODE:
            print("Check processor don't activate")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Before yield
    asyncio.create_task(main_processor())
    asyncio.create_task(check_processor())
    yield
    # Put under this line something what we need to do on shutdown
    print("See you!")


app = FastAPI(lifespan=lifespan,
              title="ETHEREUM tracker"
              )


@app.get("/")
async def root():
    return {"message": "ETHEREUM tracker"}


@app.get("/status")
async def status():
    """return status of work"""
    # data = await queue.get()
    data = prediction.status
    return {"message": "I'm still working.", "data": data}



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
