import streamlit as st

st.title("AI Text Summarizer")
st.write("Enter a long text below, and get a concise summary!")

long_text = st.text_area("Enter text to summarize:", height=200)

max_length = st.slider("Max Summary Length", 50, 300, 130)
min_length = st.slider("Min Summary Length", 20, 100, 30)

# ✅ Try to load Hugging Face summarizer
@st.cache_resource
def load_summarizer():
    try:
        from transformers import pipeline
        return pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    except:
        return None  # fallback if fails

summarizer = load_summarizer()

# Button
if st.button("Summarize"):
    if long_text.strip():
        with st.spinner("Generating summary..."):

            # ✅ If real summarizer works
            if summarizer:
                summary = summarizer(
                    long_text,
                    max_length=max_length,
                    min_length=min_length,
                    do_sample=False
                )
                result = summary[0]['summary_text']

            # 🔥 Fallback (still keeps app running)
            else:
                sentences = long_text.split(".")
                result = ". ".join(sentences[:3])[:max_length]

        st.subheader("Summary:")
        st.success(result)
    else:
        st.warning("Please enter some text.")
