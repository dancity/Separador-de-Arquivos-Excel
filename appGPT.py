import streamlit as st
import numpy as np
import pandas as pd
from io import BytesIO
import zipfile
from limpar_nomes import limpar_nome_arquivo

st.title('Separador de arquivos')
st.write('Esse aplicativo separa seu arquivo do Excel em vários arquivos baseado na coluna que você escolher')
st.markdown('Desenvolvido por **Matheus Leão Rangel**')

formats = ['xlsx', 'xls', 'csv']
uploaded_file = st.file_uploader("Escolha seu arquivo de Excel para ser separado", type=formats)

# Usando o cache para evitar recarregamentos desnecessários
@st.cache_data
def load_data(file, file_type):
    if file_type == 'csv':
        return pd.read_csv(file, sep=';', decimal=',')
    else:
        return pd.read_excel(file)

if uploaded_file is not None:
    file_type = 'csv' if uploaded_file.name.endswith('.csv') else 'excel'
    df = load_data(uploaded_file, file_type)

    st.title('Pré-visualizar tabela')
    st.dataframe(df)

    selected_column = st.selectbox('Qual coluna você deseja usar para separar os arquivos?', df.columns)
    if selected_column:
        output_list = df[selected_column].unique()
        output_count = len(output_list)
        output_filenames = [str(limpar_nome_arquivo(filename)) + ".xlsx" for filename in output_list]
        st.markdown(f'Serão criados **{output_count}** arquivos no formato Excel.')

        with st.expander('Expanda para ver os arquivos'):
            st.table(output_filenames)

        baixar_todos = st.checkbox("Baixar todos os arquivos de uma vez (.zip)?")

        if st.button('Gerar arquivos'):
            with st.spinner('Gerando arquivos... por favor, aguarde'):
                progress_bar = st.progress(0)
                
                # Preparando o arquivo .zip
                if baixar_todos:
                    zip_buffer = BytesIO()
                    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
                        for i, file in enumerate(output_list, start=1):
                            df_output = df[df[selected_column] == file]
                            fileName = str(limpar_nome_arquivo(file)) + ".xlsx"
                            # Salvando cada DataFrame como um arquivo Excel em memória
                            excel_buffer = BytesIO()
                            df_output.to_excel(excel_buffer, index=False, engine='openpyxl')
                            excel_buffer.seek(0)
                            zip_file.writestr(fileName, excel_buffer.getvalue())
                            progress_bar.progress(i / output_count)
                    zip_buffer.seek(0)
                    st.download_button(
                        label="Baixar todos os arquivos (.zip)",
                        data=zip_buffer,
                        file_name="arquivos_separados.zip",
                        mime="application/zip"
                    )
                else:
                    for i, file in enumerate(output_list, start=1):
                        df_output = df[df[selected_column] == file]
                        fileName = str(limpar_nome_arquivo(file)) + ".xlsx"
                        textLabel = 'Baixar o arquivo: ' + fileName
                        output_file = BytesIO()
                        df_output.to_excel(output_file, index=False, engine='openpyxl')
                        output_file.seek(0)
                        st.download_button(
                            label=textLabel,
                            data=output_file,
                            file_name=fileName,
                            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                        )
                        progress_bar.progress(i / output_count)
                st.success('Todos os arquivos foram gerados!')
