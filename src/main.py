import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import uvicorn

from src.database import get_async_session, get_db
from src.ethtracker.eth_tracker import Prediction
from config.config import VERBOSE_MODE, REBUILD_MODELS_TIME, WORK_WITH_DATA_BASE
from src.ethtracker.dbmanager import DBManager

db1 = DBManager()
prediction = Prediction(db1)
prediction.is_work_db = WORK_WITH_DATA_BASE


async def main_processor():
    """main application thread  """
    print("Wait for API connection...")
    prediction.get_data()
    while True:
        await prediction.current_handler()
        await asyncio.sleep(1)


async def check_processor():
    """ preparation for feature to recalculating models in background (async mode)"""
    if REBUILD_MODELS_TIME:
        while True:
            await asyncio.sleep(REBUILD_MODELS_TIME)
            if VERBOSE_MODE:
                print(f"{REBUILD_MODELS_TIME} seconds left. We have to Rebuild our models")
            prediction.rebuild_models()
            prediction.checker_temporary_history()
    else:
        if VERBOSE_MODE:
            print("Check processor don't activate")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    asyncio.create_task(main_processor())
    asyncio.create_task(check_processor())
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


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
