from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
import json
import os

router = APIRouter()

STORAGE_FILE = "data/applications.json"


def load_applications():
    if not os.path.exists(STORAGE_FILE):
        return []
    with open(STORAGE_FILE, "r") as f:
        return json.load(f)


def save_applications(data):
    os.makedirs("data", exist_ok=True)
    with open(STORAGE_FILE, "w") as f:
        json.dump(data, f, indent=2)


class Application(BaseModel):
    job_id: str
    company: str
    job_title: str
    location: str
    resume_used: Optional[str] = "Base Resume"
    status: Optional[str] = "Applied"   # Applied | Interview | Offer | Rejected
    notes: Optional[str] = ""
    url: Optional[str] = ""


@router.get("/")
def get_applications():
    return load_applications()


@router.post("/")
def add_application(app: Application):
    data = load_applications()
    app_dict = app.dict()
    app_dict["id"] = f"app-{len(data) + 1}"
    from datetime import datetime
    app_dict["applied_date"] = datetime.now().strftime("%Y-%m-%d")
    data.append(app_dict)
    save_applications(data)
    return {"message": "Application tracked!", "application": app_dict}


@router.put("/{app_id}/status")
def update_status(app_id: str, status: str):
    data = load_applications()
    for app in data:
        if app["id"] == app_id:
            app["status"] = status
            break
    save_applications(data)
    return {"message": "Status updated!"}


@router.delete("/{app_id}")
def delete_application(app_id: str):
    data = load_applications()
    data = [a for a in data if a["id"] != app_id]
    save_applications(data)
    return {"message": "Deleted!"}
