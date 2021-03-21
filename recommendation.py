from gensim.models import KeyedVectors
import os
import tqdm
import json
from sklearn.metrics.pairwise import cosine_similarity
import heapq

print("starting the model...")
model = KeyedVectors.load_word2vec_format("./biomodel/bio_embedding_extrinsic", binary=True)

nb_returns = 2








global filenames
filenames = []
global word_embeddings
word_embeddings =[]
base_path = """./data/pdf/"""
text_path = "./data/text/"
entities_path = "./data/entities/"
summary_path = "./data/summaries/"

with open("word_embeddings.json", "r") as infile:
    content = json.load(infile)
filenames = content['filenames']
word_embeddings = content['word_embeddings']
def get_question(question):
    cosine_list = []
    question = question.lower()
    avgword2vec = None
    count = 0
    for word in question.split():
        if word in model.wv.vocab:
            count += 1
            if avgword2vec is None:
                avgword2vec = model[word]
            else:
                avgword2vec = avgword2vec + model[word]
    if avgword2vec is not None:
        avgword2vec = avgword2vec / count
    for emb in word_embeddings :
        cosine_similarities = cosine_similarity([emb], [avgword2vec.tolist()])
        cosine_list.append(cosine_similarities[0][0])
    max_indexes = heapq.nlargest(nb_returns, range(len(cosine_list)), key=cosine_list.__getitem__)
    #max_value = max(cosine_list)
    #max_index = cosine_list.index(max_value)
    output = {}
    for i in range(len(max_indexes)) :
        best_filename = filenames[max_indexes[i]]
        with open(summary_path + best_filename + '.txt','r') as reader :
            summary = reader.read()
        output[i+1] = {"file": best_filename ,"summary" :summary}
    return output

#test_question = "causes of diabete"

#summary = get_question(test_question)

#json_formatted_str = json.dumps(summary, indent=2)
#print(json_formatted_str)
