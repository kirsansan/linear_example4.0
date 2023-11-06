import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.ethtracker.eth_tracker import main_process, Prediction


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Before yield
    asyncio.create_task(process1())
    yield
    # Put under this line something what we need to do on shutdown


app = FastAPI(lifespan=lifespan,
              title="ETHEREUM tracker"
              )


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/status")
async def status():
    return {"message": "I am working. Don't worry about me"}


async def process1(session: AsyncSession = Depends(get_async_session)):
    prediction = Prediction()
    while True:
        prediction.current_handler()
        # print("la la fa")
        await asyncio.sleep(2)


async def process2():
    while True:
        print("Process 2 is running asynchronously.")
        await asyncio.sleep(3)




if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
