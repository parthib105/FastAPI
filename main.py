from fastapi import FastAPI
from ch01_HTTP_methods.my_http_methods import router as ch01_router
from ch02_Path_and_Query.path_and_query import router as ch02_router
from ch04_Post_request.post_request import router as ch04_router

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Patient Management System API"}

app.include_router(ch01_router)
app.include_router(ch02_router)
app.include_router(ch04_router)