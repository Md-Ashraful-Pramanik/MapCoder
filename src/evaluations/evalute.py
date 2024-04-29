import json
import os
import numpy as np
import tqdm
from yaml import safe_load
from typing import List

from .api_comm import APICommunication
from .exec_outcome import ExecOutcome
from constants.lang_mappings import LANGUAGE_MAPPING

limits_by_lang_cfg_file = "./src/evaluations/limits_by_lang.yaml"

assert os.path.exists(
    limits_by_lang_cfg_file), "Need resource limit defaults for all runtimes, provide the path to default 'limits_by_lang.yaml' or to the modified one."

with open(limits_by_lang_cfg_file) as limit_cfg_rp:
    limits_by_lang = safe_load(limit_cfg_rp)

unittest_file = "./data/xCodeEval/unittest_db.json"
assert os.path.exists(unittest_file), "Unittest file not found."

with open(unittest_file) as ut_rp:
    unittest_db = json.load(ut_rp)


api_comm = APICommunication()


def xcode_evaluate(
    generated_code: str,
    src_uid: str,
    lang: str
):

    assert src_uid in unittest_db, "Can not find the task id or source id"

    assert lang in LANGUAGE_MAPPING, f"language must be inside the supported language list: {LANGUAGE_MAPPING.keys()}"

    results, _, _ = api_comm.execute_code(
        language=LANGUAGE_MAPPING[lang],
        source_code=generated_code,
        unittests=unittest_db[src_uid],
        limits=limits_by_lang[LANGUAGE_MAPPING[lang]],
        task_id=src_uid,
    )

    if results == "error":
        return False

    passed = True
    for result in results:
        if result['exec_outcome'] != ExecOutcome.PASSED.value:
            passed = False
            break

    return passed


def xcode_execute_internal_test(
    generated_code: str,
    tests: List[dict],
    src_uid: str,
    lang: str
):
    results, _, _ = api_comm.execute_code(
        language=LANGUAGE_MAPPING[lang],
        source_code=generated_code,
        unittests=tests,
        limits=limits_by_lang[LANGUAGE_MAPPING[lang]],
        task_id=src_uid,
        stop_on_first_fail=False
    )

    passed = True
    passed_feedback = []
    failed_feedback = []

    idx = 0
    try:
        for idx, result in enumerate(results):
            if result['exec_outcome'] == ExecOutcome.PASSED.value:
                passed_feedback.append(tests[idx])
            if result['exec_outcome'] != ExecOutcome.PASSED.value:
                failed_feedback.append(tests[idx])
                passed = False
    except:
        passed = False
        failed_feedback.extend(tests[idx:])

    feedback = f'Tested passed: \n{json.dumps(passed_feedback)}\n\nTests failed: \n{json.dumps(failed_feedback)}'

    return passed, feedback


def contest_evaluate(
    generated_code: str,
    lang: str,
    id: int,
    tests: List[dict],
):
    assert lang in LANGUAGE_MAPPING, f"language must be inside the supported language list: {LANGUAGE_MAPPING.keys()}"

    results, _, _ = api_comm.execute_code(
        language=LANGUAGE_MAPPING[lang],
        source_code=generated_code,
        unittests=tests,
        limits=limits_by_lang[LANGUAGE_MAPPING[lang]],
        task_id=id,
    )

    if results == "error":
        return False

    passed = True
    for result in results:
        if result['exec_outcome'] != ExecOutcome.PASSED.value:
            passed = False
            break

    return passed


def contest_evaluate_public_tests(
    generated_code: str,
    lang: str,
    id: int,
    tests: List[dict],
):
    results, _, _ = api_comm.execute_code(
        language=LANGUAGE_MAPPING[lang],
        source_code=generated_code,
        unittests=tests,
        limits=limits_by_lang[LANGUAGE_MAPPING[lang]],
        task_id=id,
        stop_on_first_fail=False
    )

    passed = True
    passed_feedback = []
    failed_feedback = []

    idx = 0
    try:
        for idx, result in enumerate(results):
            output = str(result['result'])
            if len(output) > 500:
                output = output[:500] + "..."
            test_case = f"Input:\n{tests[idx]['input']}\nExpected Output:\n{tests[idx]['output'][0]}\nYour Output:\n{output}\n"
            if result['exec_outcome'] == ExecOutcome.PASSED.value:
                passed_feedback.append(test_case)
            if result['exec_outcome'] != ExecOutcome.PASSED.value:
                failed_feedback.append(test_case)
                passed = False
    except:
        passed = False
        test_cases = []
        for i in range(idx, len(tests)):
            test_case = f"Input:\n{tests[i]['input']}\nExpected Output:\n{tests[i]['output'][0]}\n"
            test_cases.append(test_case)
        
        failed_feedback.extend(test_cases)

    passed_feedback = '\n'.join(passed_feedback) if len(passed_feedback) > 0 else "No test cases passed."
    failed_feedback = '\n'.join(failed_feedback)
    feedback = f'## Tested passed:\n{passed_feedback}\n\n## Tests failed:\n{failed_feedback}'

    return passed, feedback
