# import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from chainlit_graphql.db.base import create_all
from chainlit_graphql.db.database import db

from chainlit_graphql.api.v1.api import api_router
from chainlit_graphql.db.initial_data import create_initial_data


def init_app():
    app = FastAPI(title="graphql chainlit", description="Fast API", version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    async def startup():
        await create_all()
        await create_initial_data()

    @app.on_event("shutdown")
    async def shutdown():
        await db.close()

    @app.get("/health")
    def health():
        return {"message": "ok!"}

    app.include_router(api_router, prefix="/api")

    return app


app = init_app()

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="localhost", port=8888, reload=True)
