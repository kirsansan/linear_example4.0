from contextlib import asynccontextmanager

from fastapi import FastAPI


def fake_answer_to_everything_ml_model(x: float):
    return x * 42




def main_processor(session: AsyncSession = Depends(get_async_session)):
    # prediction = Prediction()
    prediction.get_data()
    while True:
        prediction.current_handler()
        # await queue.put(prediction.status)
        await asyncio.sleep(1)



async def check_processor():
    """ preparation for feature to recalculating models in background """
    prediction2 = Prediction()
    if REBUILD_MODELS_TIME:
        while True:
            # data = await queue.get()
            await asyncio.sleep(REBUILD_MODELS_TIME)
            if VERBOSE_MODE:
                print(f"{REBUILD_MODELS_TIME} seconds left. We have to Rebuild our models")
            await prediction2.rebuild_models()
    else:
        if VERBOSE_MODE:
            print("Check processor don't activate")


ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    ml_models["answer_to_everything"] = fake_answer_to_everything_ml_model
    ml_models["main"] = main_processor
    ml_models["check"] = check_processor
    yield
    # Clean up the ML models and release the resources
    ml_models.clear()


app = FastAPI(lifespan=lifespan)


@app.get("/predict")
async def predict(x: float):
    result = ml_models["answer_to_everything"](x)
    r2 = ml_models["check"]()
    return {"result": result}