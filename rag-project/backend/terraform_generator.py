import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from backend.prompts import build_terraform_prompt

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_terraform(provider: str, requirements: dict) -> str:
    prompt = build_terraform_prompt(provider, requirements)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a senior DevOps engineer and Terraform expert. "
                    "Return only valid HCL Terraform code. No markdown fences, no explanation."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
    )

    return response.choices[0].message.content.strip()