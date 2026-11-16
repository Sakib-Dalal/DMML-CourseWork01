# Interactive demo

A small Streamlit app that uses the model trained in the notebook. Pick one of the twelve stored
examples, change any of its measurements, and the app says whether the website is a phishing page
or a legitimate one.

## Run it

```bash
source ~/myenv/bin/activate
pip install -r GUI/requirements.txt
streamlit run GUI/app.py
```

The app opens at http://localhost:8501.

## What it shows

- The model that is in use, and the file it came from.
- The scores of all nine models, so the demo can be read next to the coursework results.
- A dropdown with twelve real websites, six phishing and six legitimate.
- The seventeen measurements as number inputs. Each one starts at the value of the chosen
  example, and any of them can be changed to see what moves the answer.
- The prediction, the probability, and whether it agrees with the label in the dataset.

## What it needs

`Model/` must exist, because that is where the app reads `best_model_<name>.joblib`,
`scaler.joblib` and `features.joblib`. The notebook writes that folder in Step 13.1, so run the
notebook once before starting the app. If the folder is missing, the app says so instead of
crashing.

## Example data

`examples.csv` holds twelve rows taken from the PhiUSIIL Phishing URL Dataset. Each row keeps the
URL, the true label and the seventeen features, in the same order the model expects. The rows were
chosen with ordinary address lengths between 25 and 55 characters, so that the demo looks like
real traffic instead of two letter domains.

## Files

| File | Purpose |
|---|---|
| `app.py` | The whole app |
| `examples.csv` | Twelve example websites, six of each class |
| `requirements.txt` | Pinned versions that the app was tested with |

The app reads `Model/model_scores.csv` as well, which the notebook writes. Delete that file and
the app still works, but the score table disappears from the sidebar.
