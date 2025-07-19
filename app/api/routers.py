import logging

# -*- coding: utf-8 -*-
"""
API endpoints for the analysis service.
"""

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.concurrency import run_in_threadpool

from app.dependencies import get_analyzer
from app.api.schemas import AnalysisResult
from app.services.analysis_service import ATSAnalyzer
from app.utils.file_utils import extract_text

# Initialize logger
logger = logging.getLogger(__name__)

router = APIRouter(redirect_slashes=False)

@router.post("/api/v1/analyze/", response_model=AnalysisResult)
async def analyze_resume(
    job_description: str = Form(...),
    resume: UploadFile = File(...),
    analyzer: ATSAnalyzer = Depends(get_analyzer),
):
    """
    Analyzes a resume against a job description.

    Args:
        job_description (str): The job description text.
        resume (UploadFile): The resume file.
        analyzer (ATSAnalyzer): The ATS analyzer dependency.

    Returns:
        AnalysisResult: The analysis result.
    """
    logger.info("Received request to analyze resume for job description.")

    if not resume.filename:
        logger.warning("No resume file provided.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No resume file provided.",
        )

    try:
        logger.info(f"Reading and extracting text from resume: {resume.filename}")
        resume_content = await resume.read()
        
        if not resume_content:
            logger.warning(f"Resume file is empty: {resume.filename}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The resume file is empty. Please upload a valid file.",
            )
            
        resume_text = extract_text(resume_content, resume.filename)
        
        if not resume_text:
            logger.warning(f"Could not extract text from resume: {resume.filename}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not extract text from the resume. Please ensure it is not empty or image-based.",
            )

        logger.info("Running analysis in thread pool.")
        analysis_result = await run_in_threadpool(
            analyzer.get_structured_analysis, resume_text, job_description
        )

        if not analysis_result:
            logger.error("Analysis returned no result.")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred during the analysis.",
            )

        logger.info("Resume analysis completed successfully.")
        return analysis_result

    except HTTPException as http_exc:
        # Re-raise HTTPException to ensure FastAPI handles it
        raise http_exc
    except Exception as e:
        logger.exception(f"An unexpected error occurred during resume analysis: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during the analysis.",
        )
