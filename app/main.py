from fastapi import FastAPI
from mangum import Mangum

from app.routers.org import router as org_router
from app.routers.admin import router as admin_router

app = FastAPI(title="Org Management Service")

app.include_router(org_router)
app.include_router(admin_router)

@app.get("/")
async def root():
    return {"msg": "Org Management Backend running on Vercel"}

handler = Mangum(app)
