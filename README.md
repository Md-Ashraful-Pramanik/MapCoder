# Official MapCoder Repository
[Visit our webpage](https://md-ashraful-pramanik.github.io/mapcoder.github.io/)
Visit our paper for more details

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
