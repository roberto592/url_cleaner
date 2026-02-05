import streamlit as st
from urllib.parse import urlparse

# Add custom CSS for colors and fonts
st.markdown("""
    <style>
        /* Apply to the whole page */
        body {
            background-color: #13322E !important;  /* Set background color */
            color: #00DEBB !important;  /* Set font color */
            font-family: 'Atyp Text Medium', sans-serif !important;  /* Set default font */
        }

        /* Title styling */
        .title {
            font-family: 'Mazzard Medium', sans-serif;
            color: #00DEBB;
            font-size: 36px;
            text-align: center;
            margin-bottom: 20px;
        }

        /* Button styling */
        .stButton>button {
            background-color: #0D9276;
            color: white;
            font-family: 'Mazzard Medium', sans-serif;
            padding: 12px;
            border-radius: 8px;
            font-size: 16px;
        }
        .stButton>button:hover {
            background-color: #1EB9A0;
        }

        /* Text box styling */
        .stTextInput, .stTextArea {
            background-color: #F9F9F9;
            border-radius: 8px;
            border: 1px solid #717E95;
            font-family: 'Atyp Text Medium', sans-serif;
        }

        /* Final output styling */
        .output {
            background-color: #ECF7F6;
            color: #05444A;
            padding: 10px;
            border-radius: 8px;
            margin-top: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

# Display company logo at the top (adjust the path as necessary)
st.image("banner.png", width=900)  # Adjust the path and width as needed

# Title with custom class
st.markdown('<h1 class="title">The Sure Oak URL Cleaner</h1>', unsafe_allow_html=True)

# Function to clean URLs to show only the domain
def clean_urls(urls):
    cleaned_urls = []
    for url in urls:
        try:
            parsed_url = urlparse(url.strip())
            cleaned_urls.append(parsed_url.scheme + "://" + parsed_url.netloc + "/")
        except Exception as e:
            cleaned_urls.append("")
    return cleaned_urls

# Function to remove duplicates
def remove_duplicates(urls):
    return list(set(urls))

# Function to remove 'https://' or 'http://' prefix and 'www.'
def remove_https_and_www(urls):
    cleaned_urls = []
    for url in urls:
        url = url.replace("https://", "").replace("http://", "")
        if url.startswith("www."):
            url = url[4:]  # Remove 'www.'
        cleaned_urls.append(url)
    return cleaned_urls

# Initialize session_state for holding the URLs
if 'urls' not in st.session_state:
    st.session_state.urls = []

# Streamlit UI
input_urls = st.text_area("Paste URLs here (each URL on a new line):")

# Split input URLs into a list when the user enters them in the text box
urls_list = input_urls.splitlines()

# Automatically update session_state with the latest URLs entered only if input_urls is not empty
if input_urls.strip():
    st.session_state.urls = urls_list

# Checkboxes to select transformations
clean_checkbox = st.checkbox('Clean URLs (Show only domain)', value=False)
duplicate_checkbox = st.checkbox('Remove Duplicates', value=False)
https_www_checkbox = st.checkbox('Remove HTTPS and WWW Prefix', value=False)

# Create an empty container for results that will be filled after clicking the button
results_placeholder = st.empty()

# Apply selected transformations when the button is pressed
if st.button("Apply Changes"):
    if clean_checkbox:
        st.session_state.urls = clean_urls(st.session_state.urls)
    if duplicate_checkbox:
        st.session_state.urls = remove_duplicates(st.session_state.urls)
    if https_www_checkbox:
        st.session_state.urls = remove_https_and_www(st.session_state.urls)

    # Now show the results in the placeholder
    results_placeholder.text_area("Final Cleaned URLs:", "\n".join(st.session_state.urls), height=200)
