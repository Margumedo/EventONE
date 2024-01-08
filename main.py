from fastapi import FastAPI
from starlette.responses import RedirectResponse
from app.routes.user import router as user
from app.routes.event import router as event
from app.routes.reservations import router as reservation
from app.routes.comment import router as comment


app = FastAPI(
    title="My EventOne with FastAPI",
    version="1.0.1",
    description="Esta es mi segunda api pero usando cosas nuevas",
    # openapi_tags=["name"]    
            )

routes = [user, event, reservation, comment]

for route in routes:
    app.include_router(route)


@app.get("/")
async def docs():
    return RedirectResponse(url="docs")

@app.get("/home")
async def home():
    return {"Message":"Welcome to your fucking working FastAPI"}