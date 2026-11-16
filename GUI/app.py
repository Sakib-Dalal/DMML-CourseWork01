"""A small Streamlit front end for the phishing website model.

Run it from the project root with:

    streamlit run GUI/app.py

The app loads the saved model from the Model folder, so the notebook must have been
run at least once before the app is started.
"""

from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
MODEL_FOLDER = ROOT / "Model"
EXAMPLE_FILE = ROOT / "GUI" / "examples.csv"
SCORE_FILE = MODEL_FOLDER / "model_scores.csv"

st.set_page_config(page_title="Phishing website detector", page_icon="🔎", layout="wide")


@st.cache_resource
def load_model():
    """Load the best saved model, the scaler and the feature order."""
    model_files = sorted(MODEL_FOLDER.glob("best_model_*.joblib"))
    if not model_files:
        raise FileNotFoundError(
            "No saved model found. Run the notebook first, or run: "
            "jupyter nbconvert --execute Notebook/DataMining&MachineLearning_Coursework_01.ipynb"
        )

    model_file = model_files[0]
    model = joblib.load(model_file)
    scaler = joblib.load(MODEL_FOLDER / "scaler.joblib")
    features = joblib.load(MODEL_FOLDER / "features.joblib")
    return model, scaler, features, model_file.name


@st.cache_data
def load_examples():
    return pd.read_csv(EXAMPLE_FILE)


@st.cache_data
def load_scores():
    if SCORE_FILE.exists():
        return pd.read_csv(SCORE_FILE)
    return None


def model_name_from_file(file_name):
    """best_model_multi_layer_perceptron.joblib -> multi layer perceptron"""
    cleaned = file_name.replace("best_model_", "").replace(".joblib", "")
    return cleaned.replace("_", " ")


def predict(model, scaler, features, values):
    row = pd.DataFrame([values])[features]
    scaled = scaler.transform(row)
    prediction = int(model.predict(scaled)[0])

    probability = None
    if hasattr(model, "predict_proba"):
        probability = float(model.predict_proba(scaled)[0][1])

    return prediction, probability


st.title("Phishing website detector")
st.write(
    "This app uses the model trained in the coursework notebook to decide whether a website is "
    "a phishing page or a legitimate one. Pick an example below, change any of its measurements, "
    "and press the button."
)

model = None
scaler = None
features = []
model_file_name = ""

try:
    model, scaler, features, model_file_name = load_model()
except FileNotFoundError as error:
    st.error(str(error))
    st.info(
        "The model is written by the notebook, so run the notebook once, then reload this page."
    )
    st.stop()

examples = load_examples()
scores = load_scores()

with st.sidebar:
    st.header("About the model")
    st.write("Model in use: **" + model_name_from_file(model_file_name) + "**")
    st.write("File: `" + model_file_name + "`")
    st.write("Features: " + str(len(features)))

    if scores is not None:
        st.subheader("Scores of every model")
        st.dataframe(scores.set_index("Model").round(4), height=330)

    st.caption(
        "The model reads measurements taken from the page, such as the amount of code and the "
        "number of outside references. It does not read the URL text."
    )

st.subheader("1. Choose an example")
choice_labels = []
for position, row in examples.iterrows():
    choice_labels.append(f"{row['True label']}: {row['URL']}")

choice = st.selectbox("Example website", choice_labels, label_visibility="collapsed")
example = examples.loc[choice_labels.index(choice)]

st.subheader("2. Look at the measurements")
st.caption("The true label comes from the dataset. The other columns are what the model reads.")

feature_values = {}
columns = st.columns(2)
half = (len(features) + 1) // 2

for index, feature in enumerate(features):
    container = columns[0] if index < half else columns[1]
    default = float(example[feature])
    step = 0.01 if abs(default) < 5 else 1.0
    feature_values[feature] = container.number_input(
        feature, value=default, step=step, format="%.4f"
    )

st.subheader("3. Run the model")

left, right = st.columns([1, 2])
run = left.button("Predict", type="primary", use_container_width=True)

if run:
    prediction, probability = predict(model, scaler, features, feature_values)
    predicted_label = "Legitimate" if prediction == 1 else "Phishing"
    true_label = example["True label"]

    if predicted_label == "Legitimate":
        right.success("Prediction: legitimate website")
    else:
        right.error("Prediction: phishing website")

    if probability is not None:
        if probability < 0.0001:
            shown = "less than 0.01%"
        elif probability > 0.9999:
            shown = "more than 99.99%"
        else:
            shown = f"{probability:.2%}"
        right.write("Chance of being legitimate: **" + shown + "**")
        right.progress(min(max(probability, 0.0), 1.0))

    if predicted_label == true_label:
        right.info("This matches the label in the dataset: " + true_label + ".")
    else:
        right.warning(
            "This differs from the label in the dataset, which is " + true_label + "."
        )

with st.expander("What the seventeen features mean"):
    st.write(
        "Each feature is a number taken from the website. Twelve of them describe the page behind "
        "the URL: the amount of code, the images, the scripts, the links to its own pages and to "
        "other sites, and whether it has a copyright line, a description, a submit button, a "
        "favicon, hidden fields and social links. Four describe the address: whether it uses "
        "HTTPS, how many symbols it holds, how many digits it holds, and the share of letters. "
        "The last one says whether the page answered at all."
    )

with st.expander("Where these numbers come from"):
    st.write(
        "The examples are real rows from the PhiUSIIL Phishing URL Dataset, taken from the UCI "
        "Machine Learning Repository and used under CC BY 4.0. Twelve rows are stored in "
        "`GUI/examples.csv`, six of each class."
    )
