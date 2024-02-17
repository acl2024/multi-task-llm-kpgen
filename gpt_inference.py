import os
from tqdm import tqdm 
import argparse
import utils

from openai import OpenAI

parser = argparse.ArgumentParser(description='ChatGPT for keyphrase generation.')
parser.add_argument('--model_name', type=str, default='gpt-3.5-turbo', help='Model name')

parser.add_argument('--dataset_path', type=str, default='data', help='Path to datasets')
parser.add_argument('--dataset_names', nargs='+', default=['inspec', 'krapivin', 'nus', 'semeval', 'kp20k'], help='List of testset')
parser.add_argument('--output_path', type=str, default='results', help='Output path')
parser.add_argument('--instruction', type=str, default='Generate keywords.', help='Instruction prompt')
parser.add_argument('--try_num', type=str, default='1', help='try')
parser.add_argument('--api_key', type=str, help='Openai api key')

args = parser.parse_args()


model_name = args.model_name
api_key = args.api_key

dataset_path = args.dataset_path
dataset_names = args.dataset_names
output_path = args.output_path
instruction = args.instruction
try_num = args.try_num



client = OpenAI(api_key=api_key)

for dataset_name in dataset_names:
    print(f"Dataset Name: {dataset_name}")
    
    file_path = os.path.join(dataset_path, dataset_name, 'test_src.txt')
    data_list = utils.read_txt_by_line(file_path)
    print(f'#Doc={len(data_list)}')
    output_list = []
    
    for src_doc_str in tqdm(data_list):

        response= client.chat.completions.create(
            model=model_name,
            messages=[
                {
                "role": "system",
                "content": instruction
                },
                {
                "role": "user",
                "content": src_doc_str
                }
            ],
            temperature=0.5,
            max_tokens=256,
            top_p=1)

        if response.choices[0].message.content is not None:
            generated_outputs_str = response.choices[0].message.content
        else:
            generated_outputs_str = ''

        log = {}
        log['prompt'] = instruction
        log['input'] = src_doc_str
        log['generated_ourput'] = generated_outputs_str
        # log['raw_output'] = generated_outputs_str

        output_list.append(log)

        result_path = os.path.join(output_path, '%s_%s' % (model_name, instruction), f'try{try_num}')
        if not os.path.exists(result_path):
            os.makedirs(result_path)
            print(f"Directory created: {result_path}")

    result_path = os.path.join(result_path, '%s_%s_%s_result.json' % (dataset_name, model_name, instruction))
    utils.save_json_by_line(output_list, result_path)
    
print("Done!")