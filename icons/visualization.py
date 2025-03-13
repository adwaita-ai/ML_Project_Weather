import streamlit as st
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

# Load the cleaned dataset
@st.cache_data
def load_data():
    file_path = os.path.join(os.getcwd(), "pictures_model", "cleaned_weatherAUS.csv")
    try:
        df1 = pd.read_csv(file_path)
        df1['Date'] = pd.to_datetime(df1['Date'])
        df1['Year'] = df1['Date'].dt.year
        df1['Month'] = df1['Date'].dt.month
        return df1
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return None

df1 = load_data()

# Function to display visualizations
def show_visualization(df1):
    st.subheader("📈 Visualization")
    if df1 is None or df1.empty:
        st.error("❌ No data available for visualization.")
        return

    viz_tabs = st.tabs(["📊 Count Plots", "📍 Scatter Plot", "📉 Histogram", "📦 Box Plot", "📊 Bar Plots", "📈 Line Plots", "🔘 Pie Chart"])

    with viz_tabs[0]:
        st.subheader("📊 Count Plots for Categorical Columns")
        categorical_columns = [col for col in df1.select_dtypes(include=["object"]).columns if col.lower() != "date"]
        if not categorical_columns:
            st.error("❌ No categorical columns found.")
        else:
            selected_column = st.selectbox("Select a categorical column", categorical_columns)
            counts_df = df1[selected_column].value_counts().reset_index()
            counts_df.columns = [selected_column, "count"]
            fig = px.bar(counts_df, x=selected_column, y="count", title=f"Count Plot for {selected_column}")
            st.plotly_chart(fig)

    with viz_tabs[1]:  # Scatter Plot
        st.subheader("📍 Scatter Plot")
        numerical_columns = df1.select_dtypes(include=['number']).columns.tolist()

        if len(numerical_columns) < 2:
            st.error("❌ Not enough numerical columns for scatter plot.")
        else:
            x_col = st.selectbox("Select the X-axis column:", numerical_columns, key="scatter_x")
            y_col = st.selectbox("Select the Y-axis column:", numerical_columns, key="scatter_y")
            fig = px.scatter(df1, x=x_col, y=y_col, title=f"Scatter Plot: {x_col} vs {y_col}")
            st.plotly_chart(fig, use_container_width=True)

    with viz_tabs[2]:
        st.subheader("📉 Histogram")
        selected_column = st.selectbox("Select a numerical column for histogram", numerical_columns)
        fig = px.histogram(df1, x=selected_column, nbins=30, title=f"Histogram of {selected_column}")
        st.plotly_chart(fig, use_container_width=True)

    with viz_tabs[3]:
        st.subheader("📦 Box Plot")
        selected_column = st.selectbox("Select a numerical column for box plot", numerical_columns, key='box')
        fig = px.box(df1, y=selected_column, title=f"Box Plot of {selected_column}")
        st.plotly_chart(fig, use_container_width=True)

        with viz_tabs[4]:
            st.subheader("📊 Bar Plots")
            plot_selection = st.selectbox("Select a plot", [
                "Effect of Morning Cloud Cover on Sunshine Hours",
                "Highest Rainfall Per Year",
                "Lowest Rainfall Per Year",
                "Highest Temperature in Each Location",
                "Lowest Temperature in Each Location"
            ])

            if plot_selection == "Effect of Morning Cloud Cover on Sunshine Hours" and {'Cloud9am', 'Sunshine'}.issubset(df1.columns):
                cloud = df1.groupby(['Cloud9am'])['Sunshine'].mean().reset_index()
                fig = px.bar(cloud, x='Cloud9am', y='Sunshine', title='Effect of Morning Cloud Cover on Sunshine Hours', color_discrete_sequence=['red'])
                st.plotly_chart(fig)
            
            elif plot_selection == "Highest Rainfall Per Year":
                avg_rainfall = df1.groupby(['Year', 'Location'])['Rainfall'].mean().reset_index()
                highest_rainfall_each_year = avg_rainfall.loc[avg_rainfall.groupby('Year')['Rainfall'].idxmax()]
                fig = px.bar(highest_rainfall_each_year, x='Year', y='Rainfall', color='Location', title='Highest Rainfall Per Year in Each Location')
                st.plotly_chart(fig)
            
            elif plot_selection == "Lowest Rainfall Per Year":
                avg_rainfall = df1.groupby(['Year', 'Location'])['Rainfall'].mean().reset_index()
                lowest_rainfall_each_year = avg_rainfall.loc[avg_rainfall.groupby('Year')['Rainfall'].idxmin()]
                fig = px.bar(lowest_rainfall_each_year, x='Year', y='Rainfall', color='Location', title='Lowest Rainfall Per Year in Each Location')
                st.plotly_chart(fig)
            
            elif plot_selection == "Highest Temperature in Each Location":
                maxtemp = df1.groupby('Year')['MaxTemp'].idxmax()
                maxtemp_df = df1.loc[maxtemp]
                fig = px.bar(maxtemp_df, x='Year', y='MaxTemp', color='Location', title='Highest Temperature in Each Location Over the Years')
                st.plotly_chart(fig)
            
            elif plot_selection == "Lowest Temperature in Each Location":
                mintemp = df1.groupby('Year')['MinTemp'].idxmin()
                mintemp_df = df1.loc[mintemp]
                fig = px.bar(mintemp_df, x='Year', y='MinTemp', color='Location', title='Lowest Temperature in Each Location Over the Years')
                st.plotly_chart(fig)

        with viz_tabs[5]:
            st.subheader("📈 Line Plots")
            if 'Humidity3pm' in df1.columns and 'Rainfall' in df1.columns:
                humidity = df1.groupby('Humidity3pm')['Rainfall'].mean().reset_index()
                fig1 = px.line(humidity, x='Humidity3pm', y='Rainfall', title='Mean Rainfall at Different Humidity Levels', markers=True)
                st.plotly_chart(fig1)

            if 'Location' in df1.columns and 'Rainfall' in df1.columns:
                top5 = df1.groupby('Location')['Rainfall'].mean().nlargest(5).index.tolist()
                df_top5 = df1[df1['Location'].isin(top5)]
                fig2 = px.line(df_top5, x='Year', y='Rainfall', color='Location',
                            title='Rainfall Trends Over the Years (Top 5 Locations)',
                            markers=True,
                            color_discrete_sequence=px.colors.qualitative.Pastel)
                fig2.update_layout(legend_title_text='Top 5 Locations')
                st.plotly_chart(fig2)

    with viz_tabs[6]:
            st.subheader("🔘 Pie Chart")

            # Get categorical columns and exclude "Location"
            categorical_cols = df1.select_dtypes(include=['object']).columns.tolist()
            categorical_cols = [col for col in categorical_cols if col.lower() != "location"]  # Case-insensitive exclusion

            if not categorical_cols:
                st.warning("⚠️ No categorical columns found.")
            else:
                selected_col = st.selectbox("Select a categorical column:", categorical_cols, key="pie_chart")
                category_counts = df1[selected_col].value_counts().reset_index()
                category_counts.columns = [selected_col, "Count"]
                fig = px.pie(category_counts, names=selected_col, values="Count", 
                            title=f"Distribution of {selected_col}",
                            color_discrete_sequence=px.colors.qualitative.Set3)
                st.plotly_chart(fig, use_container_width=True)