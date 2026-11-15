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

The whole implementation lives in a single notebook:

```
DataMining&MachineLearning_Coursework_01.ipynb
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
| **R4** Neural network models, trained, tuned and compared | Notebook, Step 12 |

### Models compared

Classical (R3): Gaussian Naive Bayes, Logistic Regression, Perceptron,
k-Nearest Neighbours, Decision Tree, Random Forest, Histogram Gradient Boosting.

Neural (R4): Multi-Layer Perceptron on engineered features, BERT-lite
(`google/bert_uncased_L-2_H-128_A-2`) mean-pooled URL embeddings with an MLP head,
and a character-level 1D CNN trained on the raw URL string.

Unsupervised (R2): K-Means and a Gaussian Mixture Model (the EM algorithm), scored
with silhouette, Adjusted Rand Index and Normalised Mutual Information.

## How to run

```bash
# 1. activate the environment
source ~/myenv/bin/activate

# 2. install anything missing
pip install seaborn transformers

# 3. from the repository root, open and run the notebook
jupyter notebook "DataMining&MachineLearning_Coursework_01.ipynb"
```

Or execute it end to end without opening a browser:

```bash
jupyter nbconvert --to notebook --execute --inplace \
  --ExecutePreprocessor.timeout=1800 \
  "DataMining&MachineLearning_Coursework_01.ipynb"
```

The notebook finds the dataset automatically by walking up from its own working
directory until it reaches `Datasets/`, so it runs from either the repository root
or the `Notebook/` folder.

A full run on a laptop processor takes roughly five minutes. The BERT encoding of
24,000 URLs is the slowest step.

## Results at a glance

All figures below come from the executable notebook on a stratified 24,000-row sample
(16,800 train / 7,200 test), leak-free feature set unless stated.

| Model | Accuracy | F1 | ROC-AUC |
|---|---|---|---|
| Histogram Gradient Boosting | 0.9986 | 0.9986 | 1.0000 |
| Random Forest | 0.9986 | 0.9986 | 1.0000 |
| Multi layer perceptron (17 features) | 0.9976 | 0.9976 | 1.0000 |
| Logistic Regression | 0.9976 | 0.9976 | 1.0000 |
| Character CNN on the URL | 0.9967 | 0.9967 | 0.9984 |
| Perceptron | 0.9958 | 0.9958 | 0.9999 |
| k-Nearest Neighbours | 0.9956 | 0.9956 | 0.9987 |
| Decision Tree | 0.9954 | 0.9954 | 0.9954 |
| Gaussian Naive Bayes | 0.9932 | 0.9932 | 0.9974 |
| BERT with a small head | 0.9626 | 0.9630 | 0.9911 |

Unsupervised: K-Means recovers the two classes with ARI 0.881, the Gaussian mixture
(EM) with ARI 0.915.

Two findings are worth stating up front. First, three supplied columns compare the URL with
the brand's official URL or title, so they come close to encoding the label. The notebook
removes those three before modelling and explains the reason in Step 7. Second, the frozen
two layer BERT embedding is the weakest text representation tested. The character CNN
trained from nothing beats it, which is the main result of the neural network section.

## Repository layout

```
DMML-CourseWork01/
├── DataMining&MachineLearning_Coursework_01.ipynb   the whole implementation
├── Datasets/
│   └── PhiUSIIL_Phishing_URL_Dataset.csv            the raw dataset
├── Guide/                                           coursework brief and submission rules (not tracked)
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
