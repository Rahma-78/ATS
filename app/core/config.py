# -*- coding: utf-8 -*-
"""
Application configuration settings.
"""

import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """
    Defines application settings.
    """
    PROJECT_NAME: str = "ATS Resume Analyzer"
    PROJECT_DESCRIPTION: str = "A powerful tool to analyze resumes against job descriptions, providing a detailed analysis of a candidate's suitability for a role."
    API_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL_NAME: str = os.getenv("GROQ_MODEL_NAME", "")

    class Config:
        case_sensitive = True

settings = Settings()
