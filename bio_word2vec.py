from gensim.models import KeyedVectors
import os
import tqdm
import json



model = KeyedVectors.load_word2vec_format("./biomodel/bio_embedding_extrinsic", binary=True)


global filenames
filenames = []
global word_embeddings
word_embeddings =[]
base_path = """./data/pdf/"""
text_path = "./data/text/"
entities_path = "./data/entities/"
summary_path = "./data/summaries/"


def document_vectors(filename):
    with open(summary_path + filename + '.txt','r') as reader :
        summary = reader.read()
    avgword2vec = None
    count = 0
    for word in summary.split():
        if word in model.wv.vocab:
            count += 1
            if avgword2vec is None:
                avgword2vec = model[word.lower()]
            else:
                avgword2vec = avgword2vec + model[word.lower()]

    if avgword2vec is not None:
        avgword2vec = avgword2vec / count
        word_embeddings.append(avgword2vec.tolist())
        filenames.append(filename)


for filename in tqdm.tqdm(os.listdir(base_path)) :
    document_vectors(filename)

output_dict = {"filenames" : filenames,"word_embeddings" : word_embeddings}
json_object = json.dumps(output_dict, indent = 4)
with open("word_embeddings.json", "w") as outfile:
    outfile.write(json_object)
