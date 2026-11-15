# DMML-CourseWork01

**F21DL Data Mining and Machine Learning — Group Coursework (2026/2027)**

## Project title

Trust or trick? Detecting fraudulent and scam websites from URL and page signals.

**Coursework topic:** Topic 11 — Predict whether a website is fraudulent/scam.

## Overview

A phishing website is a fake page built to look like a real one so that a person
enters a password or card number and an attacker keeps it. This project builds and
compares classifiers that decide, for a given website, whether it is legitimate or
phishing, and it asks a second question along the way: which kind of evidence
actually carries the signal — the cheap text of the URL, or the signals taken from
the page behind it?

The whole implementation lives in a single notebook, inside the `Notebook` folder:

```
Notebook/DataMining&MachineLearning_Coursework_01.ipynb
```

## Dataset

**PhiUSIIL Phishing URL Dataset** — UCI Machine Learning Repository, dataset ID 967.

| Field | Value |
|---|---|
| Source | https://archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+dataset |
| Size | 235,795 rows, 56 columns |
| Classes | 134,850 legitimate, 100,945 phishing |
| Features | Raw `URL` string plus 51 numeric features extracted from the URL and the page source |
| Licence | CC BY 4.0 |
| Citation | Prasad, A. and Chandra, S. (2024) *PhiUSIIL*, Computers and Security, 136, 103545 |

The raw file is stored at `Datasets/PhiUSIIL_Phishing_URL_Dataset.csv`. If it is
missing it can be re-downloaded with:

```bash
cd Datasets
curl -O "https://archive.ics.uci.edu/static/public/967/phiusiil+phishing+url+dataset.zip"
unzip phiusiil+phishing+url+dataset.zip
```

## Requirements covered

| Requirement | Where it is answered |
|---|---|
| **R1** Project topic, direction and research questions | Notebook, Step 1 |
| **R2** Cleaning, EDA, visualisation, feature selection and evaluation, clustering with metrics | Notebook, Steps 3–9 |
| **R3** At least three classical ML algorithms, compared with the right metrics, plus a discussion of decision trees | Notebook, Steps 10–11 |
| **R4** Neural network models, trained, tuned and compared | Notebook, Steps 12 to 13 |

### Models compared

Classical (R3): Gaussian Naive Bayes, Logistic Regression, Perceptron,
k-Nearest Neighbours, Decision Tree, Random Forest, Gradient Boosting.

Neural (R4): a Multi-Layer Perceptron on the engineered features, and BERT-lite
(`google/bert_uncased_L-2_H-128_A-2`) mean-pooled URL embeddings with an MLP head.

No convolutional network is used. Section 3.2 of the brief ties the CNN to an image
dataset, and this topic has no image data. The notebook says so in the Step 12 introduction.

Unsupervised (R2): K-Means and a Gaussian Mixture Model (the EM algorithm), scored with
the Adjusted Rand Index and normalised mutual information.


## How to run

```bash
# 1. activate the environment
source ~/myenv/bin/activate

# 2. install anything missing
pip install seaborn transformers

# 3. from the repository root, open and run the notebook
jupyter notebook "Notebook/DataMining&MachineLearning_Coursework_01.ipynb"
```

Or execute it end to end without opening a browser:

```bash
jupyter nbconvert --to notebook --execute --inplace \
  --ExecutePreprocessor.timeout=1800 \
  "Notebook/DataMining&MachineLearning_Coursework_01.ipynb"
```

The notebook finds the dataset by walking up from its own working directory until it
reaches `Datasets/`. It therefore runs from the repository root and from the `Notebook`
folder without a change to any path.

A full run on a laptop processor takes roughly five minutes. The BERT encoding of
24,000 URLs is the slowest step.

## Results at a glance

All figures below come from the executable notebook on a stratified 24,000-row sample
(16,800 train / 7,200 test), with the seventeen features the notebook selects.

| Model | Accuracy | F1 |
|---|---|---|
| Random Forest | 0.9986 | 0.9986 |
| Gradient Boosting | 0.9978 | 0.9978 |
| Multi layer perceptron | 0.9968 | 0.9968 |
| Decision Tree | 0.9954 | 0.9954 |
| Logistic Regression | 0.9947 | 0.9947 |
| Gaussian Naive Bayes | 0.9928 | 0.9928 |
| Perceptron | 0.9926 | 0.9926 |
| k Nearest Neighbours | 0.9896 | 0.9896 |
| BERT with a small head | 0.9626 | 0.9630 |

Unsupervised: K-Means matches the two classes with ARI 0.869, the Gaussian mixture (EM)
with ARI 0.963.

Two findings are worth stating up front. First, three supplied columns compare the URL with
the brand's official URL or title, so they come close to encoding the label. The notebook
removes those three before modelling and explains the reason in Step 7. Second, the frozen
two layer BERT embedding is the weakest model in the notebook. The page features carry more
information than the whole address string, which is the main result of the neural section.

## Repository layout

```
DMML-CourseWork01/
├── Notebook/
│   └── DataMining&MachineLearning_Coursework_01.ipynb   the whole implementation
├── Datasets/
│   └── PhiUSIIL_Phishing_URL_Dataset.csv                the raw dataset
├── Guide/                                               brief and submission rules (not tracked)
└── README.md
```

## Notes and limitations

* Models are trained on a stratified sample of 24,000 rows rather than the full
  235,370, so that the notebook runs end to end on a laptop in a few minutes. The
  conclusions about which feature families matter are unaffected; the absolute
  scores would move by a fraction of a percentage point on the full data.
* All examples come from a single collection period, so no temporal split is
  possible. A model trained on this data would decay as phishing campaigns change.
* The BERT weights are frozen and used as a feature extractor. Only the small
  classifier head on top is trained.

## Generative AI disclosure

Code in this repository was produced with the assistance of a generative AI tool,
in line with Framework Statement 6 of the coursework's generative AI policy. All
code was executed, and its output was reviewed and interpreted by the author.
