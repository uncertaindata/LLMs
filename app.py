from dotenv import load_dotenv
import os
import streamlit as st
from PyPDF2 import PdfReader
def funct():
    load_dotenv()

    st.set_page_config(page_title = 'Ask your PDF')
    st.header('Ask your PDF')
    st.text_input('Enter Your Question')
    pdf = st.file_uploader('Upload your PDF', type='pdf')
    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        # print(pdf_reader)
        text = ''
        for page in pdf_reader.pages:
            text +=page.extract_text()
        st.write(text)


if __name__ == '__main__':
    funct()
