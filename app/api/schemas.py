# -*- coding: utf-8 -*-
"""
Defines the Pydantic schemas for the analysis API.
"""

from pydantic import BaseModel, Field
from typing import List

class AnalysisResult(BaseModel):
    """
    Defines the structured output for the resume analysis.
    """
    candidate_summary: str = Field(
        description="A 2-3 sentence summary of the candidate's profile and overall suitability for the role."
    )
    match_percentage: int = Field(
        description="A realistic, final match percentage, rounded to the nearest whole number."
    )
    strengths: List[str] = Field(
        description="A list of the candidate's strengths."
    )
    weaknesses: List[str] = Field(
        description="A list of the candidate's weaknesses and skill gaps."
    )
    recommendations: List[str] = Field(
        description="Actionable recommendations for the candidate to improve their qualifications for the role."
    )

class AnalysisRequest(BaseModel):
    """
    Defines the request body for the analysis endpoint.
    """
    job_description: str
