import streamlit as st
from summarizer import summarize_text

# Configure Streamlit app
st.set_page_config(
    page_title="Text Summarizer",
    page_icon="✍️",
    layout="centered"
)

def main():
    st.title("📄 Text Summarizer")
    st.markdown("Automatically summarize text using extractive summarization powered by SpaCy")

    # Input text area
    text = st.text_area("Input Text:", height=300, placeholder="Paste your text here...")
    
    # Summary length slider
    summary_percent = st.slider(
        "Summary Length (% of original):",
        min_value=10,
        max_value=50,
        value=30,
        step=5
    ) / 100

    if st.button("Generate Summary"):
        if not text.strip():
            st.warning("Please enter some text to summarize")
        else:
            with st.spinner("Generating summary..."):
                summary = summarize_text(text, summary_percent)
                
            st.subheader("Summary:")
            st.write(summary)
            st.markdown(f"**Summary length:** {len(summary.split())} words "
                        f"(original: {len(text.split())} words)")

if __name__ == "__main__":
    main()