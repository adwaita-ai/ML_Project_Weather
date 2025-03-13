import streamlit as st

def show_summary():
    st.title("📜 Project Summary")

    # Exploratory Data Analysis (EDA)
    st.subheader("🔍 Exploratory Data Analysis (EDA)")
    st.markdown(
        """
        - Performed thorough **Exploratory Data Analysis (EDA)** to understand dataset characteristics.
        - **Handled missing values:**
          - Continuous data: Filled using **mean**.
          - Categorical data: Filled using **mode**.
        - Used **heatmap** to identify correlations among independent variables.
        - Applied **Variance Inflation Factor (VIF)** to detect and eliminate multicollinearity.
        """
    )
    
    st.markdown("---")  # Adds a horizontal line for better separation
    
    # Feature Engineering
    st.subheader("📊 Feature Engineering")
    st.markdown(
        """
        - **Feature Extraction:**
          - Extracted **Year** and **Month** from the **Date** column.
        - **Feature Selection:**
          - Dropped highly correlated columns to reduce multicollinearity.
        """
    )

    st.markdown("---")

    # Data Visualization
    st.subheader("📈 Data Visualization")
    st.markdown(
        """
        - **Used Seaborn** for various plots:
          - Boxplot, Lineplot, Countplot, Barplot, Scatterplot.
        - **Interactive visualizations** created using **Plotly**.
        """
    )

    st.markdown("---")

    # Data Preprocessing
    st.subheader("📉 Data Preprocessing")
    st.markdown(
        """
        - Identified **left-skewed data** and applied transformations:
          - **Power Transform** & **Winsorization** to handle outliers.
        - Encoded categorical variables using **get_dummies()**.
        - Separated **target column** from independent variables.
        - Performed **train-test split** and applied **scaling**.
        """
    )

    st.markdown("---")

    # Model Training & Evaluation
    st.subheader("🤖 Model Training & Evaluation")
    st.markdown(
        """
        - Trained various classification models:
          - **KNN, BernoulliNB, Decision Tree, Random Forest, XGBoost, CatBoost, LGBM, AdaBoost**.
        - Since this dataset is highly **imbalanced**, used **Recall** as the primary evaluation metric.
        - **Performed SMOTE** to balance the dataset.
        - Achieved best performance with **XGBoostClassifier**:
          - **Recall for 'No' class:** 0.9079
          - **Recall for 'Yes' class:** 0.8652
        """
    )