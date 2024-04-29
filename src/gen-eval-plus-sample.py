from utils.jsonl import read_jsonl, write_jsonl
from evaluations.func_evaluate import evaluate_io_et
import os


def generate_ep_dataset(
        NORMAL_RESULTS_PATH,
        EP_SAMPLES_PATH,
):
    samples = []
    results = read_jsonl(NORMAL_RESULTS_PATH)
    for result in results:
        completion = result["source_codes"][-1]

        if "from typing import *" not in completion:
            completion = "from typing import *\n" + completion

        samples.append(
            {
                "task_id": result["task_id"],
                "solution": completion,
                # "completion": result["solution"]
            }
        )

    write_jsonl(EP_SAMPLES_PATH, samples)


generate_ep_dataset(
    "./final-results/GPT4/HumanEval/GPT4-Turbo-Analogical-Human-Python3-0-1.jsonl",
    "./final-results/GPT4/HumanEvalPlus/GPT4-Turbo-Analogical-Human-Python3-0-1.jsonl"
)

mbpp_not_included_set = set([
    "Mbpp/304", "Mbpp/393", "Mbpp/399", "Mbpp/401", "Mbpp/408",
    "Mbpp/411", "Mbpp/417", "Mbpp/434", "Mbpp/443", "Mbpp/444",
    "Mbpp/452", "Mbpp/464", "Mbpp/584", "Mbpp/617", "Mbpp/625",
    "Mbpp/627", "Mbpp/738", "Mbpp/747", "Mbpp/756", "Mbpp/776",
    "Mbpp/802", "Mbpp/228", "Mbpp/291"
])

def generate_ep_dataset_mbpp(
        NORMAL_RESULTS_PATH,
        EP_SAMPLES_PATH,
):
    samples = []
    results = read_jsonl(NORMAL_RESULTS_PATH)
    for result in results:
        completion = result["source_codes"][-1]
        task_id = "Mbpp/" + result["name"].split("_")[1]
        if task_id in mbpp_not_included_set:
            continue

        if "from typing import *" not in completion:
            completion = "from typing import *\n" + completion

        samples.append(
            {
                "task_id": task_id,
                "solution": completion
            }
        )

    write_jsonl(EP_SAMPLES_PATH, samples)


# generate_ep_dataset_mbpp(
#     "./final-results/GPT4/MBPP/GPT4-Turbo-MapCoder-3-5-MBPP-Python3-0-1.jsonl",
#     "./final-results/GPT4/MBPPPlus/GPT4-Turbo-MapCoder-3-5-MBPP-Python3-0-1.jsonl"
# )

# generate_ep_dataset_mbpp(
#     "./final-results/ChatGPT/MBPP/ChatGPT-MapCoder-3-5-MBPP-Python3-0-1.jsonl",
#     "./final-results/ChatGPT/MBPPPlus/ChatGPT-MapCoder-3-5-MBPP-Python3-0-1.jsonl"
# )

# results_dir = "./final-results"
# for model in os.listdir(results_dir):
#     if model == "Gemini":
#         continue
#     human_dir = os.path.join(results_dir, model, "HumanEval")
#     human_et_dir = os.path.join(results_dir, model, "HumanEvalET")
#     mbpp_dir = os.path.join(results_dir, model, "MBPP")
#     mbpp_et_dir = os.path.join(results_dir, model, "MBPPET")

#     if os.path.exists(human_dir):
#         for file in os.listdir(human_dir):
#             if file.endswith(".jsonl"):
#                 if os.path.exists(os.path.join(human_et_dir, file)):
#                     continue
#                 print(file)
#                 generate_et_dataset(
#                     os.path.join(human_dir, file),
#                     os.path.join(human_et_dir, file)
#                 )
#     if os.path.exists(mbpp_dir):
#         for file in os.listdir(mbpp_dir):
#             if file.endswith(".jsonl"):
#                 if os.path.exists(os.path.join(mbpp_et_dir, file)):
#                     continue
#                 print(file)
#                 generate_et_dataset_mbpp(
#                     os.path.join(mbpp_dir, file),
#                     os.path.join(mbpp_et_dir, file)
#                 )
