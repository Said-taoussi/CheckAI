from flask import Flask, render_template, request
from openai import OpenAI
import ast
import json
import numpy as np
import csv
import pandas as pd
from io import TextIOWrapper

key = "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"
client = OpenAI(api_key = key)


app = Flask(__name__)

def get_completion(user_query,system_prompt, model="gpt-3.5-turbo-1106"):
    messages = [{"role": "system", "content": system_prompt},{"role": "user", "content": user_query}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )
    return response.choices[0].message.content

@app.route('/')
def home():
    return render_template('index.html')

def prepare_metrics(form_data):
    metrics = []
    descriptions = []
    weights = []
    for key, value in form_data.items():
        if 'metric' in key:
            metrics.append(value)
        elif 'description' in key:
            descriptions.append(value)
        elif 'weight' in key:
            weights.append(value)
    
    return metrics, descriptions, weights
def check_idea(metrics, descriptions, problem, solution):
    list_metrics = list(zip(metrics, descriptions))
    system_prompt = f"""
    You are an idea validator that advises human evaluators by developing clear rationale and ratings for essential metrics. The metrics are provided in the following list (Each metric comes with a small description):
    {list_metrics}
    -------------------------------------
    You will be given an idea in the form of problem/solution pairs (delimited with XML tags) in the following format:
    <problem> the problem  </problem>
    <solution> the solution to the stated problem </solution>
    -------------------------------------
    Use the following step-by-step instructions to curate your answer:
    Step 1 – Check if the idea is sloppy, off-topic (i.e., not sustainability related), unsuitable, or vague (such as the over-generic content that prioritizes form over substance, offering generalities instead of specific details or undeveloped ideas that lack substance and details). You should help concentrate human evaluators’ time and resources on concepts that are meticulously crafted, well-articulated, and hold tangible relevance. Flag each idea that could be included in this category as “Not interesting”.
    Step 2 – Evaluate the idea based on the given metrics. Give a score between 0 and 20 for each metric and also an explanation of the given score. Be strict in your rating, don’t give a high point unless the idea really align with the metrics. AGAIN BE VERY STRICT AND DON'T GIVE FREE POINTS BECAUSE THIS WILL COST US A LOT OF MONEY. THINK OF IT AS EACH POINT IS A MILLION DOLLAR INVESTEMENT.
    Step 3 – Check if the idea is particularly exceptional and ambitious. These are ideas that are potentially revolutionary and that offer substantial returns but also carry a greater risk of failure. Emphasizes the novelty aspect of the idea and points to its potential for breakthroughs. Highlight ideas that might seem unconventional to experts in their respective domains–to prevent them from being overlooked by conservative human evaluators. Flag each idea that could be included in this category as “Moonshot”. Be strict in your judgment, only the most exceptional and revolutionary ideas can be flagged as “Moonshot”.
    -------------------------------------
    Provide your answer in the form of a python dictionary. The following is a description of the different field of the dictionary that you should provide (don’t deviate from the format or add any fields):
    flags: list of flags (Possible values: “Moonshot”, “Not interesting”), could be empty.
    ovl_eval : a small text providing a high-level evaluation of the idea, and also provide rational behind the provided flags if any.
    eval_breakdown: a list of python dictionaries, each one represent a metrics and has 3 fields (metric: the metric name, score: the score you gave to the idea on this particular metric, explanation: the reasoning behind the score that you gave)
    -------------------------------------
    IMPORTANT : The output should be a python dictionary only. It should be ready to be used in code using the “eval” function, don't add any prefixes or suffixes.
    -------------------------------------
    If no idea was provided then just say “Please provide your idea”.
    """

    user_query = f"""
    <problem> {problem} </problem>
    <solution> {solution} </solution>
    """
    data = get_completion(user_query,system_prompt)
    try :
        data = eval(data)
    except :
        data = eval(data[9:-3])
    return data

@app.route('/submit', methods=['POST'])
def submit():
    form_data = request.form.to_dict()
    problem = form_data.get('problem', '')
    solution = form_data.get('solution', '')
    metrics, descriptions, weights = prepare_metrics(form_data)

    # data = check_idea(metrics, descriptions, problem, solution)
    # print(data)
    # score = calculate_score(data, weights)
    # data["score_total"] = score
    return render_template('dashboard.html', data={"ovl_eval": "sdf","score_total":21, "eval_breakdown":[], "flags":[]})#data)

def calculate_score(data, weights):
    metric_data = data.get('eval_breakdown', [])
    score_list = []
    for metric in metric_data :
        score_list.append(metric["score"])
    weights_np = np.array(weights, dtype=np.float64)/20
    score_np = np.array(score_list, dtype=np.float64)
    try :
        score = np.sum(weights_np * score_np)
    except :
        score = 0
    return round(score, 2)

@app.route('/table', methods=['POST'])
def table():
    form_data = request.form.to_dict()
    metrics, descriptions, weights = prepare_metrics(form_data)
    # Check if the 'csvFile' file is present in the request
    if 'csvFile' not in request.files:
        return "No file part"
    
    file = request.files['csvFile']

    # Check if the file is empty
    if file.filename == '':
        return "No selected file"

    # Check if the file is a CSV file
    if file and file.filename.endswith('.csv'):
        # Rewind the file to the beginning
        file.seek(0)

        # Use TextIOWrapper to handle the decoding of the file
        csv_file = TextIOWrapper(file, encoding='latin-1')

        df = pd.read_csv(csv_file)[:2]
        flagss = []
        scores = []
        datas = []
        for index, row in df.iterrows():
            problem = row[1]
            solution = row[2]
            data = check_idea(metrics, descriptions, problem, solution)
            score = calculate_score(data, weights)
            flags = data["flags"][0] if data["flags"] else "No flags"
            scores.append(score)
            flagss.append(flags)
            datas.append(data)
        df["flags"] = flagss
        df["score"] = scores
        df["data"] = datas
        df = df.sort_values(by='score', ascending=False)
        # You can now process the data as needed and pass it to the template
        return render_template('table.html', df=df)

    return "Invalid file format"

@app.route('/get_details/<identifier>')
def get_details(identifier):
    # Perform any necessary logic based on the identifier
    # For now, let's return a simple JSON response
    identifiers = identifier.split('$')
    print(identifiers)
    score = identifiers[1]
    print(identifiers[0])
    data = eval(identifiers[0])
    data["score_total"] = score
    return render_template('dashboard.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
