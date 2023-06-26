import requests
import pandas as pd
from bs4 import BeautifulSoup
import os
from llama_index import SimpleDirectoryReader,GPTListIndex,GPTVectorStoreIndex,LLMPredictor,PromptHelper,ServiceContext,StorageContext
from langchain import OpenAI

import openai
import llama_index

# from main import secret_key
# with open('key.txt','r') as f:

#     secret_key=f.read().strip()
# os.environ["OPENAI_API_KEY"]=secret_key
secret_key = os.getenv('api_key')
from langchain import OpenAI

Base_Dir=os.getcwd()

from PyPDF2 import PdfReader,PdfWriter



def get_chat_response(question):
    # API endpoint
    url = 'https://api.openai.com/v1/chat/completions'

    # Your OpenAI API key
    api_key = secret_key

    # Request headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    # Request payload
    payload = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'system', 'content': 'You are a helpful assistant.'},
                     {'role': 'user', 'content': question}]
    }

    # Send POST request to the API
    response = requests.post(url, headers=headers, json=payload)

    # Parse the response
    data = response.json()
    
    
    reply= data['choices'][0]['message']['content']

    # Get the model's reply
#     reply = data['choices'][0]['message']['content']

    return reply


def company_with_url(company_name):
    csv_path=os.path.join(Base_Dir,'companies_data.csv')
    from sentence_transformers import SentenceTransformer,util
    encode_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    df=pd.read_csv(csv_path)
    companies=list(df['company'])
    companies_urls=list(df['screener url'])
    encoded_names=encode_model.encode(companies)

    cos=util.cos_sim(encode_model.encode(company_name.split()[0]),encoded_names)

        
    m=0
    index=0
    for i in range(len(cos[0])):

        if m<cos[0][i].item():
            index=i
            m=cos[0][i]

    company=companies[index]
    screener_url=companies_urls[index]

    return (company,screener_url)


def report_url(url):

    soup_annual=BeautifulSoup(requests.get(url).content,'html.parser')
    annual_urls=[i.get('href') for i in soup_annual.find_all('a')]

    annual_reports=[]
    for i in annual_urls:
        if 'Annual' in i and '#' not in i:
            annual_reports.append(i)

    annual_report_2022=annual_reports[0]

    return annual_report_2022







def autodownload_report(url,company):

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'
    }
    
    response = requests.get(url, stream=True,headers=headers)

    folder_path=os.path.join(Base_Dir,f'Annual_reports/{company}_report')

    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
        print('folder created')
        pdf_path=os.path.join(Base_Dir,f'{company}_2022.pdf')
        # print(pdf_path)
        with open(pdf_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
        
    return 



def pdf2txt(pdf_path,company):

    if not os.path.exists(os.path.join(Base_Dir,f'Annual_reports/{company}_report/{company}_2022.txt')):

        titles = ['STANDALONE BALANCE SHEET', 'STANDALONE STATEMENT OF PROFIT AND LOSS', 'Balance Sheet', 'Balance Sheet (contd.)', 'Statement of Profit and Loss', 'Statement of Profit and Loss (contd.)']   
        with open(pdf_path, 'rb') as pdf_file:
                # Create a PDF reader object
                pdf_reader = PdfReader(pdf_file)
                text=''
                pdf_writer = PdfWriter()
                page_no=0

                for page in pdf_reader.pages:

                    page_content=page.extract_text()
                    page_no+=1
                    for word in titles:
                        if word in page_content:
                            # print(page_no)
                            text+=page.extract_text()
                            pdf_writer.add_page(page)
        
        with open(f'{company}_imp.pdf', 'wb') as output_file:
            pdf_writer.write(output_file)

        txt_path=os.path.join(Base_Dir,f'Annual_reports/{company}_report/{company}_2022.txt')
        with open(txt_path,'w',encoding='utf-8') as f:
            f.write(text)
        print('created txt file')
        pdf_path=os.path.join(Base_Dir,f'{company}_2022.pdf')
        os.remove(pdf_path)

        print('removed pdf file')

    return 

import base64
def display_pdf(pdf_file):
    with open(pdf_file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="500" type="application/pdf"></iframe>'
    
    return pdf_display

def create_index(company):

    import openai

    # api_key = "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"
    openai.api_key = secret_key


    
    vstore_path=os.path.join(Base_Dir,f'vector_stores/{company}_vstore')
    doc_path=os.path.join(Base_Dir,f'Annual_reports/{company}_report')
    if not os.path.exists(vstore_path):

        os.mkdir(vstore_path)
        max_input=4096
        tokens=200
        chunk_size=600
        max_chunk_overlap=20
        
        promptHelpter=PromptHelper(max_input,max_chunk_overlap,chunk_size_limit=chunk_size)
        
        openai.api_key=secret_key
        llmPredictor=LLMPredictor(llm=OpenAI(temperature=0,model_name='text-ada-001',max_tokens=tokens))
        
        docs=SimpleDirectoryReader(doc_path).load_data()
        
        service_context=ServiceContext.from_defaults(llm_predictor=llmPredictor,prompt_helper=promptHelpter)
        openai.api_key=secret_key
        vectorIndex=GPTVectorStoreIndex.from_documents(documents=docs)
        

        

        vectorIndex.storage_context.persist(persist_dir=vstore_path)

    return 


def load_index(vstore_path):


# rebuild storage context
    storage_context = StorageContext.from_defaults(persist_dir=vstore_path)
    # load index
    index = llama_index.load_index_from_storage(storage_context)

    return index

# print(index)

def give_answer(index,que):

    return index.as_query_engine().query(que)


def answerMe(question,company):

    vstore_path=os.path.join(Base_Dir,f'vector_stores/{company}_vstore')
    storage_context=StorageContext.from_defaults(persist_dir=vstore_path)
#     index=load_index_from_storage(storage_context)
    index=llama_index.load_index_from_storage(storage_context)
    query_engine=index.as_query_engine()
    response=query_engine.query(question)
    
    return response.response


def balance(url):
    dfs = pd.read_html(url)

    return dfs[6]
def shareholding(url):
    dfs = pd.read_html(url)

    return dfs[10]
def balance(url):
    dfs = pd.read_html(url)

    return dfs[6]
