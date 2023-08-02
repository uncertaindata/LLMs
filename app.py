from dotenv import load_dotenv
import os
import streamlit as st
import webbrowser
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.callbacks import get_openai_callback
import openai
from key_validation import is_api_key_valid
def open_support_ticket():
    email_link = "mailto:theuncertaindatascientist@gmail.com"
    webbrowser.open(email_link)


def funct():
    # load_dotenv()
    # print('load_dotenv current env variable', os.getenv('OPENAI_API_KEY'))
    st.set_page_config(page_title = 'Ask your PDF')
    st.header('Ask your PDF')
    user_input = st.text_input("Enter your OPENAI key:", type='password')
    # key_entered = st.button('Ready!')

    # if key_entered:
    os.environ['OPENAI_API_KEY'] = user_input
    openai.api_key = os.getenv('OPENAI_API_KEY')
    api_key_valid = is_api_key_valid()
    print("API key is valid:", api_key_valid)
    # st.write('API validated')
    if not api_key_valid:
        st.write('Enter Correct Key')
        st.write(user_input)
    else:
        st.write('API validated')
        # print(user_input)
        # os.environ["OPENAI_API_KEY"] = user_input
        pdf = st.file_uploader('Upload your PDF', type='pdf')


        text = ''
        if pdf is not None:
            pdf_reader = PdfReader(pdf)
            # print(pdf_reader)
            
            for page in pdf_reader.pages:
                text +=page.extract_text()
            # st.write(text)


            #we cannot feed text directly to a language model, its too big!
            #divide text to chunks -> identify relevant chuncks(based on semantic similarity wrt question) and answer based on these chunks
            text_splitter = CharacterTextSplitter(
                separator='\n',
                chunk_size = 1000,
                chunk_overlap = 200,
                length_function = len
            )
            chunks = text_splitter.split_text(text)
            # st.write(chunks)
            # for chunk in chunks:
            #     st.write(chunk)
            #     st.write('-------------------------------')

            embeddings = OpenAIEmbeddings()
            with get_openai_callback() as cb:
                knowledge_base = FAISS.from_texts(chunks,embeddings)
                print('Created embeddings')
                print(cb)
            # user_question = st.text_input('Enter Your Question')
            # prev_qry = ""
            user_question = st.text_input('Enter Your Question')
            print('Waiting untill search button is pressed to save cost')
            #simply using st.text_input ran the chain multiple times and incurred enormous cost
            if st.button('Search') and user_question!='':
                docs = knowledge_base.similarity_search(user_question)
                # st.write(docs)
                llm = OpenAI()
                chain = load_qa_chain(llm=llm,chain_type='stuff')
                # query = PromptTemplate.format_prompt('As an AI model use the information given in docs and answer the question')
                with get_openai_callback() as cb:
                    response = chain.run(input_documents = docs, question = user_question)
                    print(cb)
                st.write(response)
            else:
                st.write('No questions were asked')    
                
            # Display search results for user_query
            #     if user_question:
            #         docs = knowledge_base.similarity_search(user_question)
            #         # st.write(docs)
            #         llm = OpenAI()
            #         chain = load_qa_chain(llm=llm,chain_type='stuff')
            #         # query = PromptTemplate.format_prompt('As an AI model use the information given in docs and answer the question')
            #         with get_openai_callback() as cb:
            #             response = chain.run(input_documents = docs, question = user_question)
            #             print(cb)
            #         st.write(response)






    st.button("Contact us!", on_click=open_support_ticket)

if __name__ == '__main__':
    # is_api_key_valid('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')
    funct()