"""A small Streamlit app for the phishing website model.

Run it from the project root:

    streamlit run GUI/app.py

The app reads the saved model from the Model folder, so run the notebook once first.
"""

from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]

st.set_page_config(page_title="Phishing website detector", layout="centered")


@st.cache_resource
def load_model():
    model_files = sorted((ROOT / "Model").glob("best_model_*.joblib"))
    if not model_files:
        return None, None, None

    model = joblib.load(model_files[0])
    scaler = joblib.load(ROOT / "Model" / "scaler.joblib")
    features = joblib.load(ROOT / "Model" / "features.joblib")
    return model, scaler, features


model, scaler, features = load_model()
examples = pd.read_csv(ROOT / "GUI" / "examples.csv")

st.title("Phishing website detector")
st.write(
    "This app uses the model from our coursework notebook. Choose a website and press the button."
)

if model is None:
    st.error("No saved model found in the Model folder. Run the notebook first.")
    st.stop()

choice = st.selectbox("Choose a website", examples["URL"])
row = examples[examples["URL"] == choice].iloc[0]

st.write("This website is labelled **" + row["True label"] + "** in the dataset.")

st.write("The numbers the model reads:")
measurements = row[features].to_frame(name="Value")
measurements.index.name = "Measurement"
st.dataframe(measurements, height=340)

if st.button("Check this website"):
    model, scaler, features = load_model()

    if model is None:
        st.error("No saved model found in the Model folder. Run the notebook first.")
    else:
        new_row = pd.DataFrame([row[features]])
        scaled = scaler.transform(new_row)
        prediction = int(model.predict(scaled)[0])
        probability = float(model.predict_proba(scaled)[0][1])

        if prediction == 1:
            st.success("The model says this is a legitimate website.")
        else:
            st.error("The model says this is a phishing website.")

        st.write("The model gives it a " + f"{probability:.1%}" + " chance of being legitimate.")

st.caption("Data: PhiUSIIL Phishing URL Dataset, UCI Machine Learning Repository, CC BY 4.0.")
