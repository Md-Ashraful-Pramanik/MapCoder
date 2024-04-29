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


train_set = read_jsonl("./data/APPS/train.jsonl")
test_set = read_jsonl("./data/APPS/train.jsonl")

dataset = train_set + test_set

print(len(dataset))

dataset = pd.DataFrame(dataset)
# dataset.columns

print(dataset['difficulty'].unique())


# Filter problems from codeforces with atleast 10 input and output
filter_indices = [False] * len(dataset)
for i in range(len(dataset)):
    row = dataset.iloc[i]
    if "codeforces" in row['url'] and row['input_output'] and len(json.loads(row['input_output'])["inputs"]) > 5:
        filter_indices[i] = True

codeforces_dataset = dataset[filter_indices]

print(len(codeforces_dataset))

# Randomly choose 50 problems
codeforces_dataset_50 = codeforces_dataset.sample(n=min(50, len(codeforces_dataset)), random_state=1, replace=False)
print(len(codeforces_dataset_50))

codeforces_dataset_50.reset_index(drop=True, inplace=True)

# Filter interview problems with atleast 10 input and output
filter_indices = [False] * len(dataset)
for i in range(len(dataset)):
    row = dataset.iloc[i]
    if "interview" == row['difficulty'] and row['input_output'] and len(row['input_output']) < 2000 and len(json.loads(row['input_output'])["inputs"]) > 5:
        filter_indices[i] = True

interview_dataset = dataset[filter_indices]

print(len(interview_dataset))

# Randomly choose 50 problems
interview_dataset_50 = interview_dataset.sample(
    n=min(50, len(interview_dataset)), random_state=1, replace=False)
print(len(interview_dataset_50))

interview_dataset_50.reset_index(drop=True, inplace=True)


# Filter introductory problems with atleast 10 input and output
filter_indices = [False] * len(dataset)
for i in range(len(dataset)):
    row = dataset.iloc[i]
    if "introductory" == row['difficulty'] and len(row['input_output']) < 2000 and len(json.loads(row['input_output'])["inputs"]) > 5:
        filter_indices[i] = True

introductory_dataset = dataset[filter_indices]

print(len(introductory_dataset))

# Randomly choose 50 problems
introductory_dataset_50 = introductory_dataset.sample(
    n=min(50, len(introductory_dataset)), random_state=1, replace=False)
print(len(introductory_dataset_50))

introductory_dataset_50.reset_index(drop=True, inplace=True)

selected_df = pd.concat([introductory_dataset_50, interview_dataset_50, codeforces_dataset_50], ignore_index=True)


def get_test_cases(input, output):
    return {
        "input": "\n".join([str(x) for x in input]) if type(input) == list else input,
        "output": output if type(output) == list else [output]
    }


selected_datasets = []

for i in range(len(selected_df)):
    row = selected_df.iloc[i]
    test_cases = json.loads(row['input_output'])

    public_test_cases = list(
        map(get_test_cases, test_cases['inputs'][0:2], test_cases['outputs'][0:2]))
    test_cases = list(
        map(get_test_cases, test_cases['inputs'], test_cases['outputs']))

    test = {
        "name": str(row['id']),
        "description": str(row['question']),
        "difficulty": str(row['difficulty']),
        "id": int(row['id']),
        "sample_io": public_test_cases,
        "test_list": test_cases,
        "starter_code": str(row['starter_code']),
    }

    selected_datasets.append(test)


write_jsonl("./data/APPS/selected150.jsonl", selected_datasets)


