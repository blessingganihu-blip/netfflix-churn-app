import streamlit as st
import pickle
import pandas as pd

# load model and columns
with open('churn_model.pkl', 'rb') as f:
    model = pickle.load(f)





# input fields
age = st.number_input("Age", min_value=18, max_value=70, value=30)
subscription_type = st.selectbox("Subscription Type", ["Basic", "Standard", "Premium"])
watch_hours = st.number_input("Total Watch Hours", min_value=0.0, value=50.0)
last_login_days = st.number_input("Days Since Last Login", min_value=0, value=10)
monthly_fee = st.selectbox("Monthly Fee ($)", [8.99, 13.99, 17.99])
number_of_profiles = st.number_input("Number of Profiles", min_value=1, max_value=10, value=1)
avg_watch_time_per_day = st.number_input("Avg Watch Time Per Day (hours)", min_value=0.0, max_value=24.0, value=1.5)
gender = st.selectbox("Gender", ["Male", "Female", "Other"])
region = st.selectbox("Region", ["Africa", "Asia", "Europe", "North America", "Oceania", "South America"])
device = st.selectbox("Device", ["Laptop", "Mobile", "TV", "Tablet"])
payment_method = st.selectbox("Payment Method", ["Credit Card", "Crypto", "Debit Card", "Gift Card", "PayPal"])
favorite_genre = st.selectbox("Favorite Genre", ["Action", "Comedy", "Documentary", "Drama", "Horror", "Romance", "Sci-Fi"])

# predict button
if st.button("Predict Churn"):
    input_data = pd.DataFrame([{
        "age": age,
        "subscription_type": subscription_type,
        "watch_hours": watch_hours,
        "last_login_days": last_login_days,
        "monthly_fee": monthly_fee,
        "number_of_profiles": number_of_profiles,
        "avg_watch_time_per_day": avg_watch_time_per_day,
        "gender": gender,
        "region": region,
        "device": device,
        "payment_method": payment_method,
        "favorite_genre": favorite_genre
    }])

    # encode to match training columns
    input_encoded = pd.get_dummies(input_data)
    input_encoded = input_encoded.reindex(columns=model_columns, fill_value=0)

    prediction = model.predict(input_encoded)[0]
    probability = model.predict_proba(input_encoded)[0][1]

    if prediction == 1:
        st.error(f"⚠️ This customer is likely to churn — {probability:.0%} probability")
    else:
        st.success(f"✅ This customer is likely to stay — {1 - probability:.0%} probability")
