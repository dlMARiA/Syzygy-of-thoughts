# Syzygy-of-thoughts
🚀 **Hello, [社交平台账号](https://www.youtube.com/watch?v=gZABle836yM)**  
- xxxxxxxxxxxxxxxxxxxxxxx

<div align='left'>
<img src="assets/rader.png" alt="teaser" width="400" />
</div>
本项目为论文《Syzygy of Thoughts: Enhancing LLM Reasoning with Minimal Free Resolution》的代码实现。该论文提出了一种新颖的推理框架 Syzygy of Thoughts (SoT)，通过将交换代数与同调代数中的 最小自由分解 (Minimal Free Resolution, MFR) 原理融入思维链 (Chain of Thought, CoT)，显著提升大型语言模型 (LLM) 在复杂推理任务中的性能。SoT 针对传统 CoT 在高维、非线性推理中的局限，引入模块、自由性、映射、精确性、最小性和 Betti 数等结构化分解策略，将复杂问题转化为紧凑且逻辑自洽的推理单元。
实验在 GSM8K 和 MATH 等数据集上进行，涵盖 GPT-4o-mini、Qwen2.5 等模型，SoT 的推理准确率达到或超越主流 CoT 标准（例如，GSM8K 96.0%，MATH 79.1%），且在高温条件下保持稳定性，推理时间更具可扩展性。


<div align='left'>
<img src="assets/main.png" alt="teaser" width="800" />
</div>






## Highlights
- *
- *


## Overview
- [Schedule](#schedule)
- [Citation](#citation)
- [Installation](#installation)
- [API Configuration Setup](#api-configuration-setup)
- [Data Preparation](#data-preparation)
- [Quick Start](#quick-start)
- [Model Zoo](#model-zoo)


## Schedule
介绍xxxxxx:

- [x] Release model code of PTv3;
- [x] Release scratched config and record of indoor semantic segmentation;
  - [x] ScanNet
  - [x] ScanNet200
  - [x] S3DIS
  - [x] S3DIS 6-Fold (with cross-validation script) 


## Citation
If you find Syzygy-of-thoughts useful to your research, please cite our work as an acknowledgment. (*^▽^*)
bib
@article{zhang2023faster,
  title={Faster segment anything: Towards lightweight sam for mobile applications},
  author={Zhang, Chaoning and Han, Dongshen and Qiao, Yu and Kim, Jung Uk and Bae, Sung-Ho and Lee, Seungkyu and Hong, Choong Seon},
  journal={arXiv preprint arXiv:2306.14289},
  year={2023}
}


## Installation
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

## API Configuration Setup

Before using the Atom of Thoughts (AoT) framework, you need to set up your API key and URL:

1. Create an apikey.py file in the project root directory with the following format:

url = "https://api.openai.com/v1"  # Replace with your API endpoint
api_key = [
    "your-api-key-here",  # Replace with your actual API key
    # You can add multiple API keys to improve concurrency performance.
]

### Api Key 获取途径




### Requirements
 Syzygy-of-thoughts :

(Recommendation)
- Ubuntu: 
- CUDA: 
- PyTorch: 

### Environment

- Base environment
bash
# 改成我们自己的
conda create -n pointcept python=3.8 -y
conda activate pointcept
conda install ninja -y
conda install pytorch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 pytorch-cuda=11.8 -c pytorch -c nvidia
conda install h5py pyyaml -c anaconda -y
conda install sharedarray tensorboard tensorboardx yapf addict einops scipy plyfile termcolor timm -c conda-forge -y
conda install pytorch-cluster pytorch-scatter pytorch-sparse -c pyg -y
pip install torch-geometric

cd libs/pointops
python setup.py install
cd ../..

# spconv (SparseUNet)
# refer https://github.com/traveller59/spconv
pip install spconv-cu118  # choose version match your local cuda version

# Open3D (visualization, optional)
pip install open3d



## Data Preparation
Please further refer xxx

## Quick Start
xxxxxxxxxxxxx


## Model Zoo
### 1. 实验性能
以下表格比较了 CoT、CoT-SC (n=5) 和 SoT 在多种任务上的性能，涵盖数学推理（GSM8K、SVAMP、MultiArith、ASDiv、AQUA）、通用知识（MMLU）、多任务问答（BBH）、时间推理（Date）和逻辑推理（CLUTRR）。SoT 在所有模型和任务中均取得最佳表现。
| **Method**                        | **GSM8K** | **SVAMP** | **MultiArith** | **ASDiv** | **AQUA** | **MMLU** | **BBH** | **Date** | **CLUTRR** |
|------------------------------------|:---------:|:---------:|:--------------:|:---------:|:--------:|:--------:|:-------:|:--------:|:----------:|
| **GPT-4o-mini**                    |           |           |                |           |          |          |         |          |            |
| CoT                                | 85.1%     | 84.4%     | 99.2%          | 97.0%     | 65.0%    | 63.1%    | 66.3%   | 51.8%    | 65.9%      |
| CoT-SC (n=5)                       | 90.1%     | 86.0%     | 99.5%          | 98.5%     | 70.9%    | 67.3%    | 69.2%   | 54.9%    | 72.4%      |
| **SoT (Ours)**                     | **96.0%** | **92.2%** | **99.7%**      | **99.8%** | **75.6%** | **75.2%** | **72.8%** | **75.2%** | **75.7%**  |
| **Qwen2.5-Coder-7B-Instruct**      |           |           |                |           |          |          |         |          |            |
| CoT                                | 77.2%     | 82.4%     | 92.3%          | 92.0%     | 60.6%    | 55.1%    | 47.1%   | 31.0%    | 20.1%      |
| CoT-SC (n=5)                       | 80.2%     | 84.1%     | 95.0%          | 95.0%     | 62.2%    | 56.3%    | 49.3%   | 32.9%    | 21.0%      |
| **SoT (Ours)**                     | **89.1%** | **90.6%** | **97.0%**      | **99.8%** | **63.3%** | **57.1%** | **57.3%** | **36.2%** | **26.3%**  |
| **Qwen2.5-VL-72B-Instruct**        |           |           |                |           |          |          |         |          |            |
| CoT                                | 86.1%     | 86.9%     | 98.8%          | 98.0%     | 81.1%    | 80.1%    | 77.3%   | 75.2%    | 70.1%      |
| CoT-SC (n=5)                       | 89.1%     | 88.2%     | 99.3%          | 98.4%     | 83.9%    | 82.9%    | 79.0%   | 78.0%    | 75.0%      |
| **SoT (Ours)**                     | **96.0%** | **95.8%** | **99.7%**      | **99.2%** | **89.4%** | **84.3%** | **85.3%** | **80.2%** | **78.9%**  |
| **Gemma-3-27b-it**                 |           |           |                |           |          |          |         |          |            |
| CoT                                | 83.1%     | 85.9%     | 91.9%          | 98.5%     | 80.3%    | 70.8%    | 70.7%   | 76.9%    | 65.3%      |
| CoT-SC (n=5)                       | 87.1%     | 87.0%     | 92.3%          | 99.2%     | 85.4%    | 73.2%    | 73.2%   | 80.2%    | 66.4%      |
| **SoT (Ours)**                     | **96.0%** | **95.8%** | **99.7%**      | **99.2%** | **89.4%** | **84.3%** | **85.3%** | **80.2%** | **78.9%**  |
| **Gemma-3-12b-it**                 |           |           |                |           |          |          |         |          |            |
| CoT                                | 83.2%     | 79.0%     | 90.4%          | 97.7%     | 68.9%    | 68.1%    | 64.6%   | 77.7%    | 49.0%      |
| CoT-SC (n=5)                       | 86.1%     | 81.0%     | 93.3%          | 98.0%     | 71.7%    | 70.6%    | 66.7%   | 80.2%    | 52.2%      |
| **SoT (Ours)**                     | **92.1%** | **92.5%** | **96.1%**      | **99.2%** | **77.2%** | **72.3%** | **69.1%** | **82.5%** | **55.0%**  |
