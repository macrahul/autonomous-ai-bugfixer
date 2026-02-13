from agent.executors.zero_division import ZeroDivisionExecutor
from agent.executors.index_error import IndexErrorExecutor
from agent.executors.key_error import KeyErrorExecutor

EXECUTORS = [
    ZeroDivisionExecutor(),
    IndexErrorExecutor(),
    KeyErrorExecutor(),
]

def select_executor(error_log: str):
    for executor in EXECUTORS:
        if executor.applies_to(error_log):
            return executor
    return None