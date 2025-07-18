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
    Represents the structured analysis of a resume against a job description.
    """
    match_percentage: int = Field(
        ..., 
        description="The calculated match score between the resume and the job description.",
        example=85
    )
    strengths: List[str] = Field(
        ..., 
        description="A list of key strengths and qualifications identified in the resume.",
        example=["5+ years of experience in Python", "Experience with FastAPI and Pydantic"]
    )
    weaknesses: List[str] = Field(
        ..., 
        description="A list of key weaknesses or gaps identified in the resume.",
        example=["No experience with cloud platforms (AWS, GCP, Azure)"]
    )
    candidate_summary: str = Field(
        ..., 
        description="A brief summary of the candidate’s overall fit for the role.",
        example="The candidate is a strong fit for the role, with extensive experience in Python and web development."
    )
    recommendations: str = Field(
        ..., 
        description="Actionable recommendations for the candidate to improve their profile.",
        example="The candidate should consider gaining experience with cloud platforms to be a more competitive applicant."
    )

class AnalysisRequest(BaseModel):
    """
    Defines the request body for the analysis endpoint.
    """
    job_description: str
