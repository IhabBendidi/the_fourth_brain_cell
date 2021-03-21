from gensim.summarization.summarizer import summarize
from gensim.summarization import keywords
import multiprocessing
import os


def get_summaries(filename):
    with open(text_path + filename + '.txt','r') as reader:
        content = reader.read()
    summ_per = summarize(content, ratio = 0.03)
    for i in range(10):
        summ_per = summ_per.replace(str(i),'')
    with open(summary_path + filename + '.txt','w') as writer :
        writer.write(summ_per)

if __name__ == '__main__':
    base_path = """./data/pdf/"""
    text_path = "./data/text/"
    summary_path = "./data/summaries/"
    #os.mkdir(text_path)
    #os.mkdir(entities_path)
    a_pool = multiprocessing.Pool(7)
    a_pool.map(get_summaries, os.listdir(base_path))
