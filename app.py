import streamlit as st
import requests

st.set_page_config(
    page_title="Mistral AI Text Summarizer",
    page_icon="📝"
)

st.title("📝 Mistral AI Text Summarizer")
st.write("Summarize your text using Mistral AI.")

# Paste your NEW Mistral API key here
API_KEY = "mstrl_6RuhTCm5dZdkfcqC2akL314wwLHyW5W6_0e2bQY"


# Text input
text = st.text_area(
    "Enter your text",
    height=300,
    placeholder="Paste your long text here..."
)

# Summarization prompt
user_prompt = st.text_input(
    "Enter your summarization prompt",
    "Summarize this text in 5 simple bullet points."
)


# Button
if st.button("✨ Summarize"):

    if not text.strip():
        st.warning("Please enter some text.")

    elif API_KEY == "YOUR_NEW_MISTRAL_API_KEY":
        st.error("Please enter your Mistral API key in app.py.")

    else:

        prompt = f"""
You are an AI text summarizer.

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
            "temperature": 0.2,
            "max_tokens": 500
        }

        try:

            with st.spinner("Generating summary..."):

                response = requests.post(
                    url,
                    headers=headers,
                    json=data,
                    timeout=60
                )

            if response.status_code == 200:

                result = response.json()

                summary = result["choices"][0]["message"]["content"]

                st.subheader("📌 Summary")
                st.write(summary)

            elif response.status_code == 429:

                st.error("❌ Mistral API Rate Limit Exceeded.")

                st.warning(
                    "Your Mistral API account has reached its "
                    "current request or token limit. "
                    "Please wait and try again later."
                )

                st.write("Mistral response:")
                st.code(response.text)

            elif response.status_code == 401:

                st.error("❌ Invalid API Key.")

                st.info(
                    "Create a new Mistral API key and replace "
                    "YOUR_NEW_MISTRAL_API_KEY in app.py."
                )

            elif response.status_code == 400:

                st.error("❌ Bad Request.")

                st.code(response.text)

            else:

                st.error(
                    f"❌ API Error: {response.status_code}"
                )

                st.code(response.text)

        except requests.exceptions.Timeout:

            st.error(
                "⏳ Request timed out. Please try again."
            )

        except requests.exceptions.ConnectionError:

            st.error(
                "🌐 Could not connect to Mistral API. "
                "Check your internet connection."
            )

        except Exception as e:

            st.error(f"❌ Error: {e}")
