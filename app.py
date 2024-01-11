from flask import Flask, render_template, request, redirect, url_for, session
from openai import OpenAI
import ast
import json
import numpy as np
import csv
import pandas as pd
from io import TextIOWrapper
import io
from flask_caching import Cache
import time
from itertools import repeat
import concurrent.futures
import os
from dotenv import load_dotenv


load_dotenv()

key = os.environ.get("API_KEY")
client = OpenAI(api_key = key)

app = Flask(__name__)
cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)

def get_completion(user_query,system_prompt, model="gpt-3.5-turbo-1106"):
    messages = [{"role": "system", "content": system_prompt},{"role": "user", "content": user_query}]
    response = client.chat.completions.create(
        response_format={ "type": "json_object" },
        model=model,
        messages=messages,
    )

    return response.choices[0].message.content

@app.route('/')
def home():
    cache.clear()
    return render_template('home.html')

@app.route('/ValidateOne')
def validate_one():
    # Add logic for the ValidateOne page if needed
    return render_template('validate_one.html')

@app.route('/ValidateMultiple')
def validate_multiple():
    # Add logic for the ValidateMultiple page if needed
    return render_template('validate_multiple.html')


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

You will be given an idea in the form of problem/solution pairs (delimited with XML tags).

Use the following step-by-step instructions to curate your answer:
Step 1 – rewrite the solution in a neutral way. Remove any exaggeration words such as “revolutionary”, “cutting edge”. Use this new version of the solution as the basis of your further analysis.
Step 2 – Check if the idea is sloppy, off-topic (i.e., not sustainability related), unsuitable, or vague (such as the over-generic content that prioritizes form over substance, offering generalities instead of specific details or undeveloped ideas that lack substance and details). Flag each idea that could be included in this category as “Not interesting”.
Step 3 – Evaluate the idea based on the given metrics. Give a score between 0 and 20 for each metric and also an explanation of the given score. Be strict in your rating, don’t give a high point unless the idea really align with the metrics.
Step 4 – Check if the idea is particularly exceptional and ambitious. These are ideas that offer substantial returns but also carry a greater risk of failure. Emphasizes the novelty aspect of the idea and points to its potential for breakthroughs. Flag each idea that could be included in this category as “Moonshot”. Be strict in your judgment, only the most exceptional and revolutionary ideas can be flagged as “Moonshot”. Don’t get fooled by selling language or the use of fancy words such as “revolutionary” and “cutting edge”, THIS IS THE WORST MISTAKE YOU COULD MAKE. Compare the original solution to the neutral solution that you have written.

Provide your answer in the form of a json. The following is a description of the different field of the json that you should provide (don’t deviate from the format or add any fields):
Neutral_solution : the new version of the solution that you have rewritten to eliminate over-generic content that prioritizes form over substance and the use of exaggeration and selling language.
flags: list of flags (Possible values: “Moonshot”, “Not interesting”), could be empty.
ovl_eval : a small text providing a high-level evaluation of the idea, and also provide rational behind the provided flags if any. This field should never be empty.
eval_breakdown: a list of json objects, each one represent a metrics and has 3 fields (metric: the metric name, score: the score you gave to the idea on this particular metric, explanation: the reasoning behind the score that you gave, even if the score is 0, you still have to provide an explanation), this field should never be empty.
    """

    user_query = f"""
    <problem> {problem} </problem>
    <solution> {solution} </solution>
    """
    data = get_completion(user_query,system_prompt)
    data = process_data(data)
    return data

def process_data(data):
    try:
        data = eval(data)
    except:
        try:
            data = eval(data[9:-3])
        except:
            data = {}
    return data


@app.route('/submit', methods=['POST'])
def submit():
    form_data = request.form.to_dict()
    problem = form_data.get('problem', '')
    solution = form_data.get('solution', '')
    metrics, descriptions, weights = prepare_metrics(form_data)

    data = check_idea(metrics, descriptions, problem, solution)
    #print(data)
    score = calculate_score(data, weights)
    data["score_total"] = score
    flags = data.get("flags", [])[0] if data.get("flags", []) else "No flags"
    data["flags"] = flags
    data["problem"] = problem
    data["solution"] = solution
    return render_template('dashboard.html', data=data, source='submit')

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

def process_row(row, metrics, descriptions, weights):
    problem = row[1]
    solution = row[2]
    data = check_idea(metrics, descriptions, problem, solution)
    score = calculate_score(data, weights)
    flags = data.get("flags", [])[0] if data.get("flags", []) else "No flags"
    return score, flags, data

@app.route('/table', methods=['GET', 'POST'])
@cache.cached(timeout=3600)  # Cache the result for 10 minutes
def table():
    if request.method == 'POST':
        form_data = request.form.to_dict()
        metrics, descriptions, weights = prepare_metrics(form_data)

        # Check if the 'csvFile' file is present in the request
        if 'csvFile' in request.files:
            file = request.files['csvFile']

            # Seek to the beginning of the file before reading
            file.seek(0)
            file_content = file.read()

        # Use TextIOWrapper to handle the decoding of the file content
        csv_file = TextIOWrapper(io.BytesIO(file_content), encoding='latin-1')

        df = pd.read_csv(csv_file)
        flagss = []
        scores = []
        datas = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Pass metrics, descriptions, and weights as arguments
            results = list(executor.map(process_row, df.itertuples(index=False), repeat(metrics), repeat(descriptions), repeat(weights)))
        i = 0
        for result in results:
            score, flags, data = result
            scores.append(score)
            flagss.append(flags)
            data["problem"] = df.iloc[i, 1]
            data["solution"] = df.iloc[i, 2]
            datas.append(data)
            i += 1
        df["flags"] = flagss
        df["score"] = scores
        df["data"] = datas
        df = df.sort_values(by='score', ascending=False)

        df_json = df.to_json(orient='split')
        cache.set('df', df_json)
        # You can now process the data as needed and pass it to the template
        return render_template('table.html', df=df)
    else:
        df_json = cache.get('df')
        if df_json is not None:
            df = pd.read_json(df_json, orient='split')
        else:
            df = pd.DataFrame()  # Handle the case where the cache is empty

        return render_template('table.html', df=df)
        
@app.route('/get_details/<identifier>')
def get_details(identifier):
    # Perform any necessary logic based on the identifier
    # For now, let's return a simple JSON response
    identifiers = identifier.split('$')
    score = identifiers[1]
    data = eval(identifiers[0])
    flags = data.get("flags", [])[0] if data.get("flags", []) else "No flags"
    data["flags"] = flags
    data["score_total"] = score
    return render_template('dashboard.html', data=data, source='table')

@app.route('/go_back/<source>')
def go_back(source):
    print(source)
    if source == 'table':
        return redirect(url_for('table'))
    elif source == 'submit':
        return redirect(url_for('home'))
    # Handle other cases as needed
    else:
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(debug=False, host="0.0.0.0")