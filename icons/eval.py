import streamlit as st
import joblib
import os
import pandas as pd

def evaluate_model():
    st.title("📉 Model Evaluation")

    # ✅ Define model paths
    model_paths = {
        "Random Forest": r"pictures_model/RandomForestModel.pkl",
        "XGBoost": r"pictures_model/XGBoostModel.pkl"
    }

    # ✅ Select a model to evaluate
    selected_model = st.radio("Select a Model: ", list(model_paths.keys()))

    # ✅ Load the chosen model
    model_path = model_paths[selected_model]

    if not os.path.exists(model_path):
        st.error(f"⚠️ `{selected_model}` model file not found! Please retrain and save the model.")
        return

    try:
        # ✅ Load the dictionary containing model & accuracy
        model_data = joblib.load(model_path)
    except Exception as e:
        st.error(f"⚠️ Error loading `{selected_model}` model: {str(e)}")
        return

    if not isinstance(model_data, dict) or "model" not in model_data:
        st.error(f"⚠️ `{selected_model}` file format is invalid. Ensure the model is saved correctly.")
        return

    # Extract model details
    model = model_data.get("model", None)
    train_accuracy = model_data.get("train_accuracy", None)
    test_accuracy = model_data.get("test_accuracy", None)
    classification_report_dict = model_data.get("classification_report", None)

    # ✅ Display accuracy metrics
    st.markdown("---")  # Separator for better UI
    st.subheader("📊 Model Performance")
    if train_accuracy is not None and test_accuracy is not None:
        st.markdown(f"✅ **Training Accuracy:** `{train_accuracy:.2%}`")
        st.markdown(f"✅ **Test Accuracy:** `{test_accuracy:.2%}`")
    else:
        st.warning("⚠️ Accuracy values not found in the saved model file.")

    # ✅ Display classification report
    if classification_report_dict:
        st.markdown("---")  # Separator
        st.subheader("📜 Classification Report")

        # Convert dictionary to DataFrame and rename labels
        report_df = pd.DataFrame(classification_report_dict).T
        if "0" in report_df.index and "1" in report_df.index:
            report_df.rename(index={"0": "No", "1": "Yes"}, inplace=True)

        st.table(report_df)  # Display as a table
    else:
        st.warning("⚠️ Classification report not found in the saved model file.")
