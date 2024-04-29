from enum import Enum


class ExecOutcome(Enum):
    PASSED = "PASSED"  # code executes and output matches expected output
    WRONG_ANSWER = (
        "WRONG_ANSWER"  # code executes and output does NOT matches expected output
    )
    TIME_LIMIT_EXCEEDED = "TIME_LIMIT_EXCEEDED"  # code executes and didn't exit in time, output is ignored in this case
    RUNTIME_ERROR = "RUNTIME_ERROR"  # code failed to execute (crashed)
    COMPILATION_ERROR = "COMPILATION_ERROR"  # code failed to compile
    MEMORY_LIMIT_EXCEEDED = (
        "MEMORY_LIMIT_EXCEEDED"  # code exceeded memory limit during execution
    )
