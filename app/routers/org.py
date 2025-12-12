# app/routers/org.py
from fastapi import APIRouter, HTTPException, Depends
from ..models import OrgCreate, OrgOut
from ..crud import create_organization, get_org_by_name, ORGS, ADMINS
from ..dependencies import get_current_admin
from ..db import client

router = APIRouter(prefix="/org", tags=["org"])

@router.post("/create", response_model=OrgOut)
async def create_org(payload: OrgCreate):
    try:
        res = await create_organization(payload.organization_name, payload.admin_email, payload.admin_password)
        return {"org_name": res["org_name"], "collection_name": res["collection_name"]}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/get/{org_name}")
async def get_org(org_name: str):
    org = await get_org_by_name(org_name)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    org["admin_id"] = str(org["admin_id"])
    org["_id"] = str(org["_id"])
    return org

@router.put("/update")
async def update_org_name(new_org_name: str, admin=Depends(get_current_admin)):

    old_org_name = admin["org"]

    if new_org_name.strip().lower() == old_org_name.lower():
        raise HTTPException(status_code=400, detail="New name is same as old name")

    existing = await ORGS.find_one({"org_name": new_org_name})
    if existing:
        raise HTTPException(status_code=400, detail="Organization name already exists")

    old_db_name = f"org_{old_org_name.lower().replace(' ', '_')}"
    new_db_name = f"org_{new_org_name.lower().replace(' ', '_')}"

    old_db = client[old_db_name]
    new_db = client[new_db_name]

    collections = await old_db.list_collection_names()
    for coll in collections:
        old_coll = old_db[coll]
        new_coll = new_db[coll]

        async for doc in old_coll.find({}):
            await new_coll.insert_one(doc)

        await old_db.drop_collection(coll)

    await client.drop_database(old_db_name)

    await ORGS.update_one(
        {"org_name": old_org_name},
        {"$set": {"org_name": new_org_name, "collection_name": new_db_name}}
    )

    await ADMINS.update_one(
        {"_id": admin["admin_id"]},
        {"$set": {"org": new_org_name}}
    )

    return {"message": "Organization renamed successfully"}

@router.delete("/delete")
async def delete_org(admin=Depends(get_current_admin)):
    org_name = admin["org"]

    db_name = f"org_{org_name.lower().replace(' ', '_')}"

    await client.drop_database(db_name)
    await ORGS.delete_one({"org_name": org_name})
    await ADMINS.delete_one({"_id": admin["admin_id"]})

    return {"message": "Organization deleted successfully"}
