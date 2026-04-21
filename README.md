# CloudArch AI: Multi-Cloud Architecture Recommender

An AI-powered cloud solutioning assistant that analyzes application workload requirements and recommends the best-fit cloud provider across **AWS, Azure, and GCP**. The platform generates provider comparisons, cost estimates, architecture summaries, Terraform starter code, and architecture diagrams through an interactive Streamlit interface.

## Features

- Compare **AWS, Azure, and GCP** for a given workload
- Generate **provider recommendations** with scores and service mappings
- Show **estimated monthly cost ranges** and service-level breakdowns
- Create **architecture summaries** based on workload inputs
- Generate **Terraform starter code** for the recommended provider
- Visualize **provider score comparisons** and **cost graphs**
- Render **architecture diagrams** for the recommended design
- Use **FastAPI** for backend APIs and **Streamlit** for frontend visualization

## Tech Stack

### Backend
- Python
- FastAPI
- Uvicorn
- Pydantic
- OpenAI API
- python-dotenv

### Frontend
- Streamlit
- Plotly
- Pandas
- streamlit-mermaid

### Cloud/AI Logic
- LLM-powered recommendation engine
- Terraform code generation
- Cost estimation model
- Multi-provider service mapping

## Project Structure

```bash
multi-cloud-recommender/
│
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── recommender.py
│   ├── prompts.py
│   ├── embeddings.py
│   └── rag.py
│
├── frontend/
│   └── app.py
│
├── requirements.txt
└── README.md
```

## How It Works

1. The user submits workload details such as:
   - workload type
   - compute preference
   - database type
   - traffic pattern
   - HA/DR requirements
   - compliance needs
   - budget priority

2. The backend:
   - processes the request
   - analyzes workload requirements
   - compares AWS, Azure, and GCP
   - returns recommendations, scores, cost estimates, and Terraform code

3. The frontend:
   - displays the recommended provider
   - visualizes provider scores
   - shows service-level cost breakdowns
   - renders architecture diagrams
   - presents Terraform starter code

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/multi-cloud-recommender.git
cd multi-cloud-recommender
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
```

## Running the Application

### Start the backend

```bash
uvicorn backend.main:app --reload
```

### Start the frontend

```bash
streamlit run frontend/app.py
```

## API Endpoint

### POST `/analyze`

Analyzes the workload and returns recommendations.

#### Example Request

```json
{
  "app_name": "ImmigrationIQ",
  "workload_type": "web_api",
  "user_scale": "medium",
  "traffic_pattern": "steady",
  "compute_preference": "containers",
  "database_type": "relational",
  "high_availability": true,
  "disaster_recovery": false,
  "budget_priority": "medium",
  "preferred_region": "us-east-1",
  "compliance": "soc2",
  "team_preference": "aws",
  "additional_context": "Customer-facing application with moderate traffic."
}
```

## Example Output

- Best-fit provider recommendation
- Provider comparison table
- Architecture summary
- Assumptions
- Terraform starter code
- Cost comparison charts
- Architecture diagram

## Key Achievements

- Built an end-to-end **AI-powered cloud recommendation platform**
- Added **provider scoring and cost comparison** across AWS, Azure, and GCP
- Integrated **Terraform generation** for faster infrastructure bootstrapping
- Created a **visual decision-support interface** with charts and diagrams
- Improved robustness with structured parsing and error-handling for LLM responses

## Future Improvements

- Add user authentication
- Save previous analyses
- Improve cost modeling with live pricing APIs
- Export reports as PDF
- Support advanced architecture patterns and workload templates
- Add deployment support for cloud hosting

## Author

**Satyajit**  
Graduate Student in Information Systems at UMBC  
Focused on Cloud Engineering, DevOps, and SRE

## License

This project is licensed under the MIT License.
