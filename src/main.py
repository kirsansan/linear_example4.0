import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.ethtracker.eth_tracker import main_process, Prediction

from config.config import VERBOSE_MODE, REBUILD_MODELS_TIME
from src.models.models import CryptoSamples

queue = asyncio.Queue()
prediction = Prediction()
# ml_models = {}

async def main_processor(session: AsyncSession = Depends(get_async_session)):
    # prediction = Prediction()
    prediction.get_data()
    while True:
        prediction.current_handler()
        # await queue.put(prediction.status)
        await asyncio.sleep(1)


async def check_processor():
    """ preparation for feature to recalculating models in background """
    # prediction2 = Prediction()
    if REBUILD_MODELS_TIME:
        while True:
            # data = await queue.get()
            await asyncio.sleep(REBUILD_MODELS_TIME)
            if VERBOSE_MODE:
                print(f"{REBUILD_MODELS_TIME} seconds left. We have to Rebuild our models")
            await prediction.rebuild_models()
    else:
        if VERBOSE_MODE:
            print("Check processor don't activate")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Before yield
    asyncio.create_task(main_processor())
    asyncio.create_task(check_processor())
    #ml_models["main"] = main_processor
    #ml_models["check"] = check_processor
    yield
    # Put under this line something what we need to do on shutdown
    print("See you!")


app = FastAPI(lifespan=lifespan,
              title="ETHEREUM tracker"
              )


# app = FastAPI(title="ETHEREUM tracker")
#
#
# @app.on_event("startup")
# async def startup_event():
#     # Start process 1
#     # asyncio.create_task(ml_models["main"]())
#     res1 = ml_models["main"]()
#
#     # Start process 2
#     asyncio.create_task(ml_models["check"]())
#     res1 = ml_models["check"]()

# @app.get("/start")
# async def remote_startup_event():
#     # Start process 1
#     asyncio.create_task(ml_models["main"]())
#     # res1 = ml_models["main"]()
#
#     # Start process 2
#     asyncio.create_task(ml_models["check"]())
#     #res2 = ml_models["check"]()

@app.get("/")
async def root():
     return {"message": "ETHEREUM tracker"}


@app.get("/status")
async def status(session: AsyncSession = Depends(get_async_session)):
    # data = await queue.get()
    data = prediction.status
    return {"message": "I'm still working.", "data": data}


@app.get("/add")
async def status(session: AsyncSession = Depends(get_async_session)):
    try:
        aaa = prediction.requester_btc.get_historical_rates(15, 200)
        constant_values = {"symbol": "BTC", "interval": 15, "samples": 200, "time_": 1636171200}
        samples_to_add = [CryptoSamples(value=value, **constant_values) for value in aaa]
        session.add_all(samples_to_add)
        await session.commit()
    except:
        print("Something Error")
    return {"status": 200}


# async def consumer():
#     while True:
#         data = queue.get()
#         print(f"Consumer received: {data}")
#         yield data
#         await asyncio.sleep(1)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
