import os
import json
import glob


def simple_check(prediction_folder):
    """
    Evaluates question and answer pairs using simple check
    Returns a score for correctness.
    """
    text_recog_score = {}
    all_qas_files = glob.glob(prediction_folder + "/*.json")
    model_name = prediction_folder.split("/")[-1]
    
    judge_yes_or_no = 0
    total_qas_num = 0
    
    all_qas_files.sort()
    for i, qas_file in enumerate(all_qas_files):
        with open(qas_file, "r") as f:
            all_qas_set = json.load(f)
        
        qas_set_text_recog = [qa for qa in all_qas_set if "Text Recognition" in qa["Question Type"]]
        if len(qas_set_text_recog) == 0:
            continue
        for qas in qas_set_text_recog:
            question = qas["Q"]
            answer = [qas["A"]]
            if "a" in qas:
                answer.append(qas["a"])
            if "a_1" in qas:
                answer.append(qas["a_1"])
            if "a_2" in qas:
                answer.append(qas["a_2"])
            if "a_3" in qas:
                answer.append(qas["a_3"])

            pred = qas["Pred"]

            flag = False
            answer = [item.lower() for item in answer]
            pred = pred.lower()
            for i,item in enumerate(answer):
                if item.endswith("."):
                    answer[i] = item[:-1]
            if pred.endswith("."):
                pred = pred[:-1]
            for i,item in enumerate(answer):
                if item.endswith("。"):
                    answer[i] = item[:-1]
            if pred.endswith("。"):
                pred = pred[:-1]
            # check if pred is in answer
            if answer[0] in pred:
                judge_yes_or_no += 1
                flag = True
            else:
                if len(answer) > 1:
                    for item in answer:
                        if item in pred:
                            judge_yes_or_no += 1
                            flag = True
                            break
            
            if not flag:
                if pred in answer[0]:
                    judge_yes_or_no += 1
                    flag = True
                else:
                    if len(answer) > 1:
                        for item in answer:
                            if pred in item:
                                judge_yes_or_no += 1
                                flag = True
                                break
                    
            total_qas_num += 1

    text_recog_score[model_name] = [judge_yes_or_no, total_qas_num]
    print(f"Done_{model_name}")
    with open("score_text_recognition.json", "w") as f:
        json.dump(text_recog_score, f)

if __name__ == "__main__":
    prediction_folder = "./predict_folder"  # Replace with your actual folder path
    simple_check(prediction_folder)