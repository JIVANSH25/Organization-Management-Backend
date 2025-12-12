# app/routers/admin.py
from fastapi import APIRouter, HTTPException
from app.models import AdminLogin
from app.crud import get_admin_by_email
from app.auth import verify_password


router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/login", response_model=TokenOut)
async def admin_login(payload: AdminLogin):
    admin = await get_admin_by_email(payload.email)
    if not admin:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not verify_password(payload.password, admin["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    org = await get_org_by_name(admin["org"])
    token_payload = {"admin_id": str(admin["_id"]), "org": org["org_name"]}
    token = create_access_token(token_payload)
    return {"access_token": token}
