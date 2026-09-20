from pathlib import Path

import joblib
import streamlit as st

from prediction import make_prediction


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "used_car_price_model.joblib"

st.set_page_config(page_title="Used Car Price Predictor", page_icon="🚗", layout="centered")


@st.cache_resource
def load_bundle():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "used_car_price_model.joblib is missing. Run train_model.py first."
        )
    loaded = joblib.load(MODEL_PATH)
    required = {"model", "features", "brands", "models_by_brand"}
    if not isinstance(loaded, dict) or not required.issubset(loaded):
        raise ValueError("The model bundle is incomplete or incompatible.")
    return loaded


st.title("🚗 Used Car Price Predictor")
st.caption("Estimate a used car's selling price from its specifications.")

try:
    bundle = load_bundle()
except Exception as exc:
    st.error(f"The prediction model could not be loaded: {exc}")
    st.stop()

with st.form("prediction_form"):
    brand = st.selectbox("Brand", bundle["brands"])
    model = st.selectbox("Model", bundle["models_by_brand"][brand])

    left, right = st.columns(2)
    with left:
        vehicle_age = st.number_input("Vehicle age (years)", 0, 25, 5, 1)
        km_driven = st.number_input("Kilometres driven", 100, 500_000, 50_000, 1_000)
        mileage = st.number_input("Mileage (km/l)", 4.0, 40.0, 18.0, 0.1)
        seller_type = st.selectbox("Seller type", bundle["seller_types"])
    with right:
        engine = st.number_input("Engine capacity (cc)", 600, 7000, 1500, 50)
        max_power = st.number_input("Maximum power (bhp)", 30.0, 700.0, 100.0, 1.0)
        seats = st.number_input("Number of seats", 2, 9, 5, 1)
        fuel_type = st.selectbox("Fuel type", bundle["fuel_types"])

    transmission_type = st.selectbox(
        "Transmission type", bundle["transmission_types"]
    )
    submitted = st.form_submit_button("Predict selling price", type="primary")

if submitted:
    values = {
        "brand": brand,
        "model": model,
        "vehicle_age": int(vehicle_age),
        "km_driven": int(km_driven),
        "seller_type": seller_type,
        "fuel_type": fuel_type,
        "transmission_type": transmission_type,
        "mileage": float(mileage),
        "engine": int(engine),
        "max_power": float(max_power),
        "seats": int(seats),
    }
    try:
        estimated_price = make_prediction(bundle, values)
        st.success(f"Estimated selling price: ₹{estimated_price:,.0f}")
        st.caption("This estimate is based on historical Indian used-car data and is not a formal valuation.")
    except Exception as exc:
        st.error(f"A prediction could not be produced: {exc}")
