from fastapi import FastAPI
from mangum import Mangum
from .routers import org as org_router, admin as admin_router

app = FastAPI(title="Org Management Service")

app.include_router(org_router.router)
app.include_router(admin_router.router)

@app.get("/")
async def root():
    return {"msg": "Org Management Backend running on Vercel"}

# ADD THIS
handler = Mangum(app)
