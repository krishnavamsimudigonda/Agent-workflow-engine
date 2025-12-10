from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional

# --- State Models ---
class WorkflowState(BaseModel):
    # Base fields for Option A
    code: str = ""
    functions: List[str] = []
    complexity_score: int = 0
    issues: List[str] = []
    quality_score: int = 0
    steps_log: List[str] = []  # To track execution history

# --- API Models ---
class CreateGraphRequest(BaseModel):
    nodes: List[str]
    edges: Dict[str, str]

class RunGraphRequest(BaseModel):
    graph_id: str
    initial_state: Dict[str, Any]

class RunGraphResponse(BaseModel):
    run_id: str
    final_state: Dict[str, Any]
    execution_log: List[str]