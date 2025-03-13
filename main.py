import os
import streamlit as st
import joblib
import pandas as pd

st.set_page_config(page_title="Rainfall Prediction", layout="wide")

image_path = "./pictures_model/rainfall-removebg-preview.png"

with st.sidebar:
    st.markdown(
        """
        <style>
        .image-container {
            display: flex;
            justify-content: center;
            margin-bottom: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    if os.path.exists(image_path):
        st.image(image_path, width=250)
    else:
        st.warning("⚠️ Image not found. Please check the file path.")

# ✅ Sidebar Navigation
st.sidebar.title("Navigation")

def set_page(page_name):
    st.session_state.page = page_name

if "page" not in st.session_state:
    st.session_state.page = "Home"  # ✅ Default landing page is "Home"

with st.sidebar:
    if st.button("🏠 Home", use_container_width=True, key="home"):
        set_page("Home")
    if st.button("📊 Dataset", use_container_width=True, key="dataset"):
        set_page("Dataset")
    if st.button("📈 Visualization", use_container_width=True, key="visualization"):
        set_page("Visualization")
    if st.button("🤖 Prediction", use_container_width=True, key="prediction"):
        set_page("Prediction")
    if st.button("📉 Model Evaluation", use_container_width=True, key="model_evaluation"):
        set_page("Model Evaluation")
    if st.button("📜 Summary", use_container_width=True, key="summary"):  # ✅ New Sidebar Button
        set_page("Summary")

# ✅ Import Pages
from icons.dataset import show_dataset
from icons.visualization import show_visualization, load_data
from icons.prediction import get_user_input_and_predict
from icons.eval import evaluate_model  
from icons.summary import show_summary  # ✅ New Summary Page Import


# ✅ Load Model
model_path = "pictures_model/RandomForestModel.pkl"
if os.path.exists(model_path):
    model = joblib.load(model_path)
else:
    st.error("⚠️ Model file not found. Please check the path.")

# ✅ Load Scaler

scaler_path = "pictures_model/scaler.pkl"
if os.path.exists(scaler_path):
    scaler = joblib.load(scaler_path)
else:
    st.error("⚠️ Scaler file not found. Please check the path.")

# ✅ Load Encoded Features
encoded_mappings_path = r"pictures_model/encoded_df.pkl"
if os.path.exists(encoded_mappings_path):
    encoded_mappings = joblib.load(encoded_mappings_path)
else:
    st.error("⚠️ Encoded mappings file not found. Please check the path.")

# ✅ Load Dataset (df) for Taking User Input
df_path = "pictures_model/weatherAUS.csv"
if os.path.exists(df_path):
    df = pd.read_csv(df_path)
else:
    st.error("⚠️ Dataset file not found. Please check the path.")
    df = None  # Prevent errors if the file is missing

# ✅ Load Data for Predictions
df1 = load_data()

# ✅ Load Correct Page
if st.session_state.page == "Home":
    st.title("🌧️ Rainfall Prediction")  
    st.markdown(""" 
    ##  **Project Overview** 
    This application helps predict **whether it will rain tomorrow** using historical weather data 
    from **2007 to 2017**.
    ###  **What You Can Do**
    - 📊 **Explore Dataset:** View the dataset used for training. 
    - 📈 **Visualize Data:** Analyze rainfall trends & patterns. 
    - 🤖 **Predict Rainfall:** Input weather details and get AI predictions. 
    - 📉 **Evaluate Model:** Check the accuracy and performance of the model.
    - 📜 **Summary:** Overview of key findings and project insights.

    **👉 Use the sidebar to navigate through different sections!**
    """)
elif st.session_state.page == "Dataset":
    show_dataset()
elif st.session_state.page == "Visualization":
    show_visualization(df1)
elif st.session_state.page == "Prediction":
    if df is not None:
        get_user_input_and_predict(df)
    else:
        st.error("⚠️ Cannot proceed with prediction. Dataset not found.")
elif st.session_state.page == "Model Evaluation":
    evaluate_model()
elif st.session_state.page == "Summary":  # ✅ New Summary Page
    show_summary()
