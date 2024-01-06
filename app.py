from flask import Flask, render_template, request
from openai import OpenAI
import ast
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


@app.route('/submit', methods=['POST'])
def submit():
    form_data = request.form.to_dict()
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

    list_metrics = list(zip(metrics, descriptions))
    system_prompt = f"""
    You are an idea validator that advises human*** evaluators by developing clear rationale and ratings for essential metrics. The metrics are weighted according to their importance.
    The metrics are provided in the following list (Each metric comes with a small description):
    {list_metrics}

    You will be given an idea in the form of problem/solution pairs (delimited with XML tags) in the following format:
    <problem> the problem  </problem>
    <solution> the solution to the stated problem </solution>

    Use the following step-by-step instructions to curate your answer:
    Step 1 – Check if the idea is sloppy, off-topic (i.e., not sustainability related), unsuitable, or vague (such as the over-generic content that prioritizes form over substance, offering generalities instead of specific details). You should helps concentrate human evaluators’ time and resources on concepts that are meticulously crafted, well-articulated, and hold tangible relevance. Flag each idea that could be included in this category as “Not interesting”.
    Step 2 – Evaluate the idea based on the given metrics. Give a score between 0 and 10 for each metric and also an explanation of the given score.
    Step 3 – Check if the idea is particularly exceptional and ambitious. These are ideas that are potentially revolutionary and that offer substantial returns but also carry a greater risk of failure. Emphasizes the novelty aspect of the idea and points to its potential for breakthroughs. Highlight ideas that might seem unconventional to experts in their respective domains–to prevent them from being overlooked by conservative human evaluators. Flag each idea that could be included in this category as “Moonshot”. Be strict in your judgment, only the most exceptional and revolutionary ideas can be flagged as “Moonshot”.

    Provide your answer in the form of a python dictionary. The following is a description of the different field of the json file that you should provide (don’t deviate from the format or add any fields). If no idea was provided then just say “Please provide your idea”:
    flags: list of flags.
    notes: a text providing rational behind the provided flags if any.
    ovl_eval : a small paragraph providing a high-level evaluation of the idea.
    eval_breakdown: a list of dictionaries each object represent a metrics and has 3 fields (metric: the metric name, score: the score you gave to the idea on this particular metric, explanation: the reasoning behind the score that you gave).

    """
    problem = form_data.get('problem', '')
    solution = form_data.get('solution', '')

    user_query = f"""
    <problem> {problem} </problem>
    <solution> {solution} </solution>
    """
    data = get_completion(user_query,system_prompt)
    data = ast.literal_eval(data[7:-3])
    return render_template('dashboard.html', data=data)

def calculate_score(problem, solution):
    # Add your score calculation logic here
    # For now, let's just return a static value
    return 42

def generate_review(problem, solution):
    # Add your review generation logic here
    # For now, let's just return a static review
    return "This idea looks promising!"

if __name__ == '__main__':
    app.run(debug=True)
