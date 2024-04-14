import pandas as pd
import cohere
import openai
from cohere.error import CohereAPIError
import time
import os
import anthropic


co = cohere.Client('API-KEY')

all_prompts = pd.read_csv("good deception - final prompts.csv")
openai.api_key = "API-KEY"
SCENARIO_PROMPTS_FILENAME = "good deception - final prompts.csv"
FOLLOWUP_PROMPTS_FILENAME = "follow_up_prompts.csv"

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)
class PromptsAnswers:

    def __init__(self):
        openai.api_key = "API_KEY"

    def query_model(self, model, message):
        try:
            if model == "cohere":
                response = co.chat(
                    chat_history=[],
                    message=message,
                )
                print(response)
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
                print(response)

            if model == "gpt-4":
                response = openai.ChatCompletion.create(
                    model="gpt-4-0613",
                    messages=[
                        {'role': 'system',
                         'content': 'Respond with a single number. Think it through carefully and vote precisely. '},
                        {'role': 'user', 'content': message}],
                )
                response = response["choices"][0]["message"]["content"]

            if model=="claude":
                response = client.messages.create(
                    model="claude-2.1",
                    max_tokens=1024,
                    messages=[
                        {"role": "user", "content": "Hello, world"}
                    ]
                )

        except CohereAPIError:
            time.sleep(30)
            response = self.query_model(model, message)
        return response

    def get_response(self, prompt, model):
        message = prompt + " Response must only be a single integer of the most preferred option."
        response = self.query_model(model, message)
        if "1" in response:
            chosen_option = 1
        elif "2" in response:
            chosen_option = 2
        elif "3" in response:
            chosen_option = 3
        else:
            return None

        return chosen_option


    def generate_conversation(self, model, n):
        all_prompts = pd.read_csv(SCENARIO_PROMPTS_FILENAME)
        followup_prompts = pd.read_csv(FOLLOWUP_PROMPTS_FILENAME)

        first_responses = {"1": 0, "2": 0, "3": 0}
        second_responses = {"1": 0, "2": 0, "3": 0}
        num_changed_responses = 0
        for i in range(n):
            prompt = all_prompts.iloc[i][0]
            first_chosen_option = self.get_response(prompt, model=model)
            print(i, "first_chosen_option", first_chosen_option)
            if first_chosen_option == 1:
                first_responses["1"] += 1
                followup_prompt = followup_prompts["Option 2"].iloc[i]
            elif first_chosen_option == 2:
                first_responses["2"] += 1
                followup_prompt = followup_prompts["Option 3"].iloc[i]
            elif first_chosen_option == 3:
                followup_prompt = followup_prompts["Option 1"].iloc[i]
                first_responses["3"] += 1
            else:
                "The first response is not correct, i.e. not one of 1, 2 or 3"
                pass

            second_chosen_option = self.get_response(followup_prompt, model=model)
            print(i, "second chosen option", second_chosen_option)
            if second_chosen_option == 1:
                second_responses["1"] += 1
            elif second_chosen_option == 2:
                second_responses["2"] += 1
            elif second_chosen_option == 3:
                second_responses["3"] += 1
            else:
                "The first response is not correct, i.e. not one of 1, 2 or 3"
                pass

            if first_chosen_option != second_chosen_option:
                num_changed_responses += 1

        print("first responses:", first_responses)
        print("second responses:", second_responses)
        print("num responses changed: ", num_changed_responses, " percentage: ", num_changed_responses*100/n)


answers_class = PromptsAnswers()
generated_responses = answers_class.generate_conversation(model="cohere", n=1)
# responses = pd.DataFrame(generated_responses, index=[0])
# responses.to_csv("responses_to_prompts.csv", index=False)
