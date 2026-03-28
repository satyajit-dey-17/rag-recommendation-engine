import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from backend.models import WorkloadRequest, AnalysisResponse, ProviderRecommendation
from backend.embeddings import embed_requirements
from backend.rag import query_similar
from backend.prompts import build_recommendation_prompt, build_terraform_prompt

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def safe_string(value) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return " | ".join(f"{k}: {v}" for k, v in value.items())
    return str(value)


def safe_list(value) -> list:
    if isinstance(value, list):
        return [str(i) for i in value]
    if isinstance(value, dict):
        return [f"{k}: {v}" for k, v in value.items()]
    return [str(value)]


def generate_terraform(provider: str, req_dict: dict) -> str:
    prompt = build_terraform_prompt(provider, req_dict)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a senior DevOps engineer expert in Terraform. "
                    "Return only raw valid HCL Terraform code. "
                    "No markdown fences, no backticks, no explanation. Only HCL."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()


def generate_mermaid(provider: str, req_dict: dict, service_mapping: dict) -> str:
    ha = req_dict.get("high_availability", False)
    dr = req_dict.get("disaster_recovery", False)

    # Map service_mapping keys to safe node IDs and labels
    def node_id(key):
        return key.replace(" ", "_").replace("-", "_").upper()

    def safe_label(label):
        return label.replace("/", "-").replace('"', "")

    lines = ["flowchart TD"]

    # Fixed nodes
    lines.append('    User(["🌐 User"])')

    network = service_mapping.get("network")
    compute = service_mapping.get("compute")
    database = service_mapping.get("database")
    storage = service_mapping.get("storage")
    observability = service_mapping.get("observability")

    if network:
        lines.append(f'    NETWORK["{safe_label(network)}"]')
    if compute:
        if ha:
            lines.append(f'    COMPUTE_1["{safe_label(compute)} - Instance 1"]')
            lines.append(f'    COMPUTE_2["{safe_label(compute)} - Instance 2"]')
        else:
            lines.append(f'    COMPUTE["{safe_label(compute)}"]')
    if database:
        lines.append(f'    DATABASE[("{safe_label(database)}")]')
    if storage:
        lines.append(f'    STORAGE["{safe_label(storage)}"]')
    if observability:
        lines.append(f'    OBS["{safe_label(observability)}"]')
    if dr:
        lines.append('    DR["DR Region"]')

    # Edges
    if network:
        lines.append("    User --> NETWORK")
        if ha:
            lines.append("    NETWORK --> COMPUTE_1")
            lines.append("    NETWORK --> COMPUTE_2")
        elif compute:
            lines.append("    NETWORK --> COMPUTE")
    elif compute:
        lines.append("    User --> COMPUTE" if not ha else "    User --> COMPUTE_1\n    User --> COMPUTE_2")

    compute_ref = "COMPUTE_1" if ha else "COMPUTE"
    if database:
        lines.append(f"    {compute_ref} --> DATABASE")
    if storage:
        lines.append(f"    {compute_ref} --> STORAGE")
    if observability:
        lines.append(f"    {compute_ref} --> OBS")
        if database:
            lines.append("    DATABASE --> OBS")
    if dr and database:
        lines.append("    DATABASE --> DR")

    return "\n".join(lines)


def analyze_requirements(req: WorkloadRequest) -> AnalysisResponse:
    req_dict = req.model_dump()

    query_embedding = embed_requirements(req_dict)
    context_docs = query_similar(query_embedding, n_results=5)
    prompt = build_recommendation_prompt(req_dict, context_docs)

    # Call 1: Recommendation JSON
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a senior cloud solutions architect. "
                    "Always respond with valid JSON only. No markdown, no explanation. "
                    "Your response must contain exactly these top-level keys: "
                    "best_provider (string), architecture_summary (string), "
                    "assumptions (array of strings), recommendations (array of 3 objects). "
                    "Do NOT include terraform or mermaid_diagram keys."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        response_format={"type": "json_object"},
    )

    raw = response.choices[0].message.content
    data = json.loads(raw)

    recommendations_raw = data.get("recommendations", [])
    if isinstance(recommendations_raw, dict):
        recommendations_raw = list(recommendations_raw.values())

    recommendations = [
        ProviderRecommendation(
            provider=r["provider"].lower(),
            score=float(r.get("score", 0.0)),
            strengths=safe_list(r.get("strengths", [])),
            service_mapping={k: str(v) for k, v in r.get("service_mapping", {}).items()},
            cost_estimate=r.get("cost_estimate", None),
        )
        for r in recommendations_raw
        if isinstance(r, dict)
    ]

    best_provider = data.get("best_provider", "aws").lower()

    best_service_mapping = next(
        (r.service_mapping for r in recommendations if r.provider == best_provider),
        {}
    )

    # Call 2: Terraform
    terraform_code = generate_terraform(best_provider, req_dict)

    # Call 3: Mermaid diagram
    mermaid_diagram = generate_mermaid(best_provider, req_dict, best_service_mapping)

    summary = {
        "app_name": req.app_name,
        "workload_type": req.workload_type,
        "compute_preference": req.compute_preference,
        "database_type": req.database_type,
        "budget_priority": req.budget_priority,
        "preferred_region": req.preferred_region,
    }

    return AnalysisResponse(
        summary=summary,
        recommendations=[r.model_dump() for r in recommendations],
        best_provider=best_provider,
        architecture_summary=safe_string(data.get("architecture_summary", "")),
        terraform=terraform_code,
        assumptions=safe_list(data.get("assumptions", [])),
        mermaid_diagram=mermaid_diagram,
    )