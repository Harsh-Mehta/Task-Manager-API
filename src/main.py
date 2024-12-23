from fastapi import FastAPI
from src.tasks.router import router as tasks_router

app = FastAPI()
app.include_router(tasks_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
