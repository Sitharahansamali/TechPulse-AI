import streamlit as st
import requests
import os
from dotenv import load_dotenv
from streamlit_option_menu import option_menu

# Load env
load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL")

# Page config
st.set_page_config(
    page_title="TechPulse AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>

.main {
    background-color: #0f172a;
    color: white;
}

.block-container {
    padding-top: 2rem;
}

.article-card {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
    border: 1px solid #334155;
}

.category-badge {
    background-color: #2563eb;
    padding: 5px 12px;
    border-radius: 20px;
    color: white;
    display: inline-block;
    font-size: 14px;
    margin-bottom: 10px;
}

.metric-card {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:

    st.title("TechPulse AI")

    selected = option_menu(
        menu_title="Navigation",
        options=["Home"],
        icons=["house"],
        default_index=0
    )

    st.divider()

    category = st.selectbox(
        "Filter Category",
        [
            "All",
            "AI",
            "Cybersecurity",
            "Cloud Computing",
            "Data Science",
            "Blockchain",
            "DevOps",
            "Other"
        ]
    )

# Header
st.title(" TechPulse AI Dashboard")

st.caption(
    "AI-powered technology news analysis platform"
)

# Search
search = st.text_input(
    "🔍 Search Articles"
)

# get category image if image-url is not preset in the article
CATEGORY_IMAGES = {
    "AI": "https://images.unsplash.com/photo-1677442136019-21780ecad995",
    "Cybersecurity": "https://images.unsplash.com/photo-1510511459019-5dda7724fd87",
    "Cloud Computing": "https://images.unsplash.com/photo-1451187580459-43490279c0fa",
    "Blockchain": "https://images.unsplash.com/photo-1639762681485-074b7f938ba0",
    "Data Science": "https://images.unsplash.com/photo-1551288049-bebda4e38f71",
    "Other": "https://images.unsplash.com/photo-1495020689067-958852a7765e"
}

# Fetch Articles
try:

    if search:

        response = requests.get(
            f"{BACKEND_URL}/search",
            params={"q": search}
        )

    elif category != "All":

        response = requests.get(
            f"{BACKEND_URL}/articles/{category}"
        )

    else:

        response = requests.get(
            f"{BACKEND_URL}/articles"
        )

    articles = response.json()

    # Metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Articles",
            len(articles)
        )

    with col2:
        st.metric(
            "Categories",
            len(set([
                a.get("category")
                for a in articles
                if a.get("category")
            ]))
        )

    with col3:
        st.metric(
            "AI Processed",
            "Yes"
        )

    st.divider()

    # Articles Grid
    for article in articles:

        st.markdown(
            '<div class="article-card">',
            unsafe_allow_html=True
        )

        col1, col2 = st.columns([1, 2])

        with col1:

            image_url = article.get("image")

            if not image_url:
            
                image_url = CATEGORY_IMAGES.get(
                    article.get("category"),
                    CATEGORY_IMAGES["Other"]
                )
            
            st.image(
                image_url,
                use_container_width=True
            )    

        with col2:

            st.markdown(
                f"""
                <div class="category-badge">
                    {article.get("category")}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.subheader(article.get("title"))

            st.write(article.get("summary"))

            tags = article.get("tags", [])

            if tags:

                st.write(
                    " ".join(
                        [f"`#{tag}`" for tag in tags]
                    )
                )

            st.markdown(
                f"""
                🔗 [Read Full Article]({article.get('url')})
                """
            )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

except Exception as e:

    st.error(f"Error: {e}")