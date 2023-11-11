import asyncio
import copy
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import uvicorn


from src.database import get_async_session, get_db, engine_s

from src.ethtracker.eth_tracker import Prediction
from config.config import VERBOSE_MODE, REBUILD_MODELS_TIME, \
    FIRST_CRYPTO_SYMBOL, SECOND_CRYPTO_SYMBOL, POSSIBLE_TIMINGS, WORK_WITH_DATA_BASE
from src.ethtracker.myexeption import ConnectionLostError
from src.models.models import CryptoSamples
from src.ethtracker.dbmanager import DBManager
from src.ethtracker.exch_rates import BybitExchangeRates

# session1: AsyncSession = Depends(get_async_session)
# print("sess1", session1)
# session2 = Depends(get_db)
# print("sess2", session2)
db1 = DBManager()
# queue = asyncio.Queue()
prediction = Prediction(db1)
prediction.is_work_db = WORK_WITH_DATA_BASE


async def main_processor():
    """main application thread  """
    # prediction = Prediction()
    print("Wait for API connection...")
    prediction.get_data()
    while True:
        await prediction.current_handler()
        # await queue.put(prediction.status)
        await asyncio.sleep(1)


async def check_processor():
    """ preparation for feature to recalculating models in background (async mode)"""
    # db = DBManager(session)
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

# async def s_processor():
#     from sqlalchemy.orm import sessionmaker
#     engine = engine_s
#     SL = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#     db = SL()
#     print("s_process sess", SL)
#     print("db", db)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Before yield
    asyncio.create_task(main_processor())
    # asyncio.create_task(check_processor())
    # asyncio.create_task(s_processor())
    yield
    # Put under this line something what we need to do on shutdown
    # await session.close_all()
    print("See you!")


app = FastAPI(lifespan=lifespan,
              title="ETHEREUM tracker"
              )


@app.get("/")
async def root(session=Depends(get_db)):
    print(session)
    return {"message": "ETHEREUM tracker"}


@app.get("/status")
async def status(session: AsyncSession = Depends(get_async_session)):
    """Return current status of parameters"""
    # data = await queue.get()
    data = prediction.status
    return {"message": "I'm still working.", "data": data}


@app.get("/rebuild")
async def rebuilding():
    """Rebuild all models"""
    old_data = prediction.status
    prediction.rebuild_models()
    data = prediction.status
    return {"message": "We rebuild all models", "old data": old_data, "new data": data}


@app.get("/check")
async def check_temp():
    """Check temporary data for comparison with default models"""
    old_data = prediction.status
    prediction.checker_temporary_history()
    data = prediction.status
    return {"message": "We carry out calculations on temporary data", "old data": old_data, "new data": data}


# @app.get("/del")
# async def deleting(session: AsyncSession = Depends(get_async_session)):
#     db = DBManager(session)
#     await db.clearing(5, 200)
#
#
# @app.get("/look")
# async def looking(session: AsyncSession = Depends(get_async_session)):
#     # db = DBManager(session)
#     # await db.get_values(5, 500)
#     print(session)


# @app.get("/add")
# async def adding(session: AsyncSession = Depends(get_async_session)):
#     db = DBManager(session)
#     api_requestor1 = BybitExchangeRates(FIRST_CRYPTO_SYMBOL)
#     api_requestor2 = BybitExchangeRates(SECOND_CRYPTO_SYMBOL)
#     test_timing = copy.deepcopy(POSSIBLE_TIMINGS)
#
#     for enum, params in enumerate(test_timing):
#         print(params)
#         try:
#             data1 = api_requestor1.get_historical_rates(params['interval'], params['num_of_samples'], True)
#             data2 = api_requestor2.get_historical_rates(params['interval'], params['num_of_samples'], True)
#             try:
#                 await db.put_values(params['interval'], params['num_of_samples'], data1, data2)
#             except Exception as e:
#                 print(f"Database error {e}")
#                 return {"status": 500, "message": "Internal server error (DATABASE error)"}
#         except ConnectionLostError:
#             if VERBOSE_MODE:
#                 print("Can't detect best timing - no data available")
#                 return {"status": 500, "message": "Internal server error (API error)"}
#     return {"status": 200, "message": "Base have renovated"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
