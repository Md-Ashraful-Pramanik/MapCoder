import os
from os.path import join, dirname

# HumanEval Dataset
HUMAN_DATA_DIR = join(
    "data",
    "HumanEval",
)

HUMAN_DATA_PATH = join(
    HUMAN_DATA_DIR,
    "HumanEval.jsonl"
)

HUMAN_WST_DATA_PATH = join(
    HUMAN_DATA_DIR,
    "HumanEvalWST.jsonl"
)

HUMAN_REFLXION_FILTERED_PATH = join(
    HUMAN_DATA_DIR,
    "humaneval-py.jsonl"
)

HUMAN_HARDSET_PATH = join(
    HUMAN_DATA_DIR,
    "humaneval-py_hardest50.jsonl"
)

HUMAN_ET_DATA_PATH = join(
    HUMAN_DATA_DIR,
    "HumanEvalET.jsonl"
)

HUMAN_SIMILAR_PROBLEMS_PATH = join(
    HUMAN_DATA_DIR,
    "similar_problems_solutions.jsonl"
)


# MBPP Dataset
MBPP_DATA_DIR = join(
    "data",
    "MBPPEval",
)

MBPP_DATA_PATH = join(
    MBPP_DATA_DIR,
    "MBPP-py.jsonl"
)

MBPP_ET_DATA_PATH = join(
    MBPP_DATA_DIR,
    "MBPP_ET.jsonl"
)

MBPP_SANITIZED_DATA_PATH = join(
    MBPP_DATA_DIR,
    "MBPP_SANITIZED.json"
)

MBPP_SIMILAR_PROBLEMS_PATH = join(
    MBPP_DATA_DIR,
    "similar_problems_solutions.jsonl"
)

# XCodeEval Dataset
XCODE_DATA_DIR = join(
    "data",
    "xCodeEval",
)

XCODE_VALIDATION_DATA_PATH = join(
    XCODE_DATA_DIR,
    "prog_syn_val.jsonl"
)

XCODE_TEST_DATA_PATH = join(
    XCODE_DATA_DIR,
    "prog_syn_test.jsonl"
)

XCODE_TRAIN_DATA_DIR_PATH = join(
    XCODE_DATA_DIR,
    "train"
)

XCODE_UNIT_TEST_PATH = join(
    XCODE_DATA_DIR,
    "unittest_db.json"
)

XCODE_PROBLEM_DESCRIPTION_PATH = join(
    XCODE_DATA_DIR,
    "problem_descriptions.jsonl"
)

XCODE_SIMILAR_SRC_UIDS_PATH = join(
    XCODE_DATA_DIR,
    "similar_src_uids.json"
)

XCODE_SIMILAR_PROBLEMS_PATH = join(
    XCODE_DATA_DIR,
    "similar_problems_solutions.json"
)

XCODE_PROBLEM_FILE_MAPPINGS_PATH = join(
    XCODE_DATA_DIR,
    "problem_file_mapping.json"
)


# Code Contest Dataset
CODE_CONTEST_DATA_DIR = join(
    "data",
    "CodeContest",
)

CODE_CONTEST_DATA_PATH = join(
    CODE_CONTEST_DATA_DIR,
    "Test.jsonl"
)


# APPS Dataset
APPS_DATA_DIR = join(
    "data",
    "APPS",
)

APPS_DATA_PATH = join(
    APPS_DATA_DIR,
    "selected150.jsonl"
)
