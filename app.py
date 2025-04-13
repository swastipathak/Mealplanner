import streamlit as st
import pandas as pd
import os

# Page config
st.set_page_config(page_title="Smart Lifestyle Meal Planner", layout="wide")
st.title("🥗 Smart Lifestyle Meal Planner")

# Load dataset
csv_path = r"D:\Smartlifestyleapp\data\merged_diet_recipes.csv"
df = pd.read_csv(csv_path)
df.columns = df.columns.str.strip()

# Drop unnecessary columns
for col in ['Unnamed: 0', 'diet_type']:
    if col in df.columns:
        df.drop(columns=col, inplace=True)

# Sidebar filter
diet_options = df['Diet_type'].dropna().unique()
selected_diet = st.sidebar.selectbox("Choose a diet type:", diet_options)
top_n = st.sidebar.slider("How many recipes to view?", 1, 10, 5)

# Filter by selected diet
filtered_df = df[df['Diet_type'].str.lower() == selected_diet.lower()]

# Set your full image path
image_folder = r"D:\fooddata\Food Images"

# Display recipes
if filtered_df.empty:
    st.warning("No recipes found for the selected diet.")
else:
    for idx, row in filtered_df.head(top_n).iterrows():
        st.subheader(row['Recipe_name'])

        # Image loading logic
        image_name = str(row['Image_Name']).strip()
        found = False

        for ext in ['.jpg', '.jpeg', '.png']:
            image_path = os.path.join(image_folder, image_name + ext)
            if os.path.exists(image_path):
                st.image(image_path, use_column_width=True, caption=image_name)
                found = True
                break

        if not found:
            st.warning(f"⚠️ Image not found for: {image_name}")

        # Nutrients
        st.markdown(f"**Protein:** {row['Protein(g)']}g")
        st.markdown(f"**Carbs:** {row['Carbs(g)']}g")
        st.markdown(f"**Fat:** {row['Fat(g)']}g")

        # Ingredients
        if pd.notna(row['Ingredients']):
            st.markdown("#### 🡢 Ingredients")
            st.markdown(row['Ingredients'])

        # Instructions
        if pd.notna(row['Instructions']):
            st.markdown("#### 🍳 Instructions")
            st.markdown(row['Instructions'])

        # Shopping Button
        if 'Cleaned_Ingredients' in row and pd.notna(row['Cleaned_Ingredients']):
            if st.button(f"🛒 Find Products for {row['Recipe_name']}", key=f"product_button_{idx}"):
                st.success("🛎️ Products to buy:")
                for item in row['Cleaned_Ingredients'].split(','):
                    item = item.strip()
                    if item:
                        search_url = f"https://www.google.com/search?q=buy+{item.replace(' ', '+')}"
                        st.markdown(f"- [{item}]({search_url})")

        st.markdown("---")
