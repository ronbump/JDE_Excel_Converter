from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
async def hello():
    return {"message": "Hello World!"}

if __name__ == "__main__":
    import uvicorn
    # host 0.0.0.0 is critical so Python listens to the whole network
    uvicorn.run(app, host="0.0.0.0", port=9225)