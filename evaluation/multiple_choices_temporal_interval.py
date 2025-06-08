import openai
import os
import argparse
import json
import requests
import glob
import ast
from multiprocessing.pool import Pool


def multiple_choice(prediction_folder):
    """
    Evaluates question and answer pairs using GPT-3
    Returns a score for correctness.
    """
    temporal_score = {}
    all_qas_files = glob.glob(prediction_folder + "/*.json")
    model_name = prediction_folder.split("/")[-1]
    
    judge_yes_or_no = 0
    total_qas_num = 0
    
    all_qas_files.sort()
    for i, qas_file in enumerate(all_qas_files):
        with open(qas_file, "r") as f:
            all_qas_set = json.load(f)
        
        qas_set_temporal = [qa for qa in all_qas_set if "Temporal" in qa["Question Type"]]
        if len(qas_set_temporal) == 0:
            continue
        for qas in qas_set_temporal:
            question = qas["Q"]
            answer = qas["answer"]
            options = qas["options"]
            pred = qas["Pred"]
            
            answer_content = options[answer]
            
            # 检查是否正确
            if len(pred) == 1:
                if answer in pred:
                    judge_yes_or_no += 1
            elif len(pred) > 1:
                if answer_content.endswith("."):
                    answer_content = answer_content[:-1]
                if answer_content.endswith("。"):
                    answer_content = answer_content[:-1]
                
                if answer_content in pred:
                    judge_yes_or_no += 1
                
            
            total_qas_num += 1

        temporal_score[model_name] = [judge_yes_or_no, total_qas_num]
        print(f"Done_{model_name}")
    with open("temporal_score_multiple_choice.json", "w") as f:
        json.dump(temporal_score, f)

if __name__ == "__main__":
    predict_folder = "./your_prediction_folder"  # Replace with your actual folder path
    multiple_choice(predict_folder)