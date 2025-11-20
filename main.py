from fastapi import FastAPI
from connections import users_example
app = FastAPI()
app.include_router(users_example.router)
Response = dict[str, str]
@app.get("/")
def read_root() -> Response:
    return {"message": "Hello World"}

@app.get("/new-endpoint")
def new_endpoint() -> Response:
    return {"message": "NEW ENDPOINT"}



if __name__ == "__main__":
    print("STARTING TRUCO")
    