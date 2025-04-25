from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.crud_route import router
from app.database import init_db, engine
from fastapi.staticfiles import StaticFiles


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Инициализация
    await init_db()
    yield
    # Очистка
    await engine.dispose()


app = FastAPI(title="Legendary todo list", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def read_index():
    from fastapi.responses import FileResponse

    return FileResponse("static/index.html")
