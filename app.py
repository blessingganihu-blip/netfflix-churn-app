import streamlit as st
import pickle
import pandas as pd

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Netflix Customer Churn Predictor",
    page_icon="🎬",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------
.section-card {
    background-color: #111827;
    padding: 25px;
    border-radius: 15px;
    border: 1px solid #374151;
    margin-bottom: 25px;
}

st.markdown("""
<style>

.stApp {
    background-color: #0B1020;
}

.main .block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.hero-title {
    text-align: center;
    color: white;
    font-size: 3rem;
    font-weight: 800;
    margin-bottom: 0;
}

.hero-subtitle {
    text-align: center;
    color: #9CA3AF;
    font-size: 1.1rem;
    margin-bottom: 2rem;
}

.section-card {
    background-color: #111827;
    padding: 25px;
    border-radius: 15px;
    border: 1px solid #374151;
    margin-bottom: 25px;
}

.section-title {
    color: white;
    font-size: 1.6rem;
    font-weight: 700;
    margin-bottom: 20px;
    border-bottom: 2px solid #E50914;
    padding-bottom: 10px;
}

.stButton > button {
    width: 100%;
    background-color: #E50914;
    color: white;
    font-size: 18px;
    font-weight: bold;
    border-radius: 10px;
    height: 55px;
    border: none;
}

.stButton > button:hover {
    background-color: #B20710;
}

.result-box {
    background-color: #111827;
    padding: 25px;
    border-radius: 15px;
    border: 1px solid #374151;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------
with open("churn_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("model_columns.pkl", "rb") as f:
    model_columns = pickle.load(f)

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown(
    """
    <h1 class='hero-title'>🎬 Netflix Customer Churn Predictor</h1>
    <p class='hero-subtitle'>
        Predict whether a customer is likely to churn based on subscription,
        engagement and viewing behaviour.
    </p>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# CUSTOMER ACTIVITY
# --------------------------------------------------
st.markdown("<div class='section-card'>", unsafe_allow_html=True)
st.markdown(
    "<div class='section-title'>📚 Customer Activity</div>",
    unsafe_allow_html=True
)

left, right = st.columns(2)

with left:
    age = st.number_input(
        "Age",
        min_value=18,
        max_value=70,
        value=30
    )

    watch_hours = st.number_input(
        "Total Watch Hours",
        min_value=0.0,
        value=50.0
    )

    last_login_days = st.number_input(
        "Days Since Last Login",
        min_value=0,
        value=10
    )

with right:
    monthly_fee = st.selectbox(
        "Monthly Fee ($)",
        [8.99, 13.99, 17.99]
    )

    number_of_profiles = st.number_input(
        "Number of Profiles",
        min_value=1,
        max_value=10,
        value=1
    )

    avg_watch_time_per_day = st.number_input(
        "Avg Watch Time Per Day (hours)",
        min_value=0.0,
        max_value=24.0,
        value=1.5
    )

st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# SUBSCRIPTION DETAILS
# --------------------------------------------------
st.markdown("<div class='section-card'>", unsafe_allow_html=True)
st.markdown(
    "<div class='section-title'>💳 Subscription Details</div>",
    unsafe_allow_html=True
)

left, right = st.columns(2)

with left:
    subscription_type = st.selectbox(
        "Subscription Type",
        ["Basic", "Standard", "Premium"]
    )

    payment_method = st.selectbox(
        "Payment Method",
        ["Credit Card", "Crypto", "Debit Card", "Gift Card", "PayPal"]
    )

with right:
    device = st.selectbox(
        "Device",
        ["Laptop", "Mobile", "TV", "Tablet"]
    )

    region = st.selectbox(
        "Region",
        [
            "Africa",
            "Asia",
            "Europe",
            "North America",
            "Oceania",
            "South America"
        ]
    )

st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# PREFERENCES
# --------------------------------------------------
st.markdown("<div class='section-card'>", unsafe_allow_html=True)
st.markdown(
    "<div class='section-title'>🎭 Preferences</div>",
    unsafe_allow_html=True
)

left, right = st.columns(2)

with left:
    gender = st.selectbox(
        "Gender",
        ["Male", "Female", "Other"]
    )

with right:
    favorite_genre = st.selectbox(
        "Favorite Genre",
        [
            "Action",
            "Comedy",
            "Documentary",
            "Drama",
            "Horror",
            "Romance",
            "Sci-Fi"
        ]
    )

st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# PREDICT BUTTON
# --------------------------------------------------
if st.button("🔮 Predict Churn"):

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

    input_encoded = pd.get_dummies(input_data)
    input_encoded = input_encoded.reindex(
        columns=model_columns,
        fill_value=0
    )

    prediction = model.predict(input_encoded)[0]
    probability = model.predict_proba(input_encoded)[0][1]

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<div class='result-box'>", unsafe_allow_html=True)

    if prediction == 1:
        st.markdown(
            "<h2 style='color:#EF4444;'>⚠️ High Churn Risk</h2>",
            unsafe_allow_html=True
        )

        st.metric(
            "Churn Probability",
            f"{probability:.1%}"
        )

        st.progress(float(probability))

    else:
        st.markdown(
            "<h2 style='color:#22C55E;'>✅ Likely to Stay</h2>",
            unsafe_allow_html=True
        )

        st.metric(
            "Retention Probability",
            f"{1 - probability:.1%}"
        )

        st.progress(float(1 - probability))

    st.markdown("</div>", unsafe_allow_html=True)
