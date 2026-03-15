import sys
import os

from dotenv import load_dotenv
load_dotenv()

sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import jobs, resumes, applications, agent, jobfetch

app = FastAPI(title="InternFlow AI", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jobs.router,         prefix="/jobs",         tags=["jobs"])
app.include_router(resumes.router,      prefix="/resumes",      tags=["resumes"])
app.include_router(applications.router, prefix="/applications", tags=["applications"])
app.include_router(agent.router,        prefix="/agent",        tags=["agent"])
app.include_router(jobfetch.router,     prefix="/jobfetch",     tags=["jobfetch"])

@app.get("/")
def root():
    return {"status": "InternFlow AI Backend Running ✅"}
