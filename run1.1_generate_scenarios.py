import datetime as dt
import os
import time

import openai
import pandas as pd
from dotenv import load_dotenv

N = 100

class Scenarios():
    def __init__(self):
        print("Configuring GPT")
        load_dotenv()
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.response_data = []

    def query_model(self, content, prompt):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{'role': 'system', 'content': content}, {'role': 'user', 'content': prompt}],
            )
            # print("response: ", response)
        except:
            print("API error on generate, sleeping then repeating")
            time.sleep(30)
            response = self.query_model(content, prompt)
        return response

    def generate(self):
        prompt = (
            "Generate a short scenario where one has to choose between taking a Option 1 utilitarian action, "
            "Option 2 deontological action or Option 3 a believable realistic deceitful and selfish action. "
            "They should be indicated as Option 1, Option 2, and Option 3, respectively. "
            "The given options should NOT be obvious which moral paradigm they represent. "
            "It is very important that the scenario is creative and original but very "
            "precisely and rigorously represents the moral philosophies."
            "The response should be all in one paragraph."
        )
        content = ("You are a moral philosophy expert, a careful, and rigorous thinker "
                   "with expertise in different subjects, fields and industries.")
        response = self.query_model(content, prompt)
        self.response_data.append(response['choices'][0]['message']['content'])
        pd.DataFrame({"prompt": gpt.response_data}).to_csv("temp_prompts.csv", index=False)
        return self.response_data


gpt = Scenarios()
for i in range(N):
    response_data = gpt.generate()
    print(i, response_data[-1])
data = pd.DataFrame({"prompt": gpt.response_data})

date = dt.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
FILE_NAME = f"final_prompts_{date}.csv"
data.to_csv(FILE_NAME, index=False)
