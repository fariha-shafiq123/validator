import streamlit as st
from lxml import etree
import io

# Page Layout & Styling
st.set_page_config(page_title="XML Validator", layout="centered")

st.markdown("""
    <style>
        body {
            font-family: Arial, sans-serif;
        }
        .stButton>button {
            width: 100%;
            background-color: #28a745;
            color: white;
            border-radius: 10px;
            font-size: 16px;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #218838;
        }
        .success-box {
            background: #e6ffe6;
            color: #007f00;
            padding: 14px;
            border-radius: 10px;
            font-weight: bold;
        }
        .error-box {
            background: #ffebeb;
            color: #b30000;
            padding: 14px;
            border-radius: 10px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# App Title
st.title("📝 XML Validator with XSD")
st.subheader("Upload your XML and XSD files to check if they are valid.")

# File Uploaders
xml_file = st.file_uploader("📂 Upload XML File", type=["xml"])
xsd_file = st.file_uploader("📂 Upload XSD File", type=["xsd"])

# Function to Validate XML against XSD
def validate_xml(xml_content, xsd_content):
    try:
        xml_doc = etree.parse(xml_content)
        xsd_doc = etree.XMLSchema(etree.parse(xsd_content))

        if xsd_doc.validate(xml_doc):
            return '<div class="success-box">✅ XML is valid! 🎉</div>'
        else:
            errors = xsd_doc.error_log
            if errors:
                error_messages = "<ul>"
                for error in errors:
                    error_messages += f"<li>❌ <b>Line {error.line}:</b> {error.message}</li>"
                error_messages += "</ul>"
                return f'<div class="error-box">⚠️ XML Validation Failed! Fix these errors:</div>{error_messages}'
            else:
                return '<div class="error-box">❌ XML is NOT valid, but no detailed errors were found.</div>'
    except Exception as e:
        return f'<div class="error-box">⚠️ An error occurred: {str(e)}</div>'

# Validate Button
if st.button("✅ Validate XML"):
    if not xml_file or not xsd_file:
        st.markdown('<div class="error-box">⚠️ Please upload both XML and XSD files first.</div>', unsafe_allow_html=True)
    else:
        xml_stream = io.BytesIO(xml_file.read())
        xsd_stream = io.BytesIO(xsd_file.read())

        result = validate_xml(xml_stream, xsd_stream)
        st.markdown(result, unsafe_allow_html=True)
