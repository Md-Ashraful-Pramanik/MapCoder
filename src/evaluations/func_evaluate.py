from typing import *
import contextlib
import signal

from .executor_utils import function_with_timeout


def evaluate_io(
    sample_io: list[str],
    completion: str,
    timeout: int = 5,
    stop_early: bool = False,
):
    test_log = ""
    passed = True
    for io in sample_io:
        try:
            code = ("from typing import *\n" if "from typing import *" not in completion else "") + \
                completion + "\n" + io + "\n"
            function_with_timeout(
                exec,
                (code, globals()),
                timeout
            )
            test_log += f"passed in test case: {io}\n"
        except Exception as e:
            if stop_early:
                return False, f"failed in test case: {io}\n"
            passed = False
            test_log += f"failed in test case: {io}\n"

    return passed, test_log


def evaluate_io_et(
    sample_io: list[str],
    completion: str,
    timeout: int = 5,
    prompt: str = "",
):
    io = "\n".join(sample_io)
    try:
        code = ("from typing import *\n" if "from typing import *" not in completion else "") + \
            prompt + completion + "\n" + io + "\n"
        function_with_timeout(
            exec,
            (code, globals()),
            timeout
        )
        return True
    except Exception as e:
        return False


def evaluate_functional_correctness(
    problem: Dict,
    completion: str,
    timeout: int = 5,
    test_key: str = "test",
):
    # if problem["name"] == "mbpp_61_count_Substrings":
    #     pass
    try:
        code = ("from typing import *\n" if "from typing import *" not in completion else "") + \
            completion + "\n" + problem[test_key] + \
            "\n" + f"check({problem['entry_point']})"

        function_with_timeout(
            exec,
            (code, globals()),
            timeout
        )
        return "passed"
    except Exception as e:
        return f"failed: {e}"


def evaluate_functional_correctness2(
    problem: Dict,
    completion: str,
    timeout: float = 10,
) -> Dict:

    check_program = (
        # problem["prompt"] +
        "from typing import *\n" +
        completion + "\n" +
        problem["test"] + "\n" +
        f"check({problem['entry_point']})"
    )
    # print(check_program)

    try:
        exec(check_program)
        return "passed"
    except TimeoutException:
        return "timed out"
    except BaseException as e:
        return f"failed: {e}"


class TimeoutException(Exception):
    pass
