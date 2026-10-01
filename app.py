import streamlit as st
import requests

# Page configuration
st.set_page_config(
    page_title="AI Text Summarizer",
    page_icon="📝",
    layout="wide"
)

# Title
st.title("📝 AI Text Summarizer")
st.write("Summarize your text using the Mistral AI model with Ollama.")

# Text input
text = st.text_area(
    "Enter your text:",
    height=300,
    placeholder="Paste your paragraph or article here..."
)

# Summary length
summary_length = st.selectbox(
    "Select summary length:",
    ["Short", "Medium", "Detailed"]
)

# Generate summary
if st.button("✨ Generate Summary"):

    if not text.strip():
        st.warning("Please enter some text first.")

    else:
        if summary_length == "Short":
            instruction = "Summarize the text in 3 to 4 sentences."

        elif summary_length == "Medium":
            instruction = "Summarize the text in 5 to 7 sentences."

        else:
            instruction = "Provide a detailed summary covering all important points."

        prompt = f"""
You are an expert text summarization assistant.

Summarize the following text.

Instructions:
- {instruction}
- Keep the important information.
- Do not add information that is not present in the original text.
- Use clear and simple language.

Text:
{text}
"""

        with st.spinner("Generating summary..."):

            try:
                response = requests.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": "mistral",
                        "prompt": prompt,
                        "stream": False
                    }
                )

                if response.status_code == 200:

                    result = response.json()["response"]

                    st.success("Summary generated successfully!")

                    st.subheader("📌 Summary")
                    st.write(result)

                else:
                    st.error(
                        f"Ollama Error: {response.status_code}"
                    )

            except requests.exceptions.ConnectionError:
                st.error(
                    "Could not connect to Ollama. "
                    "Please make sure Ollama is running."
                )