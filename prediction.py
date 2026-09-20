import numpy as np
import pandas as pd


def make_prediction(bundle, values):
    row = pd.DataFrame([values], columns=bundle["features"])
    prediction = float(bundle["model"].predict(row)[0])
    if not np.isfinite(prediction):
        raise ValueError("The model returned a non-finite prediction.")
    return max(prediction, 0.0)
