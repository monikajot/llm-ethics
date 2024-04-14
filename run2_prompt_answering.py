import pandas as pd
from cohere.error import CohereAPIError
import time
import cohere
import openai
import os

co = cohere.Client('API-KEY')

all_prompts = pd.read_csv("good deception - final prompts.csv")
openai.api_key = "API-KEY"

class PromptsAnswers:

    def __init__(self):
        self.responses = {"1": 0, "2": 0, "3": 0}

    def get_responses(self, prompts=all_prompts, n=100, model="gpt-3.5-turbo"):

        for i in range(n):
            try:
                message = prompts.iloc[i][0] + " Response must only be a single integer of the most preferred option."
                if model== "cohere":
                    response = co.chat(
                        chat_history=[],
                        message=message,
                        # perform web search before answering the question. You can also use your own custom connector.
                        connectors=[]
                    )
                    response = response.text

                    print(i, response.text)
                if model == "gpt-3.5-turbo":
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {'role': 'system', 'content': 'Respond with a single number. Think it through carefully and vote precisely. '},
                            {'role': 'user', 'content': message}],
                    )
                    response = response["choices"][0]["message"]["content"]
                    print(response)
                if "1" in response:
                    self.responses["1"] += 1
                elif "2" in response:
                    self.responses["2"] += 1
                elif "3" in response:
                    self.responses["3"] += 1

            except CohereAPIError:
                responses = pd.DataFrame(self.responses, index=[0])
                responses.to_csv("responses_to_prompts.csv")
                time.sleep(30)
                print(f"missed answering {i}")
        print(self.responses)
        responses = pd.DataFrame(self.responses, index=[0])
        responses.to_csv("responses_to_prompts.csv")
        return self.responses

answers_class = PromptsAnswers()
generated_responses = answers_class.get_responses()
responses = pd.DataFrame(generated_responses, index=[0])
responses.to_csv("responses_to_prompts.csv", index=False)
