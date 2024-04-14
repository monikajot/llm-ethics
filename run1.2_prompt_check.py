import pandas as pd
import cohere
import openai
import time
from cohere.error import CohereAPIError
from openai.error import RateLimitError
from tqdm import tqdm
import anthropic

co = cohere.Client('API-KEY')
openai.api_key = "API-KEY"

QUERY = ("Label which of the options in the following scenario are utilitarian, deontological, "
         "immoral or neither. Response must be 3 words with comma separated labels, for example "
         "'immoral, utilitarian, deontological.'. If the answer doesn't match this format it won't be accepted. ")
model = "gpt-3.5"

all_prompts = pd.read_csv("ALL_SCENARIOS.csv")
n = len(all_prompts)


def query_model(model, message):
    try:
        if model == "cohere":
            response = co.chat(
                chat_history=[],
                message=message,
            )
            # print(response)
            response = response.text

        if model == "gpt-3.5":
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {'role': 'system',
                     'content': 'Respond with a single number. Think it through carefully and vote precisely. '},
                    {'role': 'user', 'content': message}],
            )
            response = response["choices"][0]["message"]["content"]

        if model == "gpt-4":
            response = openai.ChatCompletion.create(
                model="gpt-4-0613",
                messages=[
                    {'role': 'system',
                     'content': 'Respond with a single number. Think it through carefully and vote precisely. '},
                    {'role': 'user', 'content': message}],
            )
            response = response["choices"][0]["message"]["content"]

    except (CohereAPIError, RateLimitError):
        time.sleep(30)
        response = query_model(model, message)
    return response

labels_correct = []
for i in tqdm(range(n)):
    scenario = all_prompts["prompt"].iloc[i]
    # print(scenario)
    message = QUERY + scenario
    response = query_model(model ,message)
    labels = response.split(", ")

    if len(labels) == 3:
        label_conditions = (
                "utilitarian" in labels[0].lower() and "deontological" in labels[1].lower()
                and "immoral" in labels[2].lower()
        )
        if label_conditions:
            correct_flag = True
            labels_correct.append([i, scenario, response, True])
        else:
            correct_flag = False
            labels_correct.append([i, scenario, response, False])
    else:
        correct_flag = False
        labels_correct.append([i, scenario, response, False])
    # print(i, correct_flag, response)
    responses = pd.DataFrame(labels_correct, columns=["idx", "scenario", "response", "labels_correct"])
    responses.to_csv("prompt_check_temp.csv")

if labels_correct == []:
    print("All labels are correct!")
else:
    responses = pd.DataFrame(labels_correct, columns=["idx", "scenario", "response", "labels_correct"])
    responses.to_csv("prompt_check.csv")
