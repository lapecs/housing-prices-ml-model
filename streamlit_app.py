import streamlit as st
import pandas as pd
import requests

# FastAPI backend URL, used to send requests from Steamlit
# to FastAPI for model predictions
FASTAPI_URL = "http://127.0.0.1:8000"

st.title("House Price Prediction - ML Model UI")

#################################
# === Single Input Prediction ===
#################################
# Users can manually enter house feature values
st.subheader("Single Input Prediction")
bedrooms = st.number_input("Number of bedrooms")
bathrooms = st.number_input("Number of bathrooms")
sqft_living = st.number_input("Living space in sqft")
sqft_lot = st.number_input("Lot size in sqft")
floors = st.number_input("Number of floors")
waterfront = st.number_input("Is it a waterfront property (0 - No or 1 - Yes)")
view = st.number_input("Number of views of the property")
condition = st.number_input("Condition score of the property (1 - poor to 5 - excellent)")
grade = st.number_input("Grade score of the property (1 - poor to 13 - excellent)")
sqft_above = st.number_input("Living space above ground in sqft")
sqft_basement = st.number_input("Living space below ground in sqft")
yr_built = st.number_input("Year that the house was built")
yr_renovated = st.number_input("Year that the house was renovated")
zipcode = st.number_input("Zipcode of the property")
lat = st.number_input("lattitude of the property")
long = st.number_input("longitude of the property")
sqft_living15 = st.number_input("Avg living space of the 15 closest homes in sqft")
sqft_lot15 = st.number_input("Avg lot size of the 15 closest homes in sqft")


# This button triggers a request to FastAPI's /predict endpoint.
if st.button("Predict House Price"):
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
        st.success(f"Predicted House Price: {prediction:.2f}")
    else:
        st.error("Error fetching prediction. Check FastAPI logs.")

###########################################
# === Batch Prediction with File Upload ===
###########################################
# Users can upload a CSV file containing multiple rows of input data.
st.subheader("Batch Prediction via CSV Upload")
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
            st.subheader("Predictions:")
            st.write(df)
        else:
            st.error("Error processing batch prediction.")