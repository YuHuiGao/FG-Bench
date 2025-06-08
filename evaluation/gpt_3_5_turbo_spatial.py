import openai
import os
import argparse
import json
import requests
import glob
import ast
from multiprocessing.pool import Pool


def model_base_eval(prediction_folder):
    """
    Evaluates question and answer pairs using GPT-4omini
    Returns a score for correctness.
    prediction_folder: Path to the folder containing prediction JSON files.
    name of each json file should be like: {video_No.}.json
    name of prediction_folder should be like: {tested_model_name}
    each json file's content FORMAT should be like:
    [
        {
            "Question Type": "Movement Detection", # can be "Semantic Understanding", or other name of subtask, etc.
            "Q": "Question about movement in the video.",
            "A": "Answer about movement in the video.",
            "options": {
                "A": "......",
                "B": "......",
                "C": "......",
                "D": "......",
            },
            "answer": "ground truth choice"# such as "D"
            "Pred": "predicted choice" # such as "D"
        },
        {
            "Question Type": "Semantic Understanding",
            "Q": "Question about semantic understanding in the video.",
            "A": "Answer about semantic understanding in the video.",
            "Pred": "predicted answer" # such as "The cat is on the roof."
        },
    ]
    """
    spatial_score = {}

    all_qas_files = glob.glob(prediction_folder + "/*.json")
    model_name = prediction_folder.split("/")[-1]
    
    score_in_five = 0
    score_binarily = 0
    total_qas_num = 0
    all_qas_files.sort()
    for i, qas_file in enumerate(all_qas_files):
        with open(qas_file, "r") as f:
            rawdata = json.load(f)
        all_qas_set = [qa for item in rawdata for qa in item['qa_set'].values()]
        print(f"Extracting_{model_name}_{qas_file}")
        qas_set_spatial = [qa for qa in all_qas_set if "Spatial" in qa["Question Type"]] 
        print(f"Spatial data Extracted: {model_name}_{qas_file}")
            
        if len(qas_set_spatial) == 0:
            continue
        for qas in qas_set_spatial:
            question = qas["Q"]
            answer = qas["A"]
            pred = qas["Pred"]
            while True:
                try:
                    openai.api_key = "your_api_key"
                    openai.base_url = "your_base_url"
                    # Compute the correctness score
                    headers = {
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {'your_api_key'}"
                    }
                    payload = {
                        "model": "gpt-4o-mini", 
                        "messages": [{
                                "role": "system",
                                "content": 
                                    "You are an intelligent chatbot designed for evaluating the correctness of generative outputs for question-answer pairs. "
                                    "Your task is to compare the predicted answer with the correct answer and determine if they match meaningfully. Here's how you can accomplish the task:"
                                    "------"
                                    "##INSTRUCTIONS: "
                                    "- Focus on the meaningful match between the predicted answer and the correct answer.\n"
                                    "- Consider synonyms or paraphrases as valid matches.\n"
                                    "- Evaluate the correctness of the prediction compared to the answer."
                            },
                            {
                                "role": "user",
                                "content":
                                    "Please evaluate the following video-based question-answer pair:\n\n"
                                    f"Question: {question}\n"
                                    f"Correct Answer: {answer}\n"
                                    f"Predicted Answer: {pred}\n\n"
                                    "Provide your evaluation only as a yes/no and score where the score is an integer value between 0 and 5, with 5 indicating the highest meaningful match. "
                                    "Please generate the response in the form of a Python dictionary string with keys 'pred' and 'score', where value of 'pred' is  a string of 'yes' or 'no' and value of 'score' is in INTEGER, not STRING."
                                    "DO NOT PROVIDE ANY OTHER OUTPUT TEXT OR EXPLANATION. Only provide the Python dictionary string. "
                                    "For example, your response should look like this: {'pred': 'yes', 'score': 4.8}."
                            }
                        ]
                    }
                    # Convert response to a Python dictionary.
                    response = requests.post("your_base_url/v1/chat/completions", headers=headers, json=payload)
                    response = response.json()
                    response = response["choices"][0]["message"]["content"]
                    response_dict = ast.literal_eval(response)
                    
                    score_in_five += response_dict["score"]
                    score_binarily += 1 if response_dict["pred"] == "yes" else 0
                    total_qas_num += 1
                    break
                except:
                    continue
        spatial_score[model_name] = [score_in_five, score_binarily, total_qas_num]
        print(f"Done_{model_name}")
    with open("spatial_score.json", "w") as f:
        json.dump(spatial_score, f)

if __name__ == "__main__":
    prediction_folder = "./your_prediction_data_folder"  # Replace with your actual folder path
    model_base_eval(prediction_folder)