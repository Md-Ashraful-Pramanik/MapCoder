<!-- 
# Official MapCoder Repository
- [Visit our webpage](https://md-ashraful-pramanik.github.io/mapcoder.github.io/)
- Visit our paper for more details -->

# MapCoder: Multi-Agent Code Generation for Competitive Problem Solving

<p align="center">
• 🐱 <a href="https://github.com/Md-Ashraful-Pramanik/MapCoder" target="_blank">Code</a> 
• 📃 <a href="https://arxiv.org/abs/2405.11403" target="_blank">Paper</a>
• 🌐 <a href="https://md-ashraful-pramanik.github.io/mapcoder.github.io/" target="_blank">Website</a>
</p>

## News
- 🎉 Our paper is got accepted on [ACL 2024](https://2024.aclweb.org/).
- All our codebase is open-sourced with MIT License. 


## Abstract
Code synthesis, which requires a deep understanding of complex natural language (NL) problem descriptions, generation of code instructions for complex algorithms and data structures, and the successful execution of comprehensive unit tests, presents a significant challenge. Thus, while large language models (LLMs) demonstrate impressive proficiency in natural language processing (NLP), their performance in code generation tasks remains limited. In this paper, we introduce a new approach to code generation tasks leveraging the multi-agent prompting that uniquely replicates the full cycle of program synthesis as observed in human developers. Our framework, MapCoder, consists of four LLM agents specifically designed to emulate the stages of this cycle: recalling relevant examples, planning, code generation, and debugging. After conducting thorough experiments, with multiple LLMs ablations and analyses across eight challenging competitive problem-solving and program synthesis benchmarks—MapCoder showcases remarkable code generation capabilities, achieving their new state-of-the-art (pass@1)
results—(HumanEval 93.9%, MBPP 83.1%, APPS 22.0%, CodeContests 28.5%, and xCodeEval 45.3%). Moreover, our method consistently delivers superior performance across various programming languages and varying problem difficulties. 


## MapCoder Overview
![MapCoder Overview](./images/MapCoder-Overview.png)
Our goal is to develop a multi-agent code generation approach for competitive problem-solving. In order to do so, our framework, MapCoder, replicates the human programming cycle through four LLM agents - retrieval, plan, code, and debug. We devise a pipeline sequence for MapCoder, intelligently cascading the agents in a structured way and enhancing each agent's capability by augmenting in-context learning signals from previous agents in the pipeline. However, not all the agent responses/outputs are equally useful. Therefore, additionally, MapCoder features an adaptive agent traversal schema to interact among corresponding agents dynamically, iteratively enhancing the generated code by, for example, fixing bugs, while maximizing the usage of the LLM agents. Here, we first discuss the agents (as per the pipeline), their prompts, and interactions, followed by the dynamic agent traversal protocol in MapCoder towards code generation for competitive problem-solving.

### » Retrieval Agent
Our first agent, the Retrieval Agent, recalls past relevant problem-solving instances, akin to human memory. It finds k (user-defined) similar problems without manual crafting or external retrieval models. Instead, we leverage the LLM agent itself, instructing it to generate such problems.
### » Planning Agent
The second agent, the Planning Agent, aims to create a step-by-step plan for the original problem. Our Planning Agent uses examples and their plans obtained from the retrieval agent to generate plans for the original problem. A straightforward approach would be to utilize all examples collectively to generate a single target plan. However, not all retrieved examples hold equal utility. Concatenating examples in a random order may compromise the LLM's ability to generate accurate planning.
### » Coding Agent
Next is the Coding Agent. It takes the problem description, and a plan from the Planning Agent as input and translates the corresponding planning into code to solve the problem. During the traversing of agents, Coding Agent takes the original problem and one particular plan from the Planning Agent, generates the code, and test on sample I/O. If the initial code fails, the agent transfers it to the next agent for debugging. Otherwise, predicts that as the final solution.
### » Debugging Agent
Finally, the Debugging Agent utilizes sample I/O from the problem description to rectify bugs in the generated code. Similar to humans cross-checking their plan while fixing bugs, our pipeline supplements the Debugging Agent with plans from the Planning Agent. This plan-derived debugging significantly enhances bug fixing in MapCoder, underscoring the pivotal roles played by both the Debugging Agent and the Planning Agent in the generation process.


## Problem Solving Example
![MapCoder Example Problem Solving](./images/example-problem.png)

## Results of MapCoder on Eight Benchmarks
| LLM | Approach | HumanEval  | HumanEval-ET  | EvalPlus | MBPP  | MBPP-ET  | APPS  | xCodeEval  | CodeContest |
|-----------------|---------|--------------------|-----------------|-----------------|------------------------|-----------------|-----------------|-----------------|-----------------|
| ChatGPT | Direct   | 48.1% | 37.2% | 66.5% | 49.8% | 37.7% | 8.0%  | 17.9% | 5.5%   |
| | CoT | 68.9% | 55.5% | 65.2% | 54.5% | 39.6% | 7.3%  | 23.6% | 6.1%   |
| | Self-Planning | 60.3% | 46.2% | - | 55.7% | 41.9% | 9.3%  | 18.9% | 6.1%   |
| | Analogical | 63.4% | 50.6% | 59.1% | 70.5% | 46.1% | 6.7%  | 15.1% | 7.3%   |
| | Reflexion | 67.1% | 49.4% | 62.2% | 73.0% | 47.4% | - | - | - |
| | Self-collaboration | 74.4% | 56.1% | - | 68.2% | 49.5% | - | - | - |
| | MapCoder | 80.5% <br> ↑ 67.3% | 70.1% <br> ↑ 88.5% | 71.3% <br> ↑ 7.3% | 78.3% <br> ↑ 57.3% | 54.4% <br> ↑ 44.3% | 11.3% <br> ↑ 41.3% | 27.4% <br> ↑ 52.6% | 12.7% <br> ↑ 132.8%  |
| GPT4 | Direct   | 80.1% | 73.8% | 81.7% | 81.1% | 54.7% | 12.7% | 32.1% | 12.1%  |
| | CoT | 89.0% | 61.6% | - | 82.4% | 56.2% | 11.3% | 36.8% | 5.5%   |
| | Self-Planning | 85.4% | 62.2% | - | 75.8% | 50.4% | 14.7% | 34.0% | 10.9%  |
| | Analogical | 66.5% | 48.8% | 62.2% | 58.4% | 40.3% | 12.0% | 26.4% | 10.9%  |
| | Reflexion | 91.0% | 78.7% | 81.7% | 78.3% | 51.9% | - | - | - |
| | MapCoder | 93.9% <br> ↑ 17.2% | 82.9% <br> ↑ 12.4% | 83.5% <br> ↑ 2.2% | 83.1% <br> ↑ 2.5%  | 57.7% <br> ↑ 5.5%  | 22.0% <br> ↑ 73.7% | 45.3% <br> ↑ 41.2% | 28.5% <br> ↑ 135.1% |



## Running our project
1. Clone our project
```
git clone https://github.com/Md-Ashraful-Pramanik/MapCoder && cd MapCoder
```

2. Create a new conda or python virtual environment and run the following command
```
pip install -r requirements.txt
```

3. Set up the .env file by seeing the example.

4. Run the following command to see the options of running this projects
```
python src/main.py --help
```

5. Finally run this project. An example is given below:
```
python src/main.py --model ChatGPT --dataset HumanEval --strategy MapCoder
```

6. To run this projects with competitive datasets you need to setup the [ExecEval](https://github.com/ntunlp/ExecEval) for docker execution. Please visit this [link](https://github.com/ntunlp/ExecEval) to setup a docker container and run it using 5000 port. Change the line 50 of the file `src\evaluations\api_comm.py` for different setup. 


## Citation
```
@article{islam2024mapcoder,
  title={MapCoder: Multi-Agent Code Generation for Competitive Problem Solving},
  author={Islam, Md Ashraful and Ali, Mohammed Eunus and Parvez, Md Rizwan},
  journal={arXiv preprint arXiv:2405.11403},
  year={2024}
}
```
