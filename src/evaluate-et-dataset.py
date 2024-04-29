from utils.jsonl import read_jsonl, write_jsonl
from evaluations.func_evaluate import evaluate_io_et
import os


def generate_et_dataset(
        NORMAL_RESULTS_PATH,
        ET_RESULTS_PATH,
        ET_DATA_PATH=".\\data\\HumanEval\\HumanEvalET.jsonl"
):
    dataset = read_jsonl(ET_DATA_PATH)
    data_dict = {}
    for item in dataset:
        data_dict[item["task_id"]] = {"et_item": item}

    results = read_jsonl(NORMAL_RESULTS_PATH)
    for result in results:
        data_dict[result["task_id"]]["result"] = result

    correct_count = 0
    et_results = []
    for key, value in data_dict.items():
        item = value["et_item"]
        result = value["result"]
        generated_code = result["source_codes"][0] if "source_codes" in result else result["solution"]

        passed = evaluate_io_et(
            item['test_case_list'],
            generated_code,
            prompt=item["prompt"]
        )

        if passed:
            result["is_solved"] = True
            correct_count += 1
        else:
            result["is_solved"] = False

        et_results.append(result)
        print(
            f"Accuracy: {correct_count}/{len(et_results)} = {correct_count/len(et_results):.2f}")
    # write_jsonl(ET_RESULTS_PATH, et_results)

    et_results = sorted(
        et_results,
        key=lambda x: int(x["task_id"].split('/')[-1])
    )

    write_jsonl(ET_RESULTS_PATH, et_results)
    print(
        f"Accuracy: {correct_count}/{len(et_results)} = {correct_count/len(et_results):.2f}")


def generate_et_dataset_mbpp(
        NORMAL_RESULTS_PATH,
        ET_RESULTS_PATH,
        ET_DATA_PATH=".\\data\\MBPPEval\\MBPP_ET.jsonl"
):
    dataset = read_jsonl(ET_DATA_PATH)
    data_dict = {}
    for item in dataset:
        data_dict[item["task_id"]] = {"et_item": item}

    results = read_jsonl(NORMAL_RESULTS_PATH)
    for result in results:
        task_id = int(result["name"].split("_")[1])
        data_dict[task_id]["result"] = result

    correct_count = 0
    et_results = []
    for key, value in data_dict.items():
        item = value["et_item"]
        result = value.get("result", None)
        if result is None:
            continue

        generated_code = result["source_codes"][0] if "source_codes" in result else result["solution"]

        passed = evaluate_io_et(
            item['test_list'],
            generated_code
        )

        if passed:
            result["is_solved"] = True
            correct_count += 1
        else:
            result["is_solved"] = False

        et_results.append(result)
        print(
            f"Accuracy: {correct_count}/{len(et_results)} = {correct_count/len(et_results):.2f}")
    # write_jsonl(ET_RESULTS_PATH, et_results)

    et_results = sorted(
        et_results,
        key=lambda x: int(x["name"].split("_")[1])
    )

    write_jsonl(ET_RESULTS_PATH, et_results)
    print(
        f"Accuracy: {correct_count}/{len(et_results)} = {correct_count/len(et_results):.2f}")


