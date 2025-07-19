# -*- coding: utf-8 -*-
"""
Defines the Pydantic schemas for the analysis API.
"""

from pydantic import BaseModel, Field
from typing import List

class Strengths(BaseModel):
    """
    Describes the candidate's strengths.
    """
    skills: List[str] = Field(
        description="Specific skills that align with the job description."
    )
    experience: List[str] = Field(
        description="Relevant experiences that match the role's requirements."
    )

class Weaknesses(BaseModel):
    """
    Describes the candidate's weaknesses.
    """
    skills: List[str] = Field(
        description="Critical skills mentioned in the job description that are missing from the resume."
    )
    experience: List[str] = Field(
        description="Experience gaps, such as years of experience or specific industry knowledge."
    )

class Recommendations(BaseModel):
    """
    Provides actionable recommendations for the candidate.
    """
    focus_areas: List[str] = Field(
        description="Key areas the candidate should focus on to improve their profile."
    )
    online_courses: List[str] = Field(
        description="Specific online courses (including links) that can help bridge skill gaps."
    )

class AnalysisResult(BaseModel):
    """
    Defines the structured output for the resume analysis.
    """
    candidate_summary: str = Field(
        description="A 2-3 sentence summary of the candidate's profile and overall suitability for the role, based on the final, penalized score."
    )
    match_percentage: int = Field(
        description="A realistic, final match percentage, rounded to the nearest whole number. This score must be calculated after applying significant penalties for any missing critical requirements (e.g., required skills, years of experience)."
    )
    strengths: Strengths = Field(
        description="A detailed breakdown of the candidate's strengths."
    )
    weaknesses: Weaknesses = Field(
        description="A detailed breakdown of the candidate's weaknesses and skill gaps."
    )
    recommendations: Recommendations = Field(
        description="Actionable recommendations for the candidate to improve their qualifications for the role."
    )

class AnalysisRequest(BaseModel):
    """
    Defines the request body for the analysis endpoint.
    """
    job_description: str
