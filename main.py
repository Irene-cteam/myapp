from fastapi import FastAPI

app = FastAPI()


@app.get("/")  # 指定 api 路徑 (get方法)
def read_root():
    return {"Hello": "World"}


@app.get("/cal")  # 指定 api 路徑 (get方法)
def res():
    return {"res": 12345}


@app.get("/test")  # 指定 api 路徑 (get方法)
def res():
    return {"test": "test"}
