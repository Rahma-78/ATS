# -*- coding: utf-8 -*-
"""
API endpoints for the analysis service.
"""

import logging
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
    if not resume.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No resume file provided."
        )

    try:
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
            logging.error("Analysis failed: get_structured_analysis returned None.")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get a structured analysis from the model. The prompt may be too complex or the model may be unable to generate a valid JSON response.",
            )

        return analysis_result

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logging.error(f"An unexpected error occurred during analysis: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during the analysis process.",
        )
