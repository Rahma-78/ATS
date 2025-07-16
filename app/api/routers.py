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

router = APIRouter()

@router.post("/analyze/", response_model=AnalysisResult)
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
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No resume file provided."
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

        analysis_result = await run_in_threadpool(analyzer.get_structured_analysis, resume_text, job_description)
        if not analysis_result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred during the analysis.",
            )

        return analysis_result

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        )
