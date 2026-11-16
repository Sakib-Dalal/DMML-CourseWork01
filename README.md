# Trust or trick? Detecting fraudulent and scam websites from URL and page signals

**F21DL Data Mining and Machine Learning, Group Coursework, 2026/27**

**Coursework topic:** Topic 11, predict whether a website is fraudulent or a scam. The brief marks
this topic as advanced, which means a group should confirm it with the teaching team in the lab
before committing to it.

| | |
|---|---|
| Repository | https://github.com/Sakib-Dalal/DMML-CourseWork01 |
| Notebook | [Notebook/DataMining&MachineLearning_Coursework_01.ipynb](Notebook/DataMining&MachineLearning_Coursework_01.ipynb) |
| Demo app | [GUI/](GUI/) |

## Group

| Name | Matriculation number | Contribution |
|---|---|---|
| To be completed | H | |
| To be completed | H | |
| To be completed | H | |
| To be completed | H | |
| To be completed | H | |

The contribution column is filled in from the peer assessment form at the end of the project.

## 1. What the project is

A phishing website is a fake page built to look like a real one, so that a person types a password
or a card number into it. A security team cannot check every website by hand, so we build models
that read a website and decide whether it is legitimate or a scam.

The dataset gives two kinds of evidence for each website: numbers about the address itself, and
numbers about the page behind it. The project asks which kind carries the signal.

The research questions are:

1. How well can a model tell fake websites from real ones?
2. Which features are useful, the ones about the URL or the ones about the page?
3. Do the groups that an unsupervised algorithm finds match the real classes?
4. Does a neural network do better than the classical models?

## 2. Coursework requirements

| Requirement | Where it is answered | What is there |
|---|---|---|
| **R1** Topic, direction and questions | Notebook, Step 1 | Questions, objectives and four hypotheses |
| **R2** Data analysis and exploration | Notebook, Steps 3 to 9 | Cleaning with a reason for each change, three EDA graphs, feature selection with two methods, K-Means and EM with three metrics |
| **R3** Baseline models and evaluation | Notebook, Steps 10 and 11 | Seven classical algorithms, four metrics, and a discussion of decision trees |
| **R4** Neural networks | Notebook, Steps 12 and 13 | Multi layer perceptron tuned over four shapes, a one dimensional CNN, and a comparison against every classical model |

Section 2 of the brief also asks for both generative and discriminative models. Gaussian naive
Bayes and the Gaussian mixture are generative, and the other six models are discriminative.

## 3. Dataset

**PhiUSIIL Phishing URL Dataset**, from the UCI Machine Learning Repository.

| Field | Value |
|---|---|
| Source | https://archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+dataset |
| Rows in the file | 235,795, with 56 columns |
| Rows we use | 235,370, after removing 425 duplicate URLs |
| Classes | 134,850 legitimate, 100,520 phishing |
| Features | The raw `URL` string plus 51 numeric features from the URL and the page source |
| Licence | CC BY 4.0 |
| Citation | Prasad and Chandra (2024), see the references below |

One dataset is used. The brief allows between one and three, and says that one may be enough.

The file is stored at `Datasets/PhiUSIIL_Phishing_URL_Dataset.csv`. If it is missing, it can be
downloaded again:

```bash
cd Datasets
curl -O "https://archive.ics.uci.edu/static/public/967/phiusiil+phishing+url+dataset.zip"
unzip phiusiil+phishing+url+dataset.zip
```

The thesis of this dataset is that a fake page can be recognised from measurements of its
structure. Three of the supplied columns, `URLSimilarityIndex`, `URLTitleMatchScore` and
`DomainTitleMatchScore`, compare the URL against the official URL or title of the brand. Those
three come close to restating the label, so the notebook removes them before modelling and explains
the reason in Step 7.

## 4. Repository layout

```
DMML-CourseWork01/
├── Notebook/
│   └── DataMining&MachineLearning_Coursework_01.ipynb   all of the code for R1 to R4
├── Datasets/
│   └── PhiUSIIL_Phishing_URL_Dataset.csv                the raw dataset
├── Model/                                               written by the notebook
├── GUI/                                                 Streamlit demo app
├── url_features.py                                      shared address measurement code
├── .streamlit/config.toml                               light theme for the demo
├── Guide/                                               brief and submission rules, not tracked
└── README.md
```

## 5. How to run

Python 3.11 or newer is needed. The work was tested on Python 3.14.

### 5.1 Make a virtual environment

The brief recommends conda or uv. A plain virtual environment works too, and it needs nothing
beyond Python itself.

The interpreter has to be Python 3.11 or newer. On this machine the default `python3` is older than
that, so the working interpreter `/opt/homebrew/bin/python3.14` is named in the command:

```bash
cd DMML-CourseWork01
/opt/homebrew/bin/python3.14 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

On another machine, use whichever Python 3.11 or newer is installed:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows the middle line is different:

```bash
.venv\Scripts\activate
```

The environment is activated again in each new terminal with `source .venv/bin/activate`. Leaving
it takes the word `deactivate`.

The environment folder is not stored in this repository, and it should not be, because it holds
absolute paths and compiled libraries that belong to one machine. `requirements.txt` is the part
that travels: it rebuilds the same set of libraries on any machine in a few minutes. A marker
therefore clones the repository, runs the four commands above, and starts the notebook. Nothing
else has to be sent over.

The work was developed in a virtual environment at `~/myenv`, which can be used instead of a new
one:

```bash
source ~/myenv/bin/activate
```

`requirements.txt` gives a minimum version for each library rather than an exact pin, so the
install does not fail when a machine has a slightly different Python. The versions the results
below were produced with are written at the bottom of that file. It covers four groups: the data
libraries, the graph libraries, torch for the CNN, and streamlit for the demo.

This recipe was tested on a clean environment. A fresh virtual environment made with the four
commands above installed numpy 2.5.3, pandas 3.0.6, scikit-learn 1.9.1, torch 2.14.1 and streamlit
1.66.0, and the notebook run inside it wrote a `model_scores.csv` identical to the one in `Model/`.
So the repository runs on a second machine from `requirements.txt` alone.

### 5.2 Run the notebook

```bash
jupyter notebook "Notebook/DataMining&MachineLearning_Coursework_01.ipynb"
```

Or run it end to end without opening a browser:

```bash
jupyter nbconvert --to notebook --execute --inplace \
  --ExecutePreprocessor.timeout=1800 \
  "Notebook/DataMining&MachineLearning_Coursework_01.ipynb"
```

The notebook finds the dataset by walking up from its own working directory until it reaches
`Datasets/`, so it runs from the repository root and from the `Notebook` folder without a change to
any path.

A full run takes about 90 seconds on a laptop processor, and the CNN training is the slowest step.
Every result in this README comes from that run. It also writes the model files into `Model/`.

### 5.3 Run the demo

The demo needs the `Model` folder, so run the notebook first.

```bash
streamlit run GUI/app.py
```

It opens at http://localhost:8501. For a machine that only needs the app, `GUI/requirements.txt`
lists the five libraries the app imports, at the versions it was tested with.

## 6. Results

All nine models were tested on the same 70,611 rows, using the seventeen features the notebook
selects. Accuracy and F1 are shown because the classes are 57 and 43 percent, so accuracy alone
would flatter a lazy model.

| Model | Accuracy | F1 |
|---|---|---|
| Multi layer perceptron | 0.9996 | 0.9997 |
| Random Forest | 0.9995 | 0.9996 |
| Gradient Boosting | 0.9993 | 0.9994 |
| One dimensional CNN | 0.9991 | 0.9992 |
| Decision Tree | 0.9986 | 0.9988 |
| Logistic Regression | 0.9984 | 0.9986 |
| k Nearest Neighbours | 0.9978 | 0.9981 |
| Perceptron | 0.9974 | 0.9977 |
| Gaussian Naive Bayes | 0.9944 | 0.9951 |

Clustering recovers the two classes far better than we expected: K-Means reaches an adjusted Rand
index of 0.892 and the Gaussian mixture 0.985.

Three things follow from the numbers.

The task is close to separable in this dataset. Every model passes 99 percent accuracy, and the top
seven sit within 0.002 of each other, so the choice of model mattered less than the choice of
features.

The page features carry the signal. Page size, the counts of internal and external references, and
the flags for social links, copyright and description all rank above the features of the address.
URL length is much weaker than common advice suggests.

The address alone is still informative. A second model that reads only the URL string reaches F1
0.9959, which is why the demo can answer for a typed address without fetching the page.

## 7. Interactive demo

`GUI/` holds a small Streamlit app that loads the saved models and lets you test them.

```bash
source ~/myenv/bin/activate
pip install -r GUI/requirements.txt
streamlit run GUI/app.py
```

It opens at http://localhost:8501. There are two ways in: one of twelve stored websites, or any
address you type. `.streamlit/config.toml` keeps the page on a white background, so start the app
from the repository root. Full detail is in [GUI/README.md](GUI/README.md).

## 8. Saved models

Steps 13.2 and 13.3 of the notebook write seven files to `Model/`. Running the notebook again
overwrites them, so the folder can be deleted at any time and rebuilt in about 90 seconds.

| File | Contents |
|---|---|
| `best_model_multi_layer_perceptron.joblib` | The model with the highest F1. The file name carries the model name |
| `scaler.joblib` | The scaler fitted on the training rows. Any new row must pass through it first |
| `features.joblib` | The seventeen feature names, in the order the model expects |
| `cnn_weights.pt` | The weights of the one dimensional CNN, stored with torch |
| `url_model_random_forest.joblib` | The smaller model that reads only the address, used by the demo |
| `url_features.joblib` | The fifteen address measurements that model expects |
| `model_scores.csv` | Accuracy, precision, recall and F1 for all nine models |

The scaler is saved next to the model on purpose. A model trained on scaled inputs gives wrong
answers if it is fed raw values, and that mistake is easy to make months later. The notebook loads
the model back and scores it again, so the stored file is proven to work rather than merely written.

## 9. Limitations

1. One collection period. Every row comes from the same effort, so a model trained on it decays as
   phishing campaigns change. The right test for deployment is a temporal split, which this dataset
   cannot support well.
2. Label noise. Whether a website counts as legitimate is the judgement of the dataset creator.
   Look alike sites that are harmless, and real sites with poor practice, both blur the boundary.
3. Page measurements are the strong ones. They require fetching the page, so a filter that must
   answer before any fetch will be weaker than the scores above suggest.
4. No fit for a CNN on images. This topic has no image data, so the convolution is applied to the
   sequence of features instead. Section 12.4 of the notebook explains the choice.
5. Demo only. The demo is a coursework artefact, not a security product. It should not be pointed at
   traffic, and its answer is not evidence about any real website.

## 10. Ethics and data use

The dataset is public and is used under CC BY 4.0. It holds website addresses and measurements taken
from pages. It does not hold personal data about people, and it was collected by its authors, not by
us. We did not scan any website ourselves, and the demo does not fetch or store pages. The dataset is
cited in section 3 and in the references, as the licence requires.

## 11. Generative AI disclosure

Code in this repository was produced with the help of a generative AI tool, in line with Framework
Statement 6 of the coursework policy. The full prompt used is recorded in the last cell of the
notebook, as the brief requires. All code was executed, and every result in this repository came
from that execution rather than from the tool's description of it.

## 12. References

1. Prasad, A. and Chandra, S. (2024) PhiUSIIL: A diverse security profile empowered phishing URL
   detection framework based on similarity index and incremental learning. Computers and Security,
   136, 103545. Dataset: UCI Machine Learning Repository, ID 967, CC BY 4.0.
   https://archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+dataset
2. Pedregosa, F. et al. (2011) Scikit-learn: Machine Learning in Python. Journal of Machine Learning
   Research, 12, pp. 2825-2830.
