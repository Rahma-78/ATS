import logging
import os

from fastapi import (
    FastAPI,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
    status,
    Request,
)
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.dependencies import get_analyzer
from app.api.schemas import AnalysisResult
from app.services.analysis_service import ATSAnalyzer
from app.utils.file_utils import extract_text
from app.core.config import settings

# --- Configuration ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# --- FastAPI App Initialization ---
root_path = os.environ.get("ROOT_PATH", "")
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.API_VERSION,
    root_path=root_path,
)

# --- Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Static Files & Templates ---
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/static")


# --- Root Endpoint ---
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# --- Analyze Endpoint ---
@app.post("/api/v1/analyze", response_model=AnalysisResult)
async def analyze_resume(
    job_description: str = Form(...),
    resume: UploadFile = File(...),
    analyzer: ATSAnalyzer = Depends(get_analyzer),
):
    """
    Analyzes a resume against a job description.
    """
    logging.info("analyze_resume endpoint hit")
    if not resume.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No resume file provided."
        )

    try:
        logging.info("Starting resume analysis")
        resume_content = await resume.read()
        resume_text = extract_text(resume_content, resume.filename)
        if not resume_text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not extract text from the resume. Please ensure it is not empty or image-based.",
            )

        analysis_result = await run_in_threadpool(
            analyzer.get_structured_analysis, resume_text, job_description
        )
        if not analysis_result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred during the analysis.",
            )

        return analysis_result

    except Exception as e:
        logging.exception("An unexpected error occurred:")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        )