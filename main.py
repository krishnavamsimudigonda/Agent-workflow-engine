import uuid
from fastapi import FastAPI, HTTPException
from models import RunGraphRequest, RunGraphResponse, CreateGraphRequest, WorkflowState
from workflows import create_code_review_workflow

app = FastAPI(title="AI Workflow Engine")

# In-memory storage
GRAPHS = {}
RUNS = {}

# Pre-load our example workflow
GRAPHS["code-review-agent"] = create_code_review_workflow()

@app.post("/graph/create")
async def create_graph(request: CreateGraphRequest):
    """
    Endpoint to register a new graph structure. 
    """
    graph_id = str(uuid.uuid4())
    # In a real dynamic system, we would parse nodes/edges here.
    return {"graph_id": graph_id, "message": "Graph blueprint created (mock)"}

@app.post("/graph/run", response_model=RunGraphResponse)
async def run_graph(request: RunGraphRequest):
    """Executes a workflow given an ID and initial state."""
    
    # 1. Retrieve Graph
    engine = GRAPHS.get(request.graph_id) or GRAPHS.get("code-review-agent")
    
    if not engine:
        raise HTTPException(status_code=404, detail="Graph not found")

    # 2. Initialize State
    try:
        state = WorkflowState(**request.initial_state)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid state: {str(e)}")

    # 3. Run Workflow
    final_state = await engine.run(state)
    
    # 4. Save Run History
    run_id = str(uuid.uuid4())
    
    # --- UPDATED: Use model_dump() instead of dict() ---
    RUNS[run_id] = final_state.model_dump()

    return RunGraphResponse(
        run_id=run_id,
        final_state=final_state.model_dump(),
        execution_log=final_state.steps_log
    )

@app.get("/graph/state/{run_id}")
async def get_run_state(run_id: str):
    """Returns the state of a past workflow run."""
    if run_id not in RUNS:
        raise HTTPException(status_code=404, detail="Run ID not found")
    return RUNS[run_id]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)