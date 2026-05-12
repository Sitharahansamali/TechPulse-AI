import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Backend URL
BACKEND_URL = os.getenv("BACKEND_URL")

# Page Config
st.set_page_config(
    page_title="TechPulse AI",
    layout="wide"
)

# Title
st.title("TechPulse AI")

st.write(
    "AI-powered technology news platform"
)

# Search
search = st.text_input(
    "Search Articles"
)

# Fetch Articles
try:

    if search:

        response = requests.get(
            f"{BACKEND_URL}/search",
            params={"q": search}
        )

    else:

        response = requests.get(
            f"{BACKEND_URL}/articles"
        )

    articles = response.json()

    # Display Articles
    for article in articles:

        with st.container():

            st.subheader(article.get("title"))

            col1, col2 = st.columns([1, 2])

            with col1:

                if article.get("image"):

                    st.image(
                        article.get("image"),
                        use_container_width=True
                    )

            with col2:

                st.write(
                    f"**Category:** {article.get('category')}"
                )

                st.write(
                    article.get("summary")
                )

                # Tags
                tags = article.get("tags", [])

                if tags:

                    st.write(
                        " ".join(
                            [f"`#{tag}`" for tag in tags]
                        )
                    )

                st.markdown(
                    f"[Read Full Article]({article.get('url')})"
                )

            st.divider()

except Exception as e:

    st.error(f"Error: {e}")