import asyncio
from fastapi import FastAPI
from src.ethtracker.eth_tracker import main_process, Prediction

app = FastAPI(
    title="ETHEREUM tracker"
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


async def process1():
    prediction = Prediction()
    while True:
        prediction.current_handler()
        print("la la fa")
        await asyncio.sleep(2)

async def process2():
    while True:
        print("Process 2 is running asynchronously.")
        await asyncio.sleep(3)


@app.on_event("startup")
async def startup_event():
    # Запускаем процесс 1
    asyncio.create_task(process1())

    # Запускаем процесс 2
    asyncio.create_task(process2())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
