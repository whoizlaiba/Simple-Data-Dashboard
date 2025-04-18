
import streamlit as st
import pandas as pd

st.title("Simple Data Dashboard")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Error reading the file: {e}")
    else:
        st.subheader("Data Preview")
        st.write(df.head())

        st.subheader("Data Summary")
        if not df.describe().empty:
            st.write(df.describe())
        else:
            st.write("No numeric data to describe.")

        st.subheader("Data Filter")
        columns = df.columns.tolist()

        if columns:
            selected_column = st.selectbox("Select column to filter by", columns)

            if not df[selected_column].isnull().all():
                unique_values = df[selected_column].dropna().unique()
                selected_value = st.selectbox("Select value", unique_values)

                filtered_df = df[df[selected_column] == selected_value]
                st.write(filtered_df)

                # Plot Data Section
                st.subheader("Plot Data")

                numeric_columns = df.select_dtypes(include=['number']).columns.tolist()

                if not filtered_df.empty and numeric_columns:
                    x_column = st.selectbox("Select x-axis column", columns)
                    y_column = st.selectbox("Select y-axis column", numeric_columns)

                    if st.button("Generate Plot"):
                        if x_column in filtered_df.columns and y_column in filtered_df.columns:
                            try:
                                chart_data = filtered_df.set_index(x_column)[y_column]
                                st.line_chart(chart_data)
                            except Exception as e:
                                st.error(f"Error generating plot: {e}")
                        else:
                            st.warning("Selected columns are not available for plotting.")
                else:
                    st.write("Filtered data is empty or no numeric columns available for plotting.")
            else:
                st.write("Selected column contains only null values.")
        else:
            st.warning("No columns found in the uploaded file.")
else:
    st.write("Waiting on a file upload...")
