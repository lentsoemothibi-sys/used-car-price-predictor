# Used Car Price Predictor

This Streamlit application predicts the selling price of a used car in Indian rupees.

## Run locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

The trained `used_car_price_model.joblib` file must remain in the same folder as `streamlit_app.py`.

## Deploy with GitHub and Streamlit Community Cloud

1. Create a new public GitHub repository.
2. Upload `streamlit_app.py`, `prediction.py`, `used_car_price_model.joblib`, `requirements.txt`, and `README.md` to its root.
3. Sign in to https://share.streamlit.io with GitHub.
4. Choose **Create app**, select the repository and branch, and set the main file to `streamlit_app.py`.
5. Select **Deploy**, wait for the build to finish, and test a prediction.

The dataset and training script are included for reproducibility but are not required for the deployed app.
