import streamlit as st
import numpy as np
import joblib
from config.paths_config import MODEL_OUTPUT_PATH

# Load model
model = joblib.load(MODEL_OUTPUT_PATH)

# App title
st.title("🏨 Hotel Reservation Cancellation Prediction")

# Form Inputs
with st.form("prediction_form"):
    lead_time = st.number_input("Lead Time", min_value=0)
    no_of_special_request = st.number_input("No. of Special Requests", min_value=0)
    avg_price_per_room = st.number_input("Average Price per Room", min_value=0.0, format="%.2f")
    arrival_month = st.selectbox("Arrival Month", list(range(1, 13)), format_func=lambda x: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][x-1])
    arrival_date = st.selectbox("Arrival Date", list(range(1, 32)))

    market_segment_type = st.selectbox("Market Segment Type", options=[0, 1, 2, 3, 4],
                                       format_func=lambda x: ["Aviation", "Complimentary", "Corporate", "Offline", "Online"][x])

    no_of_week_nights = st.number_input("No. of Week Nights", min_value=0)
    no_of_weekend_nights = st.number_input("No. of Weekend Nights", min_value=0)

    type_of_meal_plan = st.selectbox("Type of Meal Plan", options=[0, 1, 2, 3],
                                     format_func=lambda x: ["Meal Plan 1", "Meal Plan 2", "Meal Plan 3", "Not Selected"][x])

    room_type_reserved = st.selectbox("Room Type Reserved", options=[0, 1, 2, 3, 4, 5, 6],
                                      format_func=lambda x: f"Room Type {x+1}")

    submitted = st.form_submit_button("Predict")

# Prediction
if submitted:
    input_data = np.array([[lead_time, no_of_special_request, avg_price_per_room,
                            arrival_month, arrival_date, market_segment_type,
                            no_of_week_nights, no_of_weekend_nights,
                            type_of_meal_plan, room_type_reserved]])

    prediction = model.predict(input_data)[0]

    if prediction == 0:
        st.error("❌ The customer is likely to **cancel** the reservation.")
    else:
        st.success("✅ The customer is **not likely to cancel** the reservation.")
