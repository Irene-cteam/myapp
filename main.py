from fastapi import FastAPI

app = FastAPI()


@app.get("/")  # 指定 api 路徑 (get方法)
def read_root():
    return {"Hello": "World"}
