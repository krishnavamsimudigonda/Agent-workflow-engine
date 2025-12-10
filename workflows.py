import random
from engine import WorkflowEngine
from models import WorkflowState
from tools import TOOL_REGISTRY

# --- Node Functions ---

def node_extract(state: WorkflowState) -> WorkflowState:
    # Simulate extracting functions
    state.functions = [f"func_{i}" for i in range(3)]
    return state

def node_complexity(state: WorkflowState) -> WorkflowState:
    # Use tool from registry
    tool = TOOL_REGISTRY.get("calculate_complexity")
    score = tool(state.code) if tool else 0
    state.complexity_score = score
    return state

def node_detect_issues(state: WorkflowState) -> WorkflowState:
    # Use tool from registry
    tool = TOOL_REGISTRY.get("detect_smells")
    issues = tool(state.code) if tool else []
    state.issues = issues
    return state

def node_suggest_improvements(state: WorkflowState) -> WorkflowState:
    # Simulate AI suggestions
    if state.issues:
        # Simulate fixing one issue per loop to demonstrate looping
        fixed = state.issues.pop(0) 
        state.steps_log.append(f"Fixed issue: {fixed}")
        state.quality_score += 20
    else:
        state.quality_score = 100
    return state

# --- Conditional Logic ---

def check_quality_gate(state: WorkflowState) -> str:
    # Branching/Looping Logic [cite: 12, 13]
    if state.quality_score >= 80:
        return None  # End workflow
    else:
        return "suggest_improvements" # Loop back

# --- Graph Assembly ---

def create_code_review_workflow() -> WorkflowEngine:
    engine = WorkflowEngine()
    
    # 1. Register Nodes
    engine.add_node("extract", node_extract)
    engine.add_node("complexity", node_complexity)
    engine.add_node("detect_issues", node_detect_issues)
    engine.add_node("suggest_improvements", node_suggest_improvements)
    
    # 2. Define Flow (Edges)
    engine.set_entry_point("extract")
    engine.add_edge("extract", "complexity")
    engine.add_edge("complexity", "detect_issues")
    engine.add_edge("detect_issues", "suggest_improvements")
    
    # 3. Define Loop (Conditional Edge)
    # After suggestions, check if we need to loop or end
    engine.add_conditional_edge("suggest_improvements", check_quality_gate)
    
    return engine