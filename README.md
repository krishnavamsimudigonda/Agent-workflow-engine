# Agnet Workflow Engine

A pure-Python backend engine designed to orchestrate state-based workflows. This system allows for the definition of nodes (tasks), directed edges (flow), and conditional logic (branching/looping) to build complex agentic behaviors without heavy dependencies.

It serves as a simplified, functional implementation of concepts found in frameworks like LangGraph, focusing on clarity, type safety, and clean architecture.

##  System Architecture

The project follows a modular design to separate the core engine logic from the API layer and specific workflow implementations.

```text
AI_Workflow_Engine
├── engine.py        # Core Logic: Handles graph traversal, state propagation, and cyclic routing.
├── models.py        # Data Layer: Pydantic models for strict state validation.
├── workflows.py     # Implementation: Defines the specific "Code Review Agent" logic.
├── tools.py         # Registry: Decoupled function registry for modular tool use.
├── main.py          # API Layer: FastAPI endpoints for interaction.

```
## Key Features
Directed Cyclic Graphs: Unlike simple pipelines, this engine supports loops (cycles), allowing workflows to "retry" or "refine" outputs based on dynamic criteria.

Deterministic State Management: Uses Pydantic to enforce a strict schema for the shared state, ensuring data consistency across different nodes.

Hybrid Execution: The engine is capable of handling both synchronous and asynchronous node execution strategies.

Conditional Routing: Dynamic edges allow the workflow to change its path at runtime based on the state (e.g., if quality < 80: return "retry").

 Setup & Installation
Prerequisites
Python 3.8+



1. Clone the Repository


git clone <ASDFGHJKL> 
cd AI_Workflow_Engine

2. Configure Environment
It is recommended to use a virtual environment.


### Windows
python -m venv venv
venv\Scripts\activate

### Mac/Linux
python3 -m venv venv
source venv/bin/activate

3. Install Dependencies

pip install fastapi uvicorn

## Usage Guide: Testing the Agent
The engine comes pre-loaded with a Code Review Agent designed to demonstrate the graph's looping capabilities. It analyzes code, detects issues, and loops through a refinement process until quality thresholds are met.

1. Run the Test
Navigate to the Swagger UI: http://localhost:8000/docs

Expand the POST /graph/run endpoint.

Click Try it out and paste the following payload to simulate "bad" code:

JSON


{
  "graph_id": "code-review-agent",
  "initial_state": {
    "code": "def bad_code(): global x; eval('2 + 2');",
    "quality_score": 0
  }
} 

2. Expected Output
When you execute the request, you will receive a JSON response containing the execution logs.

What to look for in the logs:

Analysis: The engine detects global and eval usage.

Loop 1: It fixes the "global variables" issue → Quality Score increases.

Loop 2: It fixes the "eval()" issue → Quality Score increases further.

Completion: The score meets the threshold (100), and the workflow exits.

Sample JSON Response:

JSON

{
  "run_id": "550e8400-e29b-41d4-a716-446655440000",
  "final_state": {
    "code": "def bad_code(): global x; eval('2 + 2');",
    "quality_score": 100,
    "issues": []
  },
  "execution_log": [
    "Executed extract",
    "Executed complexity",
    "Executed detect_issues",
    "Executed suggest_improvements",
    "Fixed issue: Avoid global variables",
    "Executed suggest_improvements",
    "Fixed issue: Avoid eval()",
    "Executed suggest_improvements"
  ]
}
