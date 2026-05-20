import time
from dataclasses import dataclass, field
from agents.planner import plan_query
from agents.sql_generator import generate_sql
from agents.executor import execute_with_retry
from agents.summarizer import summarize
from logger import log_step


@dataclass
class AgentState:
    question: str
    plan: dict = field(default_factory=dict)
    sql: str = ""
    result: list = field(default_factory=list)
    summary: str = ""
    error: str | None = None
    retry_count: int = 0
    success: bool = False
    latency_ms: float = 0.0


def run_workflow(question: str) -> AgentState:
    """
    Full agentic pipeline:
      1. Plan  →  2. Generate SQL  →  3. Execute (with retry)  →  4. Summarize
    """
    state = AgentState(question=question)
    start = time.time()

    # Step 1: Plan
    log_step(question, "plan_start", {})
    state.plan = plan_query(question)
    log_step(question, "plan_complete", {"plan": state.plan})

    # Step 2: Generate SQL
    log_step(question, "sql_generate_start", {})
    state.sql = generate_sql(state.plan)
    log_step(question, "sql_generate_complete", {"sql": state.sql})

    # Step 3: Execute with retry
    log_step(question, "execution_start", {"sql": state.sql})
    exec_result = execute_with_retry(question, state.sql)
    state.sql = exec_result["sql"]
    state.result = exec_result["result"]
    state.error = exec_result["error"]
    state.retry_count = exec_result["retry_count"]
    state.success = exec_result["success"]

    log_step(question, "execution_complete", {
        "success": state.success,
        "retry_count": state.retry_count,
        "error": state.error,
        "row_count": len(state.result),
    })

    # Step 4: Summarize
    if state.success:
        state.summary = summarize(question, state.sql, state.result)
    else:
        state.summary = (
            f"I was unable to answer your question after {state.retry_count} "
            f"attempts. Last error: {state.error}"
        )

    state.latency_ms = round((time.time() - start) * 1000, 2)
    log_step(question, "workflow_complete", {
        "success": state.success,
        "latency_ms": state.latency_ms,
        "summary": state.summary,
    })

    return state
