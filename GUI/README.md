# Interactive demo

A small Streamlit app that uses the model trained in the notebook.

Choose one of the twelve stored websites, press the button, and the app says whether the model
thinks it is a phishing page or a legitimate one.

## Run it

```bash
source ~/myenv/bin/activate
pip install -r GUI/requirements.txt
streamlit run GUI/app.py
```

The app opens at http://localhost:8501. Start it from the project root, because that is where
`.streamlit/config.toml` lives, and that file keeps the page on a white background.

## What it shows

- A dropdown with twelve real websites, six phishing and six legitimate.
- The label that the dataset gives to the chosen website.
- The seventeen measurements the model reads, as a small table.
- The prediction and the probability, after you press the button.

## What it needs

The `Model` folder, because that is where `best_model_<name>.joblib`, `scaler.joblib` and
`features.joblib` are read from. The notebook writes that folder in Step 13.1, so run the notebook
once before starting the app. If the folder is missing the app says so instead of crashing.

## Example data

`examples.csv` holds twelve rows taken from the PhiUSIIL Phishing URL Dataset. Each row keeps the
URL, the true label and the seventeen features, in the same order the model expects. The rows were
chosen with ordinary address lengths between 25 and 55 characters, so the demo looks like real
traffic instead of two letter domains.

## Files

| File | Purpose |
|---|---|
| `app.py` | The whole app, about 60 lines |
| `examples.csv` | Twelve example websites, six of each class |
| `requirements.txt` | Pinned versions that the app was tested with |
