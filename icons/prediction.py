import numpy as np
import pandas as pd
import streamlit as st
import joblib


<<<<<<< HEAD
import gdown
import os
file_id = '152PyisZggi2W5xum38LNTHapCK59CI6Z'
url = f'https://drive.google.com/uc?id={file_id}'
output_path = 'pictures_model/encoded_df.pkl'
gdown.download(url, output_path, quiet=False)
print(f"File downloaded to: {os.path.abspath(output_path)}")
=======
# import gdown
# import os
# file_id = '152PyisZggi2W5xum38LNTHapCK59CI6Z'
# url = f'https://drive.google.com/uc?id={file_id}'
# output_path = 'pictures_model/encoded_df.pkl'
# gdown.download(url, output_path, quiet=False)
# print(f"File downloaded to: {os.path.abspath(output_path)}")
>>>>>>> 09b8994 (first commit)



scaler = joblib.load("D:/ML_PROJECT/pictures_model/scaler.pkl")
encoded_mappings = joblib.load("D:/ML_PROJECT/pictures_model/encoded_df.pkl")
rf_model_data = joblib.load("D:/ML_PROJECT/pictures_model/RandomForestModel.pkl")
rf_model = rf_model_data["model"]

def get_user_input_and_predict(df):
    if "Date" in df.columns:
        df = df.drop(columns=["Date"])

    categorical_features = ["Location", "WindGustDir", "WindDir9am", "WindDir3pm", "RainToday"]
    numerical_features = [
        "MinTemp", "MaxTemp", "Rainfall", "Evaporation", "Sunshine",
        "WindGustSpeed", "WindSpeed9am", "WindSpeed3pm", "Humidity3pm",
        "Pressure3pm", "Cloud9am", "Cloud3pm", "Temp9am"
    ]

    st.title("🌦️ Rain Prediction(Random Forest)")

    user_input = {}

    # ✅ Categorical Inputs
    for col in categorical_features:
        if col in df.columns:
            unique_values = df[col].dropna().unique().tolist()
            user_input[col] = st.selectbox(f"Select {col}:", unique_values)

    # ✅ Numerical Inputs
    for col in numerical_features:
        if col in df.columns:
            median_value = df[col].median()
            user_input[col] = st.number_input(f"Enter {col}:", value=median_value)

    feature_columns = list(encoded_mappings.columns)
    if "RainTomorrow" in feature_columns:
        feature_columns.remove("RainTomorrow")

    feature_dict = {col: 0 for col in feature_columns}

    # Fill dictionary with numerical values
    for key, value in user_input.items():
        if key in numerical_features:
            feature_dict[key] = value

    # One-hot encode categorical values
    for key in categorical_features:
        one_hot_key = f"{key}_{user_input[key]}"
        if one_hot_key in feature_dict:
            feature_dict[one_hot_key] = 1

    arr_df = pd.DataFrame([feature_dict])
    arr_df = arr_df[scaler.feature_names_in_]  

    # ✅ Predict when button is clicked
    if st.button("☁️ Will it rain tomorrow?"):
        arr_scaled = scaler.transform(arr_df)
        prediction = rf_model.predict(arr_scaled)[0]
        st.success(f"{'Yes' if prediction == 1 else 'No'}")

if __name__ == "__main__":
    df = pd.read_csv("D:/ML_PROJECT/data/rainfall_data.csv")  
    get_user_input_and_predict(df)
