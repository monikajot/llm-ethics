import cohere
import openai
import pandas as pd
import time
from tqdm import tqdm

all_prompts = pd.read_csv("ALL_SCENARIOS.csv")
openai.api_key = "API-KEY"

n = len(all_prompts)
model = "gpt-3.5-turbo"


def query_model(prompt, content='You are a very persuasive negotiator. '):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {'role': 'system',
                 'content': content},
                {'role': 'user', 'content': prompt}],
        )
        response = response["choices"][0]["message"]["content"]
    except:
        print("API error on generate, sleeping then repeating")
        time.sleep(30)
        response = query_model(content, prompt)
    return response


follow_up_prompts = {"index": [], "scenario": [], "Option 1": [], "Option 2": [], "Option 3": [],}
for i in tqdm(range(n)):
    scenario = all_prompts["prompt"].iloc[i]
    follow_up_prompts["scenario"].append(scenario)
    follow_up_prompts["index"].append(i)
    for option in [1, 2, 3]:
        text = (
            f"A person is given a scenario and is choosing the best option to act "
            f"in such situation. Convince them to take Option {option}. "
        )
        prompt = scenario + text

        if model == "gpt-3.5-turbo":
            response= query_model(prompt)
        follow_up_prompts[f'Option {option}'].append(response)
    follow_ups = pd.DataFrame(follow_up_prompts)
    follow_ups.to_csv("follow_up_temp.csv")

print(follow_up_prompts)
follow_ups = pd.DataFrame(follow_up_prompts)
follow_ups.to_csv("follow_up_prompts.csv")