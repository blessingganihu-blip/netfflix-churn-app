import streamlit as st
import pickle
import pandas as pd

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Netflix Customer Churn Predictor",
    page_icon="🎬",
    layout="centered"
)

# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>

.stApp {
    background-color: #0B1020;
}

.main .block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.hero-title {
    text-align: center;
    color: white;
    font-size: 3.5rem;
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
    min-height: 380px;
}

.section-title {
    color: white;
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 2px solid #E50914;
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

[data-testid="stMetric"] {
    background-color: #1F2937;
    padding: 10px;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# LOAD MODEL
# ==================================================

with open("churn_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("model_columns.pkl", "rb") as f:
    model_columns = pickle.load(f)

# ==================================================
# HEADER
# ==================================================

st.markdown(
    """
    <h1 class="hero-title">🎬 Netflix Customer Churn Predictor</h1>

    <div style="
        width: 200px;
        height: 4px;
        background-color: #E50914;
        margin: 15px auto 25px auto;
        border-radius: 5px;">
    </div>

    <p class="hero-subtitle">
        Fill in the customer details below to predict whether they are likely to churn.
    </p>
    """,
    unsafe_allow_html=True
)
# ==================================================
# TOP ROW
# ==================================================

col1, col2 = st.columns(2)

with col1:



        st.markdown("""
<div class="section-title">
    👤 Customer Profile
</div>
""", unsafe_allow_html=True)
        age = st.number_input(
            "Age",
            min_value=18,
            max_value=70,
            value=30
        )

        gender = st.selectbox(
            "Gender",
            ["Male", "Female", "Other"]
        )

        favorite_genre = st.selectbox(
            "Favourite Genre",
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


    
with col2:

    st.markdown("""
    <div class="section-title">
        📺 Customer Activity
    </div>
    """, unsafe_allow_html=True)

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

    avg_watch_time_per_day = st.number_input(
        "Avg Watch Hours Per Day",
        min_value=0.0,
        max_value=24.0,
        value=1.5
    )
# ==================================================
# BOTTOM ROW
# ==================================================

col3, col4 = st.columns(2)


with col3:

    st.markdown("""
    <div class="section-title">
        🌍 Location & Device
    </div>
    """, unsafe_allow_html=True)

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

    device = st.selectbox(
        "Device",
        ["Laptop", "Mobile", "TV", "Tablet"]
    )

    number_of_profiles = st.number_input(
        "Number of Profiles",
        min_value=1,
        max_value=10,
        value=1
    )
with col4:
    

   st.markdown("""
<div class="section-title">
    💳 Subscription Details
</div>
""", unsafe_allow_html=True)

        subscription_type = st.selectbox(
            "Subscription Type",
            ["Basic", "Standard", "Premium"]
        )

        payment_method = st.selectbox(
            "Payment Method",
            [
                "Credit Card",
                "Crypto",
                "Debit Card",
                "Gift Card",
                "PayPal"
            ]
        )

        monthly_fee = st.selectbox(
            "Monthly Fee ($)",
            [8.99, 13.99, 17.99]
        )

# ==================================================
# PREDICTION
# ==================================================

left, center, right = st.columns([1, 2, 1])

with center:
    predict = st.button("🔮 Predict Churn")
    
if predict:

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
            "<h2 style='color:#22C55E;'>✅ Likely To Stay</h2>",
            unsafe_allow_html=True
        )

        st.metric(
            "Retention Probability",
            f"{1 - probability:.1%}"
        )

        st.progress(float(1 - probability))

    st.markdown("</div>", unsafe_allow_html=True)
