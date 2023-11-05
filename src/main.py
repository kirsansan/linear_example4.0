from fastapi import FastAPI

app = FastAPI(
    title="ETHEREUM observer"
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{get}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
