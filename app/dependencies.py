# -*- coding: utf-8 -*-
"""
FastAPI dependencies.
"""

from functools import lru_cache
from app.core.config import settings
from app.services.analysis_service import ATSAnalyzer

@lru_cache()
def get_analyzer() -> ATSAnalyzer:
    """
    Returns a cached instance of the ATSAnalyzer.
    """
    return ATSAnalyzer(
        groq_api_key=settings.GROQ_API_KEY,
        model_name=settings.GROQ_MODEL_NAME
    )
