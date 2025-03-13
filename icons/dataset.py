import streamlit as st
import pandas as pd
import os

def show_dataset():
    dataset_path = os.path.join(os.getcwd(), "pictures_model", "weatherAUS.csv")

    st.title("📂 Dataset")

    if os.path.exists(dataset_path):
        try:
            df = pd.read_csv(dataset_path, encoding="ISO-8859-1")
            st.write(f"✅ Dataset Loaded Successfully! \n Shape: {df.shape}")

            # ✅ Main Tabs
            tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 DataFrame", "📜 Description", "ℹ️ Info", "🔍 Missing Values", "🔠 Data Types"])

            with tab1:
                st.subheader("DataFrame")

                # ✅ FILTER SECTION (Inside the Tab)
                st.write("**Filter by Column Values:**")
                filter_cols = st.multiselect("Select Columns to Filter", df.columns)

                # Dictionary to store selected filters
                filters = {}

                for col in filter_cols:
                    unique_values = sorted(df[col].dropna().unique())  # Sort values for better UI
                    filters[col] = st.multiselect(f"Select Values for {col}", unique_values)

                # Apply filters dynamically
                filtered_df = df.copy()
                for col, values in filters.items():
                    if values:  # Apply filter only if user selects values
                        filtered_df = filtered_df[filtered_df[col].isin(values)]

                st.dataframe(filtered_df, height=600)

            with tab2:
                st.subheader("Dataset Description")
                
                # Drop rows where all values are NaN (which might be causing blanks)
                description_df = df.describe().round(2).dropna(how="all")

                st.dataframe(description_df, height=400, use_container_width=True)


            with tab3:
                st.subheader("Dataset Info")
                info_df = pd.DataFrame({
                    "Column": df.columns,
                    "Non-Null Count": df.count().values,
                    "Dtype": df.dtypes.values
                })
                memory_usage = df.memory_usage(deep=True).sum() / (1024 ** 2)
                st.write(f"**💾 Estimated Memory Usage:** `{memory_usage:.2f} MB`")
                st.dataframe(info_df, height=500, use_container_width=True)

            with tab4:
                st.subheader("Missing Values")

                # Compute missing values
                missing_values = df.isna().sum()
                missing_df = pd.DataFrame({
                    'Column': missing_values.index,
                    'Missing Values': missing_values.values
                }).query("`Missing Values` > 0").reset_index(drop=True)

                # Compute percentage of missing values
                missing_percentage_df = missing_df.copy()
                missing_percentage_df["Percentage"] = (missing_percentage_df["Missing Values"] / len(df)) * 100
                missing_percentage_df = missing_percentage_df.sort_values(by="Percentage", ascending=False)[["Column", "Percentage"]]

                # Filter columns with missing values > 1000
                high_missing_df = missing_df[missing_df["Missing Values"] > 1000]

                # Select box for missing value analysis
                option = st.selectbox(
                    "Select Missing Values Analysis",
                    ["All Columns with Missing Values", "Percentage of Missing Values", "Columns with Missing Values > 1000"]
                )

                if option == "All Columns with Missing Values":
                    st.write("**Columns with Missing Values:**")
                    st.dataframe(missing_df[["Column", "Missing Values"]], height=400, use_container_width=True)

                elif option == "Percentage of Missing Values":
                    st.write("**Percentage of Missing Values in Each Column:**")
                    st.dataframe(missing_percentage_df, height=400, use_container_width=True)

                elif option == "Columns with Missing Values > 1000":
                    st.write("**Columns with More Than 1000 Missing Values:**")
                    if not high_missing_df.empty:
                        st.dataframe(high_missing_df[["Column", "Missing Values"]], height=400, use_container_width=True)
                    else:
                        st.success("✅ No columns have more than 1000 missing values.")

            with tab5:
                st.subheader("Data Types")

                # ✅ Filter Options for Data Types
                dtype_option = st.selectbox(
                    "Select Data Type Filter",
                    ["All Columns", "Only Float Data Types", "Only Object Data Types"]
                )

                data_types_df = pd.DataFrame({
                    "Column": df.columns,
                    "Data Type": df.dtypes.astype(str).values
                })

                if dtype_option == "🔢 Only Float Data Types":
                    filtered_dtype_df = data_types_df[data_types_df["Data Type"] == "float64"]
                elif dtype_option == "🔠 Only Object Data Types":
                    filtered_dtype_df = data_types_df[data_types_df["Data Type"] == "object"]
                else:
                    filtered_dtype_df = data_types_df

                st.dataframe(filtered_dtype_df, height=400, use_container_width=True)

        except Exception as e:
            st.error(f"❌ Error reading dataset: {e}")
    else:
        st.error("⚠️ Dataset file not found!")
