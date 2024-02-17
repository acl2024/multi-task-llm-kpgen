import os
import sys
from tqdm import tqdm 
import argparse
import utils

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


parser = argparse.ArgumentParser(description='Llama 2-Chat for keyphrase generation.')
parser.add_argument('--cuda_device', type=str, default='0', help='CUDA device number')
parser.add_argument('--model_name', type=str, default='Llama-2-13b-chat-hf', help='Model name')
parser.add_argument('--model_path', type=str, default='meta-llama/', help='Model path')

parser.add_argument('--dataset_path', type=str, default='data', help='Path to datasets')
parser.add_argument('--dataset_names', nargs='+', default=['inspec', 'krapivin', 'nus', 'semeval', 'kp20k'], help='List of testset')
parser.add_argument('--output_path', type=str, default='results', help='Output path')
parser.add_argument('--instruction', type=str, default='Generate keywords.', help='Instruction prompt')
parser.add_argument('--try_num', type=str, default='1', help='try')
parser.add_argument('--auth_token', type=str, help='HF access tokens')


args = parser.parse_args()

os.environ["CUDA_VISIBLE_DEVICES"] = args.cuda_device

model_name = args.model_name
model_path = os.path.join(args.model_path, model_name)
auth_token = args.auth_token

dataset_path = args.dataset_path
dataset_names = args.dataset_names
output_path = args.output_path
instruction = args.instruction
try_num = args.try_num


prompt_template = '''<s>[INST] <<SYS>> {} <</SYS>>

{} [/INST]'''

tokenizer = AutoTokenizer.from_pretrained(model_path, token=auth_token)
model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.float16, low_cpu_mem_usage=True, token=auth_token)

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f'device: {device}')

model.to(device)
model.eval()

with torch.no_grad():

    for dataset_name in dataset_names:
        print(f"Dataset Name: {dataset_name}")
        

        file_path = os.path.join(dataset_path, dataset_name, 'test_src.txt')
        data_list = utils.read_txt_by_line(file_path)
        print(f'#Doc={len(data_list)}')
        output_list = []
        
        for src_doc_str in tqdm(data_list):

            input_prompt = prompt_template.format(instruction, src_doc_str)
            inputs = tokenizer(input_prompt, return_tensors="pt",)
            inputs = inputs.input_ids.to(device)
            
            outputs = model.generate(inputs, max_new_tokens=256, use_cache=True)
            outputs_str = tokenizer.decode(outputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=False)

            generated_outputs_str = utils.get_generated_output(outputs_str)

            log = {}
            log['prompt'] = input_prompt
            log['input'] = src_doc_str
            log['generated_ourput'] = generated_outputs_str
            # log['raw_output'] = outputs_str

            output_list.append(log)


        result_path = os.path.join(output_path, '%s_%s' % (model_name, instruction), f'try{try_num}')
        if not os.path.exists(result_path):
            os.makedirs(result_path)
            print(f"Directory created: {result_path}")


        result_path = os.path.join(result_path, '%s_%s_%s_result.json' % (dataset_name, model_name, instruction))
        utils.save_json_by_line(output_list, result_path)

print("Done!")