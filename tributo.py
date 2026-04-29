import streamlit as st
import requests
import pandas as pd

st.set_page_config(layout="wide")

st.title('Consultar CNPJ a Tributar por CNAE')

cnpj = st.text_input('Digite o CNPJ da empresa, apenas números:',  placeholder='64396581000105')

if cnpj:
    r= requests.get(f'https://minhareceita.org/{cnpj}')

    if r.status_code != 200:
        st.error('Erro ao consultar o CNPJ. Por favor, tente novamente.')
    else:
        j= r.json()
        if len(j)==1:
            st.warning(j)
        else:
            l=[]
            l2=[]
            l.append(j["cnae_fiscal"])
            l2.append("cnae_fiscal")
            tamanho=len(j["cnaes_secundarios"])
            for i in range(tamanho):
                l.append(j["cnaes_secundarios"][i]['codigo'])
                l2.append("cnaes_secundarios")

            temp=pd.DataFrame({'CNAE':l,'Tipo':l2})
            df=pd.read_excel('CONSULTA CNAE para GLAUCEA.xlsx',sheet_name='ANEXO CTMI')
            df=df[df[0].isin(l)][[0,'RETORNO PARA CODCONT','UFITA/ANO\nALVARÁ']].sort_values(by='UFITA/ANO\nALVARÁ',ascending=False)
            df.columns=['CNAE','Descrição','Valor']
            df=df.merge(temp,on='CNAE',how='left')

            st.text(f'{cnpj} - {j["razao_social"]}')
            st.text(f'{j['uf']} - {j["municipio"]} - {j['bairro']} - {j['cep']}')
            st.text(f'{j["descricao_tipo_de_logradouro"]} {j["logradouro"]} N°{j["numero"]} complemento {j['complemento']}')
            st.dataframe(df, hide_index=True)

