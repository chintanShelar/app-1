import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Set the vibe for the page
st.set_page_config(page_title="Forecasting Vibe Check", layout="wide")
st.title("📊 The Forecasting Vibe Check App")

st.markdown("Drop your Excel files below and let's see if your numeric data has that normal distribution energy.")

# The dropzone
uploaded_file = st.file_uploader("Upload Excel File (.xlsx, .xls)", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        # Read the spreadsheet
        df = pd.read_excel(uploaded_file)
        st.success("File uploaded successfully. No cap.")
        
        # Filter out the noise, keep only the numbers
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) == 0:
            st.warning("Big yikes. There are no numeric columns in this file.")
        else:
            for col in numeric_cols:
                st.markdown(f"### Feature: {col}")
                
                # Crunching the numbers
                col_mean = df[col].mean()
                col_median = df[col].median()
                col_std = df[col].std()
                
                # The proximity logic
                if pd.isna(col_std) or col_std == 0:
                    is_near = (col_mean == col_median)
                else:
                    is_near = abs(col_mean - col_median) < (0.10 * col_std)
                
                # Display the stats
                st.write(f"**Mean:** {col_mean:.4f} | **Median:** {col_median:.4f}")
                
                # The Judgment
                if is_near:
                    st.success("✨ The data can be used for forecasting. Mean and median are basically twins.")
                else:
                    st.error("🚩 Big skew energy. Mean and median are drifting apart. Not ideal for forecasting.")
                
                # Painting the picture (Histogram)
                fig, ax = plt.subplots(figsize=(10, 4))
                ax.hist(df[col].dropna(), bins=30, color='#00d4ff', edgecolor='black', alpha=0.7)
                ax.set_title(f"Distribution of {col}")
                ax.set_xlabel("Value")
                ax.set_ylabel("Frequency")
                ax.grid(axis='y', linestyle='--', alpha=0.5)
                
                st.pyplot(fig)
                st.markdown("---")
                
    except Exception as e:
        st.error(f"Oof, something broke the matrix: {e}")
