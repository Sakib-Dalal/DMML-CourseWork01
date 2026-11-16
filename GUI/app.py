"""A small Streamlit app for the phishing website model.

Run it from the project root:

    streamlit run GUI/app.py
"""

import sys
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from url_features import features_from_url  # type: ignore[import-not-found]

st.set_page_config(page_title="Phishing website detector", layout="centered")


@st.cache_resource
def load_models():
    model_files = sorted((ROOT / "Model").glob("best_model_*.joblib"))
    if not model_files:
        return None

    model = joblib.load(model_files[0])
    scaler = joblib.load(ROOT / "Model" / "scaler.joblib")
    features = joblib.load(ROOT / "Model" / "features.joblib")
    url_model = joblib.load(ROOT / "Model" / "url_model_random_forest.joblib")
    url_names = joblib.load(ROOT / "Model" / "url_features.joblib")
    return model, scaler, features, url_model, url_names


def show_result(prediction, probability):
    if prediction == 1:
        st.success("The model says this is a legitimate website.")
    else:
        st.error("The model says this is a phishing website.")
    st.write("The model gives it a " + f"{probability:.1%}" + " chance of being legitimate.")


loaded = load_models()
examples = pd.read_csv(ROOT / "GUI" / "examples.csv")

st.title("Phishing website detector")
st.write("This app uses the models from our coursework notebook.")

if loaded is None:
    st.error("No saved model found in the Model folder. Run the notebook first.")
    st.stop()

model, scaler, features, url_model, url_names = loaded

mode = st.radio(
    "Which website?",
    ["One from the dataset", "An address I type"],
    horizontal=True,
)

if mode == "One from the dataset":
    choice = st.selectbox("Choose a website", examples["URL"])
    row = examples[examples["URL"] == choice].iloc[0]

    st.write("This website is labelled **" + row["True label"] + "** in the dataset.")

    st.write("The numbers the model reads:")
    measurements = row[features].to_frame(name="Value")
    measurements.index.name = "Measurement"
    st.dataframe(measurements, height=300)

    if st.button("Check this website"):
        new_row = pd.DataFrame([row[features]])
        scaled = scaler.transform(new_row)
        prediction = int(model.predict(scaled)[0])
        probability = float(model.predict_proba(scaled)[0][1])
        show_result(prediction, probability)

    st.caption(
        "This model reads seventeen measurements of the page, so it can only answer for a "
        "website that has already been measured."
    )

else:
    address = st.text_input("Website address", "https://www.gatwickexpress.com")

    if st.button("Check this website"):
        if not address.startswith("http"):
            address = "https://" + address

        values = features_from_url(address)
        new_row = pd.DataFrame([values])[url_names]
        prediction = int(url_model.predict(new_row)[0])
        probability = float(url_model.predict_proba(new_row)[0][1])

        show_result(prediction, probability)

        st.write("The numbers this model counts in the address:")
        table = pd.DataFrame([values]).T
        table.columns = ["Value"]
        table.index.name = "Measurement"
        st.dataframe(table, height=340)

    st.caption(
        "This one uses a second model that reads only the address, because a page on the live "
        "web is not measured the way the dataset was. It was trained on the addresses in this "
        "dataset, so an unusual address can still come out wrong."
    )

st.caption("Data: PhiUSIIL Phishing URL Dataset, UCI Machine Learning Repository, CC BY 4.0.")
