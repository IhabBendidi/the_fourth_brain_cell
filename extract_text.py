import shlex
import subprocess
import json
import regex
import requests
import os
import tqdm
import multiprocessing
import re




#for filename in tqdm.tqdm(os.listdir(base_path)):

    #filename = """2021.01.04.425279v5.full.pdf"""

def get_meta_files(filename):

    cmd = """curl -X 'POST' \
      'http://0.0.0.0:5000/extract/upload' \
      -H 'accept: application/json' \
      -H 'Content-Type: multipart/form-data' \
      -F 'file=@""" + base_path + filename + """;type=application/pdf'"""
    args = shlex.split(cmd)
    process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    article_text = json.loads(stdout.decode())['text']
    #article_text = ascii(article_text)
    #print(article_text)
    stripped_text = ''
    for c in article_text:
       stripped_text += c if len(c.encode(encoding='utf_8'))==1 else ''
    sentences_1 = [x for x in stripped_text.split("\n") if x.strip() != '' and len(x.strip().split(' ')) > 10]
    sentences_2 = [' '.join(x.split(' ')[:-1]) + ' ' + x.split(' ')[-1].replace('0','').replace('1','').replace('2','').replace('3','').replace('4','').replace('5','').replace('6','').replace('7','').replace('8','').replace('9','') for x in sentences_1]
    sentences = [re.sub(r'http\S+', '', x, flags=re.MULTILINE).replace('bioRxiv','').replace('preprint','').replace('al.','al') for x in sentences_2]
    temp_text = ''.join(sentences)
    sentences = temp_text.split(".")
    with open(text_path + filename + '.txt', 'w') as writer:
        for sentence in sentences :
            sentence = ' '.join(sentence.split(' ')[:-1]) + ' ' + sentence.split(' ')[-1].replace('0','').replace('1','').replace('2','').replace('3','').replace('4','').replace('5','').replace('6','').replace('7','').replace('8','').replace('9','')
            writer.writelines(sentence + "\n")




    entity_dict = {}
    """
    for sentence in tqdm.tqdm(sentences[:120]) :
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }
        params = (
            ('showStats', 'false'),
            ('model-version', 'latest'),
        )
        data = "{ 'documents': [ { 'language': 'en', 'id': '1', 'text': '" + sentence + "' } ]}"
        response = requests.post('https://jargonbuster-analytics.azurewebsites.net/text/analytics/v3.0-preview.1/domains/health', headers=headers, params=params, data=data)
        try :
            entities = json.loads(response.content.decode())['documents'][0]['entities']
            for ent in entities :
                entity_dict[ent['text']] = ent['score']
        except :
            print(response.content)
    json_object = json.dumps(entity_dict, indent = 4)
    with open(entities_path + filename + ".json", "w") as outfile:
        outfile.write(json_object)
    """
if __name__ == '__main__':
    base_path = """./data/pdf/"""
    text_path = "./data/text/"
    entities_path = "./data/entities/"
    #os.mkdir(text_path)
    #os.mkdir(entities_path)
    a_pool = multiprocessing.Pool(7)
    a_pool.map(get_meta_files, os.listdir(base_path))
