# FG Benchmark

Official repository of "[Do Current Video LLMs Have Strong OCR Abilities? A Preliminary Study](https://aclanthology.org/2025.coling-main.659/)"

**FG Bench**, a novel benchmark designed to evaluate the OCR performance of multi-modal models in videos. Comprising 1,028 videos and 2,961 question-answer pairs, 

Download： [The thunder SkyDrive](https://pan.xunlei.com/s/VODLlDIq_iJCO4ol84e2t3_3A1?pwd=zjnc#) or [Baidu Netdisk](https://pan.baidu.com/s/1g56idSRa0afZiNCkg7dB9A?pwd=pyu5)

# News

`2025.1.20` FG-Bench is released

`2024.11.30`  FG-Bench is accepted by COLING 2025

# FG-Bench

FG Bench (Video-OCR Bench) is the **first specialized benchmark** for evaluating the video OCR capabilities of multimodal large language models (LLMs). It systematically tests models' performance in core scenarios such as dynamic text processing, temporal localization, and multi-frame information integration. The benchmark provides high-quality datasets and a standardized evaluation framework through a combination of **semi-automated construction processes** and **manual refinement**, offering critical references for the research and optimization of video LLMs.

![example_subtask](.\examples.png)

#### **Core Features**

1. **Multi-Dimensional Task Coverage**
   Includes **6 sub-tasks** that comprehensively simulate real-world video OCR requirements:

   - **Text Recognition (TR)**: Accurately extract dynamic text content (e.g., moving license plates, counter numbers);
   - **Semantic Understanding (SU)**: Analyze text meaning in context (e.g., the applicability of "buy one, get one free");
   - **Spatial Relation (SR)**: Locate the relative position of text to objects (e.g., the object with an "Exit" sign);
   - **Text Attribute Recognition (TAR)**: Identify visual attributes such as font color and language;
   - **Movement Detection (MD)**: Track the movement trajectory of text or objects (e.g., the driving direction of a vehicle);
   - **Temporal Localization (TL)**: Determine when text appears/disappears (e.g., the first occurrence time of a warning message).

2. **Large-Scale High-Quality Dataset**

   - **1,028 videos**: Covering 20+ scenarios such as driving, news, and education, with an average duration of 10–30 seconds;
   - **2,961 question-answer pairs**: Generated using InternVL-1.5 and GPT-3.5, with manual validation for logical correctness and visual dependency;
   - **Dynamic scenario design**: Includes complex challenges like text occlusion, frame-by-frame changes, and high-speed movement.

3. **Semi-Automated Construction Process**

   ![liuchengtu](.\process_pipline.png)

   - **Efficiency and Cost-Effectiveness**: Combines OCR capabilities of image LLMs (e.g., InternVL-1.5 for text attribute extraction) with manual optimization, deployable on a single A6000 GPU;
   - **Data Quality Assurance**: Uses GPT-4o-mini to evaluate semantic consistency, ensuring unique answers and video-dependent questions.

4. **Comprehensive Evaluation Framework**

   - **14 Models Tested**: Including 8 video LLMs (e.g., Qwen2-VL-7B, MiniCPM-V 2.6) and 6 image LLMs (e.g., Monkey);
   - **Multi-Metric Evaluation**: Accuracy, semantic alignment, and multiple-choice positioning precision to quantify model performance across tasks;
   - **Weakness Diagnosis**: All models showed accuracy <0.25 in **temporal localization tasks**, highlighting insufficient temporal modeling capabilities.

#### **Key Achievements and Findings**

![image-20250520171043781](.\results.png)

- **Top Model Performance**: Qwen2-VL-7B (average score 0.4653) and MiniCPM-V 2.6 (0.4508) lead in overall performance but still perform near random guesses in temporal localization;
- **Advantages of Video LLMs**: Significantly outperform image LLMs in dynamic information processing (single-image models like Monkey scored <0.2);
- **Insights from Movement Detection**: Frame-by-frame analysis improves dynamic information capture, with frame-wise processing models achieving 0.592 accuracy in movement detection, far exceeding frame-stitching methods.

