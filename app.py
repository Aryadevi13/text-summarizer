import streamlit as st
from txtai.pipeline import Summary
from PyPDF2 import PdfReader
import requests
from bs4 import BeautifulSoup

# Set page configuration
st.set_page_config(layout="wide")

# Function to summarize text
@st.cache_resource
def text_summary(text, maxlength=None):
    summary = Summary()
    result = summary(text)
    return result

# Function to extract text from URL
def extract_text_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract text from paragraphs and headers
        paragraphs = soup.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6"])
        text = "\n".join([p.get_text() for p in paragraphs])
        
        return text
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

# Function to extract text from PDF
def extract_text_from_pdf(file_path):
    with open(file_path, "rb") as f:
        reader = PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

# Main function
def main():
    st.title("Document Summarization App")
    st.sidebar.title("Options")
    choice = st.sidebar.selectbox("Select your choice", ["Summarize Text", "Summarize URL", "Summarize Document"])

    if choice == "Summarize Text":
        st.subheader("Summarize Text using txtai")
        input_text = st.text_area("Enter your text here")
        if st.button("Summarize Text"):
            if input_text:
                st.markdown("**Your Input Text**")
                st.info(input_text)
                result = text_summary(input_text)
                st.markdown("**Summary Result**")
                st.success(result)
            else:
                st.warning("Please enter some text to summarize.")

    elif choice == "Summarize URL":
        st.subheader("Summarize URL Content using txtai")
        url = st.text_input("Enter the URL")
        if st.button("Summarize URL"):
            if url:
                st.info("Extracting content from the URL...")
                extracted_text = extract_text_from_url(url)
                if extracted_text:
                    st.markdown("**Extracted Text is Below:**")
                    st.info(extracted_text)
                    st.markdown("**Summary Result**")
                    url_summary = text_summary(extracted_text)
                    st.success(url_summary)
            else:
                st.warning("Please enter a URL to summarize.")

    elif choice == "Summarize Document":
        st.subheader("Summarize Document using txtai")
        input_file = st.file_uploader("Upload your document here", type=['pdf'])
        if st.button("Summarize Document"):
            if input_file:
                with open("doc_file.pdf", "wb") as f:
                    f.write(input_file.getbuffer())
                st.info("File uploaded successfully")
                extracted_text = extract_text_from_pdf("doc_file.pdf")
                st.markdown("**Extracted Text is Below:**")
                st.info(extracted_text)
                st.markdown("**Summary Result**")
                doc_summary = text_summary(extracted_text)
                st.success(doc_summary)
            else:
                st.warning("Please upload a PDF document to summarize.")

if __name__ == "__main__":
    main()
