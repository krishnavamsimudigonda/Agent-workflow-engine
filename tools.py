# Simple dictionary registry
TOOL_REGISTRY = {}

def register_tool(name):
    def decorator(func):
        TOOL_REGISTRY[name] = func
        return func
    return decorator

# --- Tools Definition ---

@register_tool("detect_smells")
def detect_smells(code: str):
    """Mock tool to find issues in code."""
    # Logic: if code contains 'bad', it's an issue
    issues = []
    if "global" in code:
        issues.append("Avoid global variables")
    if "eval" in code:
        issues.append("Avoid eval()")
    if len(code) > 100:
        issues.append("Function too long")
    return issues

@register_tool("calculate_complexity")
def calculate_complexity(code: str):
    """Mock tool to calculate cyclomatic complexity."""
    return code.count("if") + code.count("for") + 1