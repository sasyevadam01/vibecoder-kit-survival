"""
Deterministic FSM Orchestrator Template.
Provides an executable framework for multi-agent system state management.
No em-dashes or forbidden fonts used.
"""

import sys
import logging
from typing import Dict, Any, Callable, Optional, Set

# Setup simple logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)
logger = logging.getLogger("FSMOrchestrator")


class State:
    """
    Represents a discrete state within the finite state machine.
    """
    def __init__(
        self,
        name: str,
        action_fn: Callable[[Dict[str, Any]], Dict[str, Any]],
        transition_fn: Optional[Callable[[Dict[str, Any]], str]] = None
    ):
        self.name = name
        self.action_fn = action_fn
        self.transition_fn = transition_fn

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the logic associated with this state and returns the updated context.
        """
        logger.info(f"Entering State: {self.name}")
        return self.action_fn(context)

    def next_state(self, context: Dict[str, Any]) -> str:
        """
        Determines the next state based on the current context.
        """
        if self.transition_fn:
            next_s = self.transition_fn(context)
            logger.info(f"Transition evaluated from {self.name} to {next_s}")
            return next_s
        return "SUCCESS"


class StateMachine:
    """
    Orchestrates execution of states, managing transitions and context safety.
    """
    def __init__(self, initial_state: str, max_iterations: int = 20):
        self.states: Dict[str, State] = {}
        self.initial_state = initial_state
        self.max_iterations = max_iterations
        self.visited_states: Set[str] = set()

    def add_state(self, state: State) -> None:
        """
        Registers a state inside the machine.
        """
        self.states[state.name] = state

    def run(self, initial_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Runs the state machine starting from the initial state.
        """
        context = initial_context.copy()
        current_state_name = self.initial_state
        iterations = 0

        while current_state_name != "SUCCESS" and current_state_name != "FAILURE":
            if iterations >= self.max_iterations:
                logger.error("State machine reached maximum safety iterations limit.")
                context["error"] = "Max iterations reached"
                break

            state = self.states.get(current_state_name)
            if not state:
                logger.error(f"State '{current_state_name}' is not registered.")
                context["error"] = f"State {current_state_name} not found"
                break

            try:
                # Execute action
                context = state.execute(context)
                
                # Determine next state
                next_state_name = state.next_state(context)
                current_state_name = next_state_name
            except Exception as e:
                logger.exception(f"Exception encountered in state {current_state_name}: {str(e)}")
                context["error"] = str(e)
                current_state_name = "FAILURE"
                break

            iterations += 1

        logger.info(f"FSM finished execution. Final state: {current_state_name}")
        context["final_state"] = current_state_name
        return context


# --- Example Execution Scenario ---
def fetch_action(context: Dict[str, Any]) -> Dict[str, Any]:
    logger.info("Fetching raw input data...")
    context["raw_data"] = "  VibeCoder-Kit-Survival-Payload  "
    return context


def validate_action(context: Dict[str, Any]) -> Dict[str, Any]:
    logger.info("Validating clean formats...")
    raw = context.get("raw_data", "")
    cleaned = raw.strip()
    context["clean_data"] = cleaned
    # Mark validity
    context["is_valid"] = len(cleaned) > 0
    return context


def process_action(context: Dict[str, Any]) -> Dict[str, Any]:
    logger.info("Processing valid payload...")
    data = context.get("clean_data", "")
    context["result"] = f"Processed: {data.upper()}"
    return context


def handle_error_action(context: Dict[str, Any]) -> Dict[str, Any]:
    logger.error("Handling validation failure...")
    context["result"] = "Fallback recovery engaged"
    return context


# Transition Logic
def validate_transition(context: Dict[str, Any]) -> str:
    if context.get("is_valid"):
        return "process_data"
    return "handle_error"


if __name__ == "__main__":
    logger.info("Initializing State Machine demo...")
    
    # 1. Define states
    s_fetch = State("fetch_data", fetch_action, lambda ctx: "validate_data")
    s_validate = State("validate_data", validate_action, validate_transition)
    s_process = State("process_data", process_action, lambda ctx: "SUCCESS")
    s_error = State("handle_error", handle_error_action, lambda ctx: "SUCCESS")

    # 2. Build machine
    fsm = StateMachine(initial_state="fetch_data")
    fsm.add_state(s_fetch)
    fsm.add_state(s_validate)
    fsm.add_state(s_process)
    fsm.add_state(s_error)

    # 3. Execute
    output = fsm.run({})
    print(f"\nFinal Context Results: {output}")
