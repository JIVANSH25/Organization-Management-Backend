# app/crud.py
from .db import master_db, client
from .auth import hash_password
from datetime import datetime
from bson import ObjectId

ORGS = master_db.organizations
ADMINS = master_db.admins

def _normalize_coll_name(org_name: str) -> str:
    # safe collection name
    safe = org_name.lower().strip().replace(" ", "_")
    return f"org_{safe}"

async def create_organization(org_name: str, admin_email: str, admin_password: str):
    # check duplicate org name
    existing = await ORGS.find_one({"org_name": {"$regex": f"^{org_name}$", "$options": "i"}})
    if existing:
        raise ValueError("Organization already exists")

    coll_name = _normalize_coll_name(org_name)

    # Option A: one DB per org could be client[db_name], but we'll create collections within a dedicated DB for simplicity
    # create a collection for the org (no-op if exists)
    org_db = client[coll_name]   # this creates a namespace when we insert later

    # create admin
    hashed = hash_password(admin_password)
    admin_doc = {
        "email": admin_email,
        "password": hashed,
        "org": org_name,
        "created_at": datetime.utcnow()
    }
    admin_result = await ADMINS.insert_one(admin_doc)

    # store org metadata
    org_doc = {
        "org_name": org_name,
        "collection_name": coll_name,
        "admin_id": admin_result.inserted_id,
        "created_at": datetime.utcnow()
    }
    await ORGS.insert_one(org_doc)

    return {
        "org_name": org_name,
        "collection_name": coll_name,
        "admin_id": str(admin_result.inserted_id)
    }

async def get_org_by_name(org_name: str):
    return await ORGS.find_one({"org_name": {"$regex": f"^{org_name}$", "$options": "i"}})

async def get_admin_by_email(email: str):
    return await ADMINS.find_one({"email": email})
