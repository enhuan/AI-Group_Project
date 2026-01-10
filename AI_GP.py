import streamlit as st
import pandas as pd
import re
import ast
from collections import Counter
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# ---------------------------------------------
# 1. PAGE CONFIG
# ---------------------------------------------
st.set_page_config(
    page_title="CookMate",
    layout="wide"
)


# ---------------------------------------------
# 2. LOAD DATA
# ---------------------------------------------
@st.cache_data
def load_and_clean_data():
    df = pd.read_csv("1_Recipe_csv.csv")

    def simple_clean(text):
        text = str(text).lower()
        text = re.sub(r"[^a-z\s]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    df["search_field"] = df["ingredients"].apply(simple_clean)
    return df


df = load_and_clean_data()

# ---------------------------------------------
# 3. SESSION STATE
# ---------------------------------------------
if "started" not in st.session_state:
    st.session_state.started = False

# ---------------------------------------------
# 4. HEADER WITH LOGOS
# ---------------------------------------------
col_main, col_logo = st.columns([6, 2])
with col_logo:
    l1, l2 = st.columns(2)
    with l1:
        st.image("umpsa.png", width=100)
    with l2:
        st.image("CookMate.png", width=100)

# ---------------------------------------------
# 5. HOME PAGE
# ---------------------------------------------
if not st.session_state.started:

    st.markdown("<h1 style='text-align:center; color:#6e82d3;'>🍳 CookMate</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center; color:#967EAF;'>Your Personalized Recipe Recommender</h3>",
                unsafe_allow_html=True)
    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(
            "### 👨‍🍳 About CookMate\n"
            "CookMate is an **AI-powered, data-driven recipe recommendation system** that helps users "
            "discover dishes based on available ingredients. By applying intelligent matching techniques, "
            "it reduces food waste, saves time, inspires creativity, and makes home cooking easier. It will "
            "guide you to cook every delicious meal! 🍽️"
        )

    with col2:
        st.success(
            "### 🤝 Collaboration\n"
            "CookMate features a **high-quality, multi-category recipe dataset** with over **62,000+ recipes**. "
            "We plan to collaborate with **Secret Recipe** to continuously update and expand the dataset, "
            "so that every user always has fresh, inspiring recipes to explore. ✨️"
        )

    with col3:
        st.warning(
            "### 🌱 ESG Commitment\n"
            "- **Environmental:** Reduce food waste and promote sustainable cooking 🌍\n"
            "- **Social:** Empower everyone to cook healthy meals at home 🥦\n"
            "- **Governance:** Ethical and transparent data usage 📊\n"
            "\nCookMate is committed to responsible consumption and a sustainable culinary experience."
        )

    st.divider()

    # ROW 1
    c1, c2 = st.columns(2)

    with c1:
        st.info(
            "### 🗂️ Step 1: Choose Category & Subcategory\n"
            "Start your search by selecting:\n\n"
            "• A **Category** (e.g. Air Fryer, Dessert, Main Course)\n\n"
            "• A **Subcategory** to further narrow down recipes\n\n"
            "CookMate will find recipes that match what you are looking for!"
        )

    with c2:
        st.success(
            "### 🧾 Step 2: Get Ingredient Suggestions\n"
            "Once a subcategory is selected:\n\n"
            "• CookMate shows **common ingredients** used in that subcategory\n\n"
            "• Use them as inspiration or guidance\n\n"
            "You don’t need to remember everything — CookMate helps you!"
        )

    st.markdown("<h4 style='text-align:center;'>⬇️</h4>", unsafe_allow_html=True)

    # ROW 2
    c3, c4 = st.columns(2)

    with c3:
        st.warning(
            "### 🧺 Step 3: Enter Your Ingredients\n"
            "Type in the ingredients you have at home:\n\n"
            "• Separate ingredients with commas or spaces\n\n"
            "• Example: chicken, garlic, onion\n\n"
            "CookMate will match recipes based on what you already have!"
        )

    with c4:
        st.info(
            "### 🔍 Step 4: Choose Matching Mode\n"
            "Decide how ingredients should be matched:\n\n"
            "• **Match ALL ingredients** → recipes must include all your ingredients\n\n"
            "• **Match ANY ingredient** → recipes include at least one of them\n\n"
            "Let's see what fits your cooking style best!"
        )

    st.markdown("<h4 style='text-align:center;'>⬇️</h4>", unsafe_allow_html=True)

    # ROW 3
    c5, c6 = st.columns(2)

    with c5:
        st.success(
            "### 🍳 Step 5: Select Cooking Preference\n"
            "Customize how detailed your recipes should be:\n\n"
            "• **All Recipes** → no restriction\n\n"
            "• **Quick Recipes** → faster and simpler meals\n\n"
            "• **Full Recipes** → detailed cooking steps\n\n"
            "Busy days or relaxed cooking sessions? CookMate is perfect for you anytime!"
        )

    with c6:
        st.warning(
            "### 🎛️ Step 6: Control Number of Results\n"
            "Use the **Max Results** slider to:\n\n"
            "• Choose how many recipes you want to see\n\n"
            "• Do you need just a few or full list of choices?\n\n"
            "Let us know how many recommendations you need!"
        )

    st.markdown("<h4 style='text-align:center;'>⬇️</h4>", unsafe_allow_html=True)

    # FINAL STEP
    st.error(
        "### 🍽️ Step 7: Search & Explore Recipes\n"
        "Click **Search** to view your personalized recipe list:\n\n"
        "• Recipes are ranked based on your ingredients\n\n"
        "• View ingredients and step-by-step directions\n\n"
        "• Click the provided link to open Google Images for visual inspiration 📷\n\n"
        "Enjoy cooking with CookMate!"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚀 Start Cooking with CookMate"):
        st.session_state.started = True

    st.stop()

# ---------------------------------------------
# 6. BACK TO HOME BUTTON
# ---------------------------------------------
col_back, col_title = st.columns([1, 6])
with col_back:
    if st.button("🏠 Back to Home"):
        st.session_state.started = False

with col_title:
    st.markdown("<h2 style='color:#546DA6;'>🍳 CookMate Recipe Search</h2>", unsafe_allow_html=True)

# ---------------------------------------------
# 7. SIDEBAR FILTERS
# ---------------------------------------------
st.sidebar.header("🔍 Personalize Your Search")

# Category
categories = ["All"] + sorted(df["category"].dropna().unique())
selected_cat = st.sidebar.selectbox("Category", categories)

filtered_df = df.copy()
if selected_cat != "All":
    filtered_df = filtered_df[filtered_df["category"] == selected_cat]

# Subcategory
subcategories = ["All"] + sorted(filtered_df["subcategory"].dropna().unique())
selected_sub = st.sidebar.selectbox("Subcategory", subcategories)

if selected_sub != "All":
    filtered_df = filtered_df[filtered_df["subcategory"] == selected_sub]

# Ingredient guidance
if selected_sub != "All":
    ingredient_text = " ".join(filtered_df["search_field"].dropna())
    common_ingredients = [
        w for w, _ in Counter(ingredient_text.split()).most_common(20)
        if len(w) > 2
    ]
    st.sidebar.markdown("🧾 **Common Ingredients in This Subcategory**")
    st.sidebar.write(", ".join(common_ingredients))

# Ingredient input
raw_input = st.sidebar.text_input(
    "Enter Ingredients",
    placeholder="e.g. chicken, garlic, onion"
).lower()

search_mode = st.sidebar.radio(
    "Ingredient Matching Mode",
    ["Match ALL ingredients", "Match ANY ingredient"]
)

recipe_type = st.sidebar.selectbox(
    "Cooking Preference",
    ["All", "Quick Recipes", "Full Recipes"]
)

max_results = st.sidebar.slider("Max Results", 5, 50, 20)

search_clicked = st.sidebar.button("🔎 Search Recipes")

# ---------------------------------------------
# DATASET VISUALIZATIONS
# ---------------------------------------------
if not search_clicked:
    st.markdown("### 📊 Dataset Overview")

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Total Recipes", f"{len(df):,}")
    m2.metric("Categories", df['category'].nunique())
    m3.metric("Subcategories", df['subcategory'].nunique())
    m4.metric("Avg Ingredients", round(df['num_ingredients'].mean(), 1))
    m5.metric("Avg Steps", round(df['num_steps'].mean(), 1))

    st.divider()

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("#### ☁️ Category Themes")
        cat_text = " ".join(df['category'].dropna().astype(str))

        wc = WordCloud(
            background_color="white",
            colormap="plasma",
            width=800,
            height=500,
            collocations=False,
            repeat=True
        ).generate(cat_text)

        fig_wc, ax = plt.subplots()
        ax.imshow(wc, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig_wc)

    with col_right:
        st.markdown("#### 📈 Complexity Distribution")
        viz_choice = st.radio("Show distribution of:", ["Ingredients", "Steps"], horizontal=True)

        if viz_choice == "Ingredients":
            fig_hist = px.histogram(df, x="num_ingredients", nbins=40,
                                    title="Distribution of Number of Ingredients",
                                    color_discrete_sequence=['#6e82d3'])
            fig_hist.update_layout(xaxis_title="Number of Ingredients", yaxis_title="Recipe Count")
        else:
            fig_hist = px.histogram(df, x="num_steps", nbins=40,
                                    title="Distribution of Cooking Steps",
                                    color_discrete_sequence=['#967EAF'])
            fig_hist.update_layout(xaxis_title="Number of Steps", yaxis_title="Recipe Count")

        st.plotly_chart(fig_hist, use_container_width=True)

# ---------------------------------------------
# 8. SEARCH LOGIC
# ---------------------------------------------
if search_clicked:

    result_df = filtered_df.copy()

    ingredients = []
    if raw_input:
        ingredients = [i for i in re.split(r",|\s+", raw_input) if i.strip()]
        if search_mode == "Match ALL ingredients":
            for ing in ingredients:
                result_df = result_df[
                    result_df["search_field"].str.contains(rf"\b{re.escape(ing)}\b", na=False)
                ]
        else:
            pattern = "|".join(rf"\b{re.escape(i)}\b" for i in ingredients)
            result_df = result_df[
                result_df["search_field"].str.contains(pattern, na=False)
            ]

        # Relevance sorting
        result_df["match_score"] = result_df["search_field"].apply(
            lambda x: sum(ing in x for ing in ingredients)
        )
        result_df = result_df.sort_values("match_score", ascending=False)

    # Quick / Full recipe
    if recipe_type == "Quick Recipes":
        result_df = result_df[result_df["directions"].str.len() < 500]
    elif recipe_type == "Full Recipes":
        result_df = result_df[result_df["directions"].str.len() >= 500]

    result_df = result_df.head(max_results)

    # ---------------------------------------------
    # 9. OUTPUT
    # ---------------------------------------------
    st.header(f"🍱 Found {len(result_df)} Recipes")

    if result_df.empty:
        st.warning("No recipes found. Try different filters.")
    else:
        for idx, row in result_df.iterrows():
            with st.expander(f"📖 {row['recipe_title']}"):

                # Description
                st.markdown("#### 📝 Description")
                st.write(row["description"])

                # Inside the recipe expander loop
                query = row['recipe_title'].replace(" ", "+")
                google_url = f"https://www.google.com/search?tbm=isch&q={query}"

                st.markdown(
                    f"#### 🖼️ Example Image\n"
                    f"[Click here to view example images of **{row['recipe_title']}**]({google_url})",
                    unsafe_allow_html=True
                )

                # Ingredients & Directions
                col1, col2 = st.columns([1, 2])

                with col1:
                    st.markdown("#### 🛒 Ingredients")
                    try:
                        ing_list = ast.literal_eval(row["ingredients"])
                        for item in ing_list:
                            st.write(f"- {item}")
                    except:
                        st.write(row["ingredients"])

                with col2:
                    st.markdown("#### 👨‍🍳 Directions")
                    try:
                        dir_list = ast.literal_eval(row["directions"])
                        for i, step in enumerate(dir_list, 1):
                            st.write(f"**Step {i}:** {step}")
                    except:
                        st.write(row["directions"])

                st.divider()
