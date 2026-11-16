# Interactive demo

A small Streamlit app that uses the models trained in the notebook.

There are two ways to use it. Pick one of the twelve stored websites, or type any address you
like. The app says whether the model thinks it is a phishing page or a legitimate one.

## Run it

```bash
source ~/myenv/bin/activate
pip install -r GUI/requirements.txt
streamlit run GUI/app.py
```

The app opens at http://localhost:8501. Start it from the project root, because that is where
`.streamlit/config.toml` lives, and that file keeps the page on a white background.

## Why there are two models

The main model reads seventeen measurements of the page behind the website, such as the amount of
code and the number of outside references. It can only answer for a website that has already been
measured, which is why the twelve stored examples exist.

A page on the live web is not measured the way this dataset was, so feeding guessed values into the
main model gives poor answers. The app therefore uses a second model for a typed address. That one
reads only what can be counted inside the string: length, the domain and its ending, sub domains,
HTTPS, and the counts and shares of letters, digits and symbols.

Both models were trained in the notebook, and the counting function lives in `url_features.py` at
the top of the repository, so the values used in training and the values used in the app come from
the same code.

## What it needs

The `Model` folder, because that is where `best_model_<name>.joblib`, `scaler.joblib`,
`features.joblib`, `url_model_random_forest.joblib` and `url_features.joblib` are read from. The
notebook writes that folder in Steps 13.1 and 13.2, so run the notebook once before starting the
app. If the folder is missing the app says so instead of crashing.

## Example data

`examples.csv` holds twelve rows taken from the PhiUSIIL Phishing URL Dataset. Each row keeps the
URL, the true label and the seventeen page measurements, in the same order the model expects. The
rows were chosen with ordinary address lengths between 25 and 55 characters, so the demo looks like
real traffic instead of two letter domains.

## Files

| File | Purpose |
|---|---|
| `app.py` | The whole app |
| `examples.csv` | Twelve example websites, six of each class |
| `requirements.txt` | Pinned versions that the app was tested with |
