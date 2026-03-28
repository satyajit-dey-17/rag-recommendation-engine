from pydantic import BaseModel
from typing import Optional


class ProviderRecommendation(BaseModel):
    provider: str
    score: float
    strengths: list[str]
    service_mapping: dict[str, str]
    cost_estimate: Optional[dict] = None


class WorkloadRequest(BaseModel):
    app_name: str
    workload_type: str
    user_scale: Optional[str] = None
    traffic_pattern: Optional[str] = None
    compute_preference: Optional[str] = None
    database_type: Optional[str] = None
    high_availability: Optional[bool] = False
    disaster_recovery: Optional[bool] = False
    budget_priority: Optional[str] = None
    preferred_region: Optional[str] = None
    compliance: Optional[str] = None
    team_preference: Optional[str] = None
    additional_context: Optional[str] = None


class AnalysisResponse(BaseModel):
    model_config = {"arbitrary_types_allowed": True}

    summary: dict
    recommendations: list[ProviderRecommendation]
    best_provider: str
    architecture_summary: str
    terraform: str
    assumptions: list[str]
    mermaid_diagram: Optional[str] = None