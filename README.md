# Multi-Task Prompting in Large Language Models for Zero-Shot Keyphrase Generation

This account is an anonymous account for ACL 2024.

## Requirements    
- openai 
- pytorch 
- transformers 4.32.0
- accelerate 0.24.1 


## Dataset

The datasets are the tokenized version provided by [Jiacheng Ye](https://github.com/jiacheng-ye/kg_one2set).


## Inference
Please note that the 'gpt-3.5-turbo' model alias was upgraded from 'gpt-3.5-turbo-0613' to 'gpt-3.5-turbo-0125' on February 16th.
```bash
# ChatGPT
python gpt_inference.py \
  --model_name gpt-3.5-turbo-0613 \
  --dataset_names inspec nus krapivin semeval kp20k \
  --instruction "Generate keywords." \
  --api_key YOUR_API_KEY_HERE

# Llama 2-Chat
python llama2_inference.py \
  --cuda_device 0 \
  --model_name Llama-2-13b-chat-hf \
  --dataset_names inspec nus krapivin semeval kp20k \
  --instruction "Generate keywords." \
  --auth_token YOUR_AUTH_TOKEN_HERE
```

## Evaluation
```bash
python eval.py \
  --pred_dir_path "results/gpt-3.5-turbo-0613_Generate keywords./try1" \
  --dataset_names inspec nus krapivin semeval kp20k
```
