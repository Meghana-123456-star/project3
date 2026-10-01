import streamlit as st
import requests

st.title("Mistral AI Text Summarizer")

API_KEY = "mstrl_c710PaOTB63cAYEeiR3oxwRSfoCsMHnM_4ynmoF"

text = st.text_area(
    "Enter your huge text",
    height=300
)

user_prompt = st.text_input(
    "Enter your summarization prompt",
    "Summarize this text in 5 simple bullet points."
)

if st.button("Summarize"):

    if text.strip() == "":
        st.warning("Please enter some text.")
    else:

        prompt = f"""
You are an AI text summarizer.

Summarize the following text according to the user's instruction.

User instruction:
{user_prompt}

Text:
{text}

Rules:
- Keep the original meaning.
- Remove unnecessary repetition.
- Use simple English.
- Include important facts, dates and numbers.
- Do not add information that is not present in the text.
"""

        url = "https://api.mistral.ai/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "mistral-small-latest",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.2
        }

        response = requests.post(
            url,
            headers=headers,
            json=data
        )

        if response.status_code == 200:
            result = response.json()

            summary = result["choices"][0]["message"]["content"]

            st.subheader("Summary")
            st.write(summary)

        else:
            st.error("Something went wrong.")
            st.write(response.text)
