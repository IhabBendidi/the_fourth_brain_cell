# The Fourth Brain Cell

This project is made by The Three Last Brain Cells team, in the starthack Hackathon, Microsoft Challenge.

### Table of Contents

- goal
- Project description
- Quickstart
- Dataset used
- Installation
- Usage
- Implementation details

### Goal

The goal of the project is to empower patients to better understand medical information. Inspired by how the developer community and research community federate each other to peer review papers or answers, either through journals or stackoverflow, we present the global project Medoverflow for simplified medicine. The theorical details of the project can be found in the pitch video, but at it's core, the real challenge is to recommend to medical students (who will write answers that our chatbot would use in his database of answers to medical patients) peer reviewed research papers as well as their summaries rapidly, for a maximum efficiency.

This repository only focuses on all the technical aspects and implementation of the recommendation engine needed for that task, as it was deemed more important and central to this project (in the small time we got) than spending that time working on web interfaces without the proper technology and innovation behind it.

### Project Description

#### General description

Patients will have access to a chatbot that can answer medical questions. The chatbot will be able to generate understandable answers based on the information that is on a medical forum where medical professionals are encouraged to contribute accessible and understandable answers to medical questions. Medical professionals and their related institutions will receive a score based on the amount of answers they provide, the quality of these answers and how understandable these answers are articulated.
The main incentive to contribute to the platform is the score, which translates into reputational value for medical students, doctors,... and for their related institutions as a whole (hospitals, universities,...).

We get the valuable medical information from the researcher to the patient in the following steps.
First, a paper is written and it goes through a peer review process. Then, the paper gets published. This part of the process has been around for a long time, but this is the point where we step in to make this information accessible to people who haven’t spent over a decade at university to study this kind of stuff.
We use a word2vec embedding trained on pubmed data for vectorizing the papers, then we use metrics of similarity to link papers to the questions that patients will ask.

Next we provide a summary of the papers on the Med Overflow professional platform where medical students (and professionals) convert it into an understandable explanation. Different medical professionals review the answers and the highest ranked answer is sent to the patient through the chatbot we created with Rasa.

#### scope of this repository

In this repository, we're creating the recommendation engine that is coupled with the Jargon API offered by Microsoft, to extract information. This recommendation engine we made has a database of pdf research papers that it uses as a reference, and then depending on the questions of the user, summarizes the most relevant research papers to that specific question. This is supposed to both help medical students write up easily and efficiently correct answers, and for the people that don't find reliable answers to at least have the most reliable research papers summarized.

This is an API without a graphic interface. This part was deemed the most critical and priority of the project (constraints of time)

### Quickstart

To test the recommendations (imagine yourself a student about to answer a question asked by many medical patients in our app), use this curl API request to our deployed web app (deployed in Azure virtual machine).

Run the following line in terminal :

```
curl -X GET 'http://20.61.169.6:4500/api/get_recommendation?question=causes+of+love'
```

(Yep, `causes of love` surprisingly worked as a question :D)

Replace the question by a medical question of your choice. Worth noting that the precision of the recommendation would become way better using the health API of azure (details in implementation details below).

(The '+' means a space)

### Data used

The data used is pdf research papers cited in PubMed and downloaded from bioRxiv in this test. In production, all papers would be sourced from various journals directly. The number of research papers used is 103 research paper, about random subjects about clinical trials and drug development.

### Installation

#### Downloading the model

in the `biomodel` folder, download the model using this command :

```
wget https://s3-eu-west-1.amazonaws.com/pfigshare-u-files/12551780/bio_embedding_extrinsic
```

#### Running the installation

Install dependencies with `pip3 install -r requirements.txt`

Then run the app with :

```
python3 app.py
```

If new papers are going to be added to the database and synchronized, [Medical Jargon API](https://github.com/whatchacallit/medjargonbuster-api) should be installed (check its installation steps) and launched in the same server so that the two servers could communicate.

The medical jargon API is only used to extract the text from pdf files of research papers

### Usage

#### Run locally (Optional)

Follow the next commands (after installation) to run locally :

```
python3 app.py
```

Be sure to check in the last line of the `app.py` file that `host = 0.0.0.0` is deleted if you wish to run locally

The endpoint would become `http://127.0.0.1:4500`

#### synchronizing papers

Each time a research paper is added in the `/data/pdf` folder, whether locally or on server, run the following command on terminal to synchronize results of all papers :

```
bash synch.sh
```

The operation doesn't take long, and it can still be optimized further (TODO for post-hackathon)


#### Getting summary recommendations

We expose one API to get summary/paper recommendations.

- **Curl request :**

```
curl -X GET 'http://20.61.169.6:4500/api/get_recommendation?question=YOUR_QUESTION'
```

- **Input :** A string of a question to ask the recommender, so that it would return top 2 articles related to this question and their summary. Note that all spaces in the question would be replaced by "+" in the request for it to work

- **Output :**

Response example :

```
{
  "code": 200,
  "response": {
    "1": {
      "file": "2021.02.08.430342v1.full.pdf",
      "summary": "The putative causal effect of type  diabetes ..."
    },
    "2": {
      "file": "389841v2.full.pdf",
      "summary": "proposed measuring subjective sleep ... "
    }
  }
}
```

The first summary and file are the best fit, followed by the second
### Implementation details

- Usage of word2vec pretrained on biomedical data scrapped from Pubmed (bioword2vec)
- Cosine similarity distance
- Easy scalable training and high inference speed even on a small server (4 CPUs, 8GB Ram)
- Better results if Azure Health API is integrated (to extract the keywords that are the most important in the text and apply word2vec on them, or extract the entities from questions). It was tested before the API's quota was done, and it actually gave much better result, as it only compares relevant keywords with cosine similarity.
- Also worth noting that while we used a summarization algorithm similar to the Medical Jargon API, we believe we might have slightly improved results because of a more improved preprocessing (but only adapted to PDF files coming from Biorxiv, so it gotta be changed and adapted when going at scale)
