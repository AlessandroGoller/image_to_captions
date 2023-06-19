
import uvicorn

from app.app_creator import router, create_app

app = create_app()
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
