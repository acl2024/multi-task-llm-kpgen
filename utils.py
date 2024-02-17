import re
import json

def read_json_by_line(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines  = f.readlines()
    return [json.loads(line.strip()) for line in lines]

def read_txt_by_line(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def save_json_by_line(j_list, filepath):
    with open(filepath, "w", encoding='utf-8') as f:
        for json_data in j_list:
            f.write(json.dumps(json_data, ensure_ascii=False)+'\n')

def save_list_to_txt(str_list,filepath):
    with open(filepath, 'w') as file:
        for string in str_list:
            file.write(string + "\n")

def listToStr(tokens):
    sentence = ""
    for token in tokens:
        sentence = sentence+token+" "
    return sentence.strip()

def get_generated_output(str):
    split_prompt_output = str.split('[/INST]')
    return split_prompt_output[-1].strip()



def cleaning(text):
    text = re.sub(r'[\w\d]+(?:\.[\w\d]+)+', '', text)
    text = text.strip()
    text = text.lstrip(':')
    text = text.lstrip('.')
    text = text.lstrip('-')


    text = text.split(' - ')[0]
    text = text.split(':')[0]
    keyphrase = text.strip()
    keyphrase = keyphrase.replace('\"', '')
    keyphrase = keyphrase.strip()

    return keyphrase


def extract_keyphrases_from_output(text):


    lines = text.split('\n')

    keyphrases = []

    for line in lines:
        line = line.strip()
        if not line or line.lower().startswith('title:') or line.lower().startswith('summary:'):
            continue

        if line[0].isdigit() and '. ' in line:
            keyphrase = line.split('. ', 1)[1].rstrip('.').strip()
            keyphrase = cleaning(keyphrase)

            if keyphrase.lower() not in ['none', 'none found', '']:
                keyphrases.append(keyphrase)

        elif line.startswith('*'):
            parts = line.split('* ', 1)
            if len(parts) > 1:
                keyphrase = parts[1].rstrip('.').strip()
                keyphrase = cleaning(keyphrase)
                if keyphrase.lower() not in ['none', 'none found', '']:
                    keyphrases.append(keyphrase)
        elif line.startswith('•'):
            parts = line.split('• ', 1)
            if len(parts) > 1:
                keyphrase = parts[1].rstrip('.').strip()
                keyphrase = cleaning(keyphrase)
                if keyphrase.lower() not in ['none', 'none found', '']:
                    keyphrases.append(keyphrase)
        
        elif line.startswith('-'):
            parts = line.split('- ', 1)
            if len(parts) > 1:
                keyphrase = parts[1].rstrip('.').strip()
                keyphrase = cleaning(keyphrase)
                if keyphrase.lower() not in ['none', 'none found', '']:
                    keyphrases.append(keyphrase)

        elif line.lower().startswith('keyphrases:'):
            parts = line.lower().split('keyphrases:', 1)
            if len(parts) > 1:
    
                phrases = parts[1].replace(';', ',').split(',')
                for phrase in phrases:
                    keyphrase = phrase.rstrip('.').strip()
                    keyphrase = cleaning(keyphrase)
                    if keyphrase and keyphrase.lower() not in ['none', 'none found', '']:
                        keyphrases.append(keyphrase)

        elif line.lower().startswith('keywords:') or 'keywords' in line.lower():
            parts = line.lower().split('keywords:', 1)
            if len(parts) > 1:

                phrases = parts[1].replace(';', ',').split(',')
                for phrase in phrases:
                    keyphrase = phrase.rstrip('.').strip()
                    keyphrase = cleaning(keyphrase)

                    if keyphrase and keyphrase.lower() not in ['none', 'none found', '']: 
                        keyphrases.append(keyphrase)

        elif line.lower().startswith('indexing terms:') or 'indexing terms' in line.lower():
            parts = line.lower().split('indexing terms:', 1)
            if len(parts) > 1:
                phrases = parts[1].replace(';', ',').split(',')
                for phrase in phrases:
                    keyphrase = phrase.rstrip('.').strip()
                    keyphrase = cleaning(keyphrase)
                    if keyphrase and keyphrase.lower() not in ['none', 'none found', '']: #nIndexing Terms: 
                        keyphrases.append(keyphrase)

        elif len(line.split(';')) > 2:
            phrases = line.split(';')
            for phrase in phrases:
                keyphrase = phrase.rstrip('.').strip()
                keyphrase = cleaning(keyphrase)

                if keyphrase and keyphrase.lower() not in ['none', 'none found', '']:
                    keyphrases.append(keyphrase)
        elif len(line.split(',')) > 2:
            temp = []
            is_not_sent = True

            phrases = line.split(',')
            for phrase in phrases:

                keyphrase = phrase.rstrip('.').strip()
                keyphrase = cleaning(keyphrase)
                if len(keyphrase.replace('.',"").split()) > 6:
                    is_not_sent = False
                    break

                if keyphrase and keyphrase.lower() not in ['none', 'none found', '']:           
                    temp.append(keyphrase)
            if is_not_sent:
                keyphrases.extend(temp)

    return keyphrases