import asyncio
import inspect
from typing import Callable, Dict, Any, Optional
from models import WorkflowState

class WorkflowEngine:
    def __init__(self):
        self.nodes: Dict[str, Callable] = {}
        self.edges: Dict[str, str] = {}
        self.conditional_edges: Dict[str, Callable[[WorkflowState], str]] = {}
        self.entry_point: Optional[str] = None

    def add_node(self, name: str, func: Callable):
        self.nodes[name] = func

    def set_entry_point(self, name: str):
        self.entry_point = name

    def add_edge(self, source: str, target: str):
        self.edges[source] = target

    def add_conditional_edge(self, source: str, condition_func: Callable[[WorkflowState], str]):
        self.conditional_edges[source] = condition_func

    async def run(self, initial_state: WorkflowState):
        if not self.entry_point:
            raise ValueError("No entry point defined.")

        current_node_name = self.entry_point
        state = initial_state
        
        # Safety break for loops
        max_steps = 20 
        steps = 0

        while current_node_name and steps < max_steps:
            steps += 1
            node_func = self.nodes.get(current_node_name)
            
            if not node_func:
                state.steps_log.append(f"Error: Node {current_node_name} not found.")
                break

            # --- UPDATED: Smart Async/Sync Execution ---
            # This checks if the function is async and awaits it if necessary
            try:
                if inspect.iscoroutinefunction(node_func):
                    state = await node_func(state)
                else:
                    state = node_func(state)
            except Exception as e:
                state.steps_log.append(f"Error executing {current_node_name}: {str(e)}")
                break
                
            state.steps_log.append(f"Executed {current_node_name}")

            # Determine next node
            if current_node_name in self.conditional_edges:
                next_node = self.conditional_edges[current_node_name](state)
                current_node_name = next_node
            elif current_node_name in self.edges:
                current_node_name = self.edges[current_node_name]
            else:
                current_node_name = None

        return state