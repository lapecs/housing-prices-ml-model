import streamlit as st
import pandas as pd
import requests

# FastAPI backend URL, used to send requests from Steamlit to FastAPI for model predictions
FASTAPI_URL = "http://127.0.0.1:8000"

st.title("🏠 House Price Prediction")

# Tabs for separating sections into single and batch predictions to improve layout
tab1, tab2 = st.tabs(["🔍 Single Prediction", "📁 Batch Prediction"])

# === Single Input Prediction ===
with tab1:
    # Users can manually enter house feature values
    st.subheader("🏡 Single Input Prediction")
    
    with st.form("Enter House Details"):
        col1, col2, col3 = st.columns(3)
    
        with col1:
            bedrooms = st.number_input("Bedrooms", min_value=0, step=1, format="%d")
            bathrooms = st.number_input("Bathrooms", min_value=0.0, step=0.5, format="%.1f")
            sqft_living = st.number_input("Living Area (sqft)", min_value=0, step=1, format="%d")
            sqft_lot = st.number_input("Lot Size (sqft)", min_value=0, step=1, format="%d")
            floors = st.number_input("Floors", min_value=0.0, step=0.5, format="%.1f")
            waterfront = st.selectbox("Waterfront?", options=[0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    
        with col2:
            view = st.slider("View Score", 0, 4)
            condition = st.slider("Condition (1=Poor to 5=Excellent)", 1, 5)
            grade = st.slider("Grade (1=Poor to 13=Excellent)", 1, 13)
            sqft_above = st.number_input("Above Ground Living (sqft)", min_value=0, step=1, format="%d")
            sqft_basement = st.number_input("Basement Area (sqft)", min_value=0, step=1, format="%d")
    
        with col3:
            yr_built = st.number_input("Year Built", min_value=1800, max_value=2025, format="%d")
            yr_renovated = st.number_input("Year Renovated (0 if never)", min_value=0, max_value=2025, format="%d")
            zipcode = st.number_input("Zipcode", min_value=0, format="%d")
            lat = st.number_input("Latitude", format="%.6f")
            long = st.number_input("Longitude", format="%.6f")
            sqft_living15 = st.number_input("Avg Living Area of Neighbors (sqft)", min_value=0, step=1, format="%d")
            sqft_lot15 = st.number_input("Avg Lot Size of Neighbors (sqft)", min_value=0, step=1, format="%d")

        submit = st.form_submit_button("Predict House Price")

    if submit:
        # This button triggers a request to FastAPI's /predict endpoint.
        input_data = {
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "sqft_living": sqft_living,
            "sqft_lot": sqft_lot,
            "floors": floors,
            "waterfront": waterfront,
            "view": view,
            "condition": condition,
            "grade": grade,
            "sqft_above": sqft_above,
            "sqft_basement": sqft_basement,
            "yr_built": yr_built,
            "yr_renovated": yr_renovated,
            "zipcode": zipcode,
            "lat": lat,
            "long": long,
            "sqft_living15": sqft_living15,
            "sqft_lot15": sqft_lot15
        }

        response = requests.post(f"{FASTAPI_URL}/predict_single", json=input_data)
        # The response is displayed on the Streamlit UI.
        if response.status_code == 200:
            prediction = response.json()["predicted_price"]
            # prediction = response.json()["predicted_price"][0]
            st.success(f"💰 Predicted House Price: ${prediction:,.2f}")
        else:
            st.error("❌ Error fetching prediction. Check FastAPI logs.")

# === Batch Prediction with File Upload Tab ===
with tab2:
    # Users can upload a CSV file containing multiple rows of input data.
    st.subheader("Upload CSV file for Batch Predictions")
    
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("Uploaded Data Preview:", df.head())
    
        # The file is sent to the FastAPI /predict_batch endpoint.
        if st.button("Get Batch Predictions"):
            files = {"file": uploaded_file.getvalue()}
            response = requests.post(f"{FASTAPI_URL}/predict_batch", files=files)
    
            #Predictions are added to the dataset and displayed on the UI.
            if response.status_code == 200:
                predictions = response.json()["predictions"]
                df["Predicted House Price"] = predictions
                st.subheader("✅ Predictions:")
                st.write(df)
            else:
                st.error("❌ Error processing batch prediction.")