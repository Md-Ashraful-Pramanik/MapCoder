# Using this python file we have converted the code contest dataset to the format of the xCodeEval dataset.

import pandas as pd
import json


def read_jsonl(filename):
    """Reads a jsonl file and yields each line as a dictionary"""
    lines = []
    # i = 0
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            lines.append(json.loads(line))
            # i += 1
            # print(i)
    return lines

# Write a python list of dictionaries into a jsonl file


def write_jsonl(filename, lines):
    """Writes a python list of dictionaries into a jsonl file"""
    with open(filename, "w", encoding="utf-8") as file:
        for line in lines:
            file.write(json.dumps(line) + "\n")


df = pd.read_parquet("./data/CodeContest/validation.parquet", engine='pyarrow')
df = df[['name', 'cf_contest_id', 'cf_tags', 'difficulty',
         'description', 'public_tests', 'private_tests', 'generated_tests']]


def get_test_cases(input, output):
    return {
        "input": str(input),
        "output": [str(output)]
    }


test_datasets = []

for i in range(len(df)):
    row = df.iloc[i]

    public_test_cases = list(
        map(get_test_cases, row['public_tests']['input'], row['public_tests']['output']))
    test_cases = []
    test_cases.extend(list(map(
        get_test_cases, row['private_tests']['input'], row['private_tests']['output'])))
    test_cases.extend(list(map(
        get_test_cases, row['generated_tests']['input'], row['generated_tests']['output'])))

    test = {
        "name": str(row['name']),
        "description": str(row['description']),
        "tags": list(row['cf_tags']),
        "difficulty": int(row['difficulty']),
        "id": int(row['cf_contest_id']),
        "sample_io": public_test_cases,
        "test_list": test_cases
    }

    test_datasets.append(test)


write_jsonl("./data/CodeContest/Val.jsonl", test_datasets)
