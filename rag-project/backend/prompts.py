def build_recommendation_prompt(requirements: dict, context_docs: list[str]) -> str:
    context = "\n\n---\n\n".join(context_docs) if context_docs else "No reference docs available."

    return f"""
You are a senior cloud solutions architect with deep expertise in AWS, Azure, and GCP.

Using the validated architecture references below, analyze the user's workload requirements
and return a structured JSON recommendation comparing all three cloud providers.

## Validated Architecture References
{context}

## User Workload Requirements
- App name: {requirements.get('app_name')}
- Workload type: {requirements.get('workload_type')}
- User scale: {requirements.get('user_scale')}
- Traffic pattern: {requirements.get('traffic_pattern')}
- Compute preference: {requirements.get('compute_preference')}
- Database type: {requirements.get('database_type')}
- High availability: {requirements.get('high_availability')}
- Disaster recovery: {requirements.get('disaster_recovery')}
- Budget priority: {requirements.get('budget_priority')}
- Preferred region: {requirements.get('preferred_region')}
- Compliance: {requirements.get('compliance')}
- Team preference: {requirements.get('team_preference')}
- Additional context: {requirements.get('additional_context')}

## Scoring Instructions
Score each provider from 0 to 100 using these weighted dimensions:
- Requirement fit (35%): How well provider services match the workload type and compute preference
- Cost alignment (25%): How well pricing fits the budget priority
- Operational simplicity (15%): Ease of management and reduced operational overhead
- Reliability and HA support (15%): Native support for high availability and disaster recovery
- Team familiarity (10%): Alignment with team preference and existing tools

Rules:
- If team_preference is set, add up to 8 points to that provider
- If compliance is hipaa/soc2/pci, add 3 points to AWS and Azure
- If budget_priority is low and workload suits serverless, add 5 points to GCP
- If workload_type is ml_platform, add 5 points to GCP for TPU advantage
- If workload_type is batch and scale is large, add 3 points to Azure for HPC strength
- If team_preference is neutral and no strong signals exist, scores must be within 5 points of each other

## STRICT JSON FORMAT RULES
- "best_provider" must be a lowercase string: "aws", "azure", or "gcp"
- "architecture_summary" must be a single plain text string, NOT a dict or object
- "assumptions" must be a flat array of plain text strings, NOT a dict or object
- "recommendations" must be an ARRAY of exactly 3 objects, one per provider
- Each recommendation object must have: provider, score, strengths, service_mapping, cost_estimate
- "strengths" must be an array of plain text strings
- "service_mapping" must be a flat dict with string keys and string values
- "cost_estimate" must be an object with keys: monthly_min (integer), monthly_max (integer), currency ("USD"), breakdown (flat dict of service: estimated cost range string)
- Base cost estimates on the workload scale, compute preference, database type, and HA requirements
- Do NOT include "terraform" or "mermaid_diagram" keys

## Required JSON Structure
Return ONLY this JSON, no markdown, no explanation:

{{
  "best_provider": "aws",
  "architecture_summary": "Plain text summary of the recommended architecture as a single string.",
  "assumptions": [
    "Plain text assumption 1",
    "Plain text assumption 2"
  ],
  "recommendations": [
    {{
      "provider": "aws",
      "score": 85.0,
      "strengths": ["Strength one", "Strength two", "Strength three"],
      "service_mapping": {{
        "compute": "ECS Fargate",
        "database": "Amazon RDS for PostgreSQL",
        "storage": "Amazon S3",
        "network": "VPC + ALB",
        "observability": "CloudWatch"
      }},
      "cost_estimate": {{
        "monthly_min": 150,
        "monthly_max": 350,
        "currency": "USD",
        "breakdown": {{
          "compute": "$80-$180/mo",
          "database": "$50-$120/mo",
          "storage": "$5-$20/mo",
          "network": "$10-$25/mo",
          "observability": "$5-$10/mo"
        }}
      }}
    }},
    {{
      "provider": "azure",
      "score": 78.0,
      "strengths": ["Strength one", "Strength two", "Strength three"],
      "service_mapping": {{
        "compute": "Azure Container Apps",
        "database": "Azure Database for PostgreSQL",
        "storage": "Azure Blob Storage",
        "network": "VNet + Application Gateway",
        "observability": "Azure Monitor"
      }},
      "cost_estimate": {{
        "monthly_min": 160,
        "monthly_max": 370,
        "currency": "USD",
        "breakdown": {{
          "compute": "$85-$190/mo",
          "database": "$55-$130/mo",
          "storage": "$5-$20/mo",
          "network": "$10-$25/mo",
          "observability": "$5-$10/mo"
        }}
      }}
    }},
    {{
      "provider": "gcp",
      "score": 80.0,
      "strengths": ["Strength one", "Strength two", "Strength three"],
      "service_mapping": {{
        "compute": "Cloud Run",
        "database": "Cloud SQL for PostgreSQL",
        "storage": "Cloud Storage",
        "network": "VPC + HTTPS Load Balancer",
        "observability": "Cloud Monitoring"
      }},
      "cost_estimate": {{
        "monthly_min": 130,
        "monthly_max": 310,
        "currency": "USD",
        "breakdown": {{
          "compute": "$65-$160/mo",
          "database": "$45-$110/mo",
          "storage": "$5-$15/mo",
          "network": "$10-$20/mo",
          "observability": "$5-$10/mo"
        }}
      }}
    }}
  ]
}}
"""


def build_terraform_prompt(provider: str, requirements: dict) -> str:
    provider_details = {
        "aws": {
            "region_var": "us-east-1",
            "compute_hint": "Use ECS Fargate or Lambda depending on compute preference.",
            "db_hint": "Use Amazon RDS or DynamoDB depending on database type.",
        },
        "azure": {
            "region_var": "eastus",
            "compute_hint": "Use Azure Container Apps or Azure Functions depending on compute preference.",
            "db_hint": "Use Azure Database for PostgreSQL or Cosmos DB depending on database type.",
        },
        "gcp": {
            "region_var": "us-central1",
            "compute_hint": "Use Cloud Run or GKE depending on compute preference.",
            "db_hint": "Use Cloud SQL or Firestore depending on database type.",
        },
    }.get(provider, {})

    return f"""
You are a senior DevOps engineer and Terraform expert specializing in {provider.upper()} infrastructure.

Generate production-ready Terraform code for the following workload. The code must be complete,
real, and immediately usable — not a placeholder or skeleton.

## Workload Requirements
- App name: {requirements.get('app_name')}
- Workload type: {requirements.get('workload_type')}
- Compute preference: {requirements.get('compute_preference')}
- Database type: {requirements.get('database_type')}
- High availability: {requirements.get('high_availability')}
- Disaster recovery: {requirements.get('disaster_recovery')}
- Preferred region: {requirements.get('preferred_region') or provider_details.get('region_var')}
- Compliance: {requirements.get('compliance')}
- Additional context: {requirements.get('additional_context')}

## Provider Guidance
- Compute: {provider_details.get('compute_hint')}
- Database: {provider_details.get('db_hint')}

## Requirements for the Terraform code
- Include a provider block with the correct {provider.upper()} provider and region variable
- Include a variables.tf-style variable block for region, app_name, and environment
- Include core infrastructure resources: compute, database, networking (VPC/VNet/VPC), and IAM roles
- Include outputs for key resource endpoints (e.g. load balancer DNS, database endpoint)
- Use best practices: tagging, separate resource naming, no hardcoded secrets
- If high_availability is true, configure multi-AZ or equivalent redundancy

## Strict Output Rules
- Return ONLY raw HCL Terraform code
- No markdown code fences, no backticks, no triple backticks
- No explanation, no comments outside of HCL inline # comments
- Start directly with the terraform {{ }} block
"""


