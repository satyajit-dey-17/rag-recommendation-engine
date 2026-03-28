import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def embed_text(text: str) -> list[float]:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )
    return response.data[0].embedding


def embed_requirements(req_dict: dict) -> list[float]:
    text = (
        f"Workload: {req_dict.get('workload_type')}. "
        f"Compute: {req_dict.get('compute_preference')}. "
        f"Database: {req_dict.get('database_type')}. "
        f"Scale: {req_dict.get('user_scale')}. "
        f"Traffic: {req_dict.get('traffic_pattern')}. "
        f"HA: {req_dict.get('high_availability')}. "
        f"DR: {req_dict.get('disaster_recovery')}. "
        f"Budget: {req_dict.get('budget_priority')}. "
        f"Compliance: {req_dict.get('compliance')}. "
        f"Region: {req_dict.get('preferred_region')}."
    )
    return embed_text(text)