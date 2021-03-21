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

TBD

### Quickstart

To test the recommendations (imagine yourself a student about to answer a question asked by many medical patients in our app), use this curl API request to our deployed web app (deployed in Azure virtual machine).

Run the following line in terminal :

```
curl -X GET 'http://20.61.169.6:4500/api/get_recommendation?question=causes+of+diabetes'
```

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
TBD
```
### Implementation details

- Usage of word2vec pretrained on biomedical data scrapped from Pubmed (bioword2vec)
- Cosine similarity distance
- Easy scalable training and high inference speed even on a small server (4 CPUs, 8GB Ram)
- Better results if Azure Health API is integrated (to extract the keywords )
