import streamlit as st

import os

import requests
import pandas as pd 
import numpy as np
from bs4 import BeautifulSoup
import pypdf
import llama_index
import os

# with open('key.txt','r') as f:

#     secret_key=f.read().strip()




from views import get_chat_response,company_with_url,report_url,autodownload_report,pdf2txt,create_index,answerMe,balance,shareholding,display_pdf,load_index,give_answer,api_status
Base_Dir=os.getcwd()
st.header('Financial Bot')

query=st.text_input('***tell name of company***')

secret_key = st.text_input('put your api key here')

press=st.button('click here')

if not api_status(secret_key):
    st.write('Api key is not valid')
    st.stop()

if press:

    st.write('confirm query :  ',query)


    company_name=get_chat_response(query+'\n \n give acutal name of this company in only one or two words ',secret_key)

  
    if not company_name:
        st.stop()

    st.write('company name :',company_name)
    full_company_name,screener_url=company_with_url(company_name)
    

    st.write('company from our database:',full_company_name)

    company=full_company_name.split(' ')[0]

    import time

    # time.sleep(10)


    # st.write('***if you have annual report of it then you can upload it***')
    # yes_no=st.button('Yes')
    # not_pdf=st.button('No')
  

    if None:
        import base64

        def download_file(file,company):
            """Downloads a file to a local folder."""
            filepath=os.path.join(Base_Dir,f'{company}_2022.pdf')
            with open(filepath, "wb") as f:
                f.write(file.read())
            return filepath

        uploaded_file = st.file_uploader("Upload a file", type=["pdf"])
        if uploaded_file is not None:
            pdf_file_path = download_file(uploaded_file,company)





    else:


        st.write('Url of company:',screener_url)
        
        

        st.write('Balance Sheet from Screener Website:')
        st.write(balance(screener_url))

        st.write('shareholding from Screener Website:')
        st.write(shareholding(screener_url))


        annual_report_url=report_url(screener_url)

        st.write(f'link of annual report 2022 of {full_company_name}',annual_report_url)

        

        st.write('annual report download stared ...')
        autodownload_report(annual_report_url,company)

        st.write('download successful')


    
    

    pdf_path=os.path.join(Base_Dir,f'{company}_2022.pdf')
    
    

    pdf2txt(pdf_path,company)

    st.write('report deleted and important data is stored in txt file ')

    st.write('this is pages of anuual report that contains important data')

    # pdf_display=display_pdf(f'{company}.pdf')
    import base64
    def display_pdf(pdf_file):
        with open(pdf_file, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="500" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
        return 
    display_pdf(f'{company}_imp.pdf')

    import openai

    openai.api_key = secret_key


    
    st.write('creating vector store and storing data in it')
    create_index(company,secret_key)

    st.write('vector store created succesfully ! ')



    import re
    def extract_number(string):
        """Extracts the number from the string."""
        regex = r"\d+,\d{3}"
        match = re.search(regex, string)
        if match:
            return match.group(0)
        else:
            return None

    questions = [
        "please read the Balance Sheet provided in pdf and fetch the value of Total non - current assets for Mar 2023. fetch only value",
        # "please read the Balance Sheet provided in pdf and fetch the value of Total current assets for Mar 2023. fetch only value",
        # "please read the Balance Sheet provided in pdf and fetch the value of Total assets for Mar 2023. fetch only value",
        # "please read the Balance Sheet provided in pdf and fetch the value of Total equity for Mar 2023. fetch only value",
        # "please read the Balance Sheet provided in pdf and fetch the value of Total non-current liabilities for Mar 2023. fetch only value",
        # "please read the Balance Sheet provided in pdf and fetch the value of Total current liabilities for Mar 2023. fetch only value",
        # "please read the Balance Sheet provided in pdf and fetch the value of Total equity and liabilities for Mar 2023. fetch only value",
        # "please read the Balance Sheet provided in pdf and fetch the value of Total income for Mar 2023. fetch only value",
        # "please read the Balance Sheet provided in pdf and fetch the value of Total expenses for Mar 2023. fetch only value",
        # "please read the Balance Sheet provided in pdf and fetch the value of Profit before tax . fetch only value",
        # "please read the Balance Sheet provided in pdf and fetch the value of Profit for the year for Mar 2023. fetch only value",
        # "please read the Balance Sheet provided in pdf and fetch the value of Total comprehensive income for the year for Mar 2023. fetch only value",
        # "please read the Balance Sheet provided in pdf and fetch the value of tax applied for the year for Mar 2023. fetch only value"
    ]

    vstore_path=os.path.join(Base_Dir,f'vector_stores/{company}_vstore')

    index=load_index(vstore_path)


    data_dict=dict()
    # key=['total non-current assets','total current assests','total asset for march','total equity','Total non-current liabilities','Total current liabilities','Total equity and liabilities','Total income','Total expenses','Profit before tax','Profit for the year','comprehensive income','tax']
    
    key=['total non-current assets']
    for i in range(len(questions)):
        ans=give_answer(index,questions[i]).response
        
        
        if ans:
            
            ans=ans.replace('\n','')
            data_dict[key[i]]=ans
            st.write(f'{key[i]} => {ans} ')
        else:
            data_dict[key[i]]=ans

            st.write(f'{key[i]} => {ans} ')

    def final_func(sen):
    
        ans=''
        for i in sen:
            if i.isdigit() or i==',':
                ans+=i
        return ans
    
    df=pd.DataFrame({f'{company}':data_dict.keys(),'2022':data_dict.values()})
    df['2022']=df['2022'].apply(final_func)


    st.write(df)

    csv_data = df.to_csv(index=False)
    st.download_button(label='Download CSV', data=csv_data, file_name=f'{company}_data.csv', mime='text/csv')




st.write('thanks for visiting us !!!')
