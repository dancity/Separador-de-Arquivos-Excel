import streamlit as st
import pandas as pd
from io import BytesIO
import zipfile
from limpar_nomes import limpar_nome_arquivo

st.set_page_config(page_title="Separador de Arquivos", layout="centered")
st.title('Separador de arquivos')
st.write('Esse aplicativo separa seu arquivo do Excel/CSV em vários arquivos baseado em uma coluna escolhida.')
st.markdown('Desenvolvido por **Matheus Leão Rangel**')

formats = ['xlsx', 'xls', 'csv']
uploaded_file = st.file_uploader("Escolha seu arquivo (Excel ou CSV) para separação", type=formats)

@st.cache_data
def load_data(file, file_type):
    """Carrega o DataFrame a partir do arquivo informado."""
    try:
        if file_type == 'csv':
            # Aqui poderíamos permitir que o usuário escolhesse separador e decimal
            return pd.read_csv(file, sep=';', decimal=',')
        else:
            return pd.read_excel(file)
    except Exception as e:
        st.error(f"Erro ao carregar arquivo: {e}")
        return pd.DataFrame()

def generate_excel_file(dataframe):
    """Gera um arquivo Excel em memória a partir de um DataFrame."""
    excel_buffer = BytesIO()
    dataframe.to_excel(excel_buffer, index=False, engine='openpyxl')
    excel_buffer.seek(0)
    return excel_buffer

def create_zip_from_subsets(df, column):
    """Cria um arquivo zip em memória contendo um arquivo Excel para cada subset do DataFrame."""
    unique_values = df[column].unique()
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
        for value in unique_values:
            subset_df = df[df[column] == value]
            file_name = f"{limpar_nome_arquivo(value)}.xlsx"
            excel_buffer = generate_excel_file(subset_df)
            zip_file.writestr(file_name, excel_buffer.getvalue())
    zip_buffer.seek(0)
    return zip_buffer, unique_values

def generate_individual_files(df, column):
    """Gera botões de download individuais para cada subset do DataFrame."""
    unique_values = df[column].unique()
    progress_bar = st.progress(0)
    total = len(unique_values)
    for i, value in enumerate(unique_values, start=1):
        subset_df = df[df[column] == value]
        file_name = f"{limpar_nome_arquivo(value)}.xlsx"
        excel_buffer = generate_excel_file(subset_df)
        st.download_button(
            label=f"Baixar {file_name}",
            data=excel_buffer,
            file_name=file_name,
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        progress_bar.progress(i / total)

if uploaded_file is not None:
    file_type = 'csv' if uploaded_file.name.endswith('.csv') else 'excel'
    df = load_data(uploaded_file, file_type)

    if not df.empty:
        st.title('Pré-visualizar tabela')
        st.dataframe(df)

        # Selecionar a coluna para separação
        selected_column = st.selectbox('**Selecione a coluna para separar os arquivos:**', df.columns)

        if selected_column:
            unique_values = df[selected_column].unique()
            output_count = len(unique_values)
            st.write(f'Serão criados **{output_count}** arquivos.')

            with st.expander('Ver nomes dos arquivos gerados'):
                output_filenames = [f"{limpar_nome_arquivo(val)}.xlsx" for val in unique_values]
                st.table(output_filenames)

            baixar_todos = st.checkbox("Gerar um único arquivo ZIP com todos os arquivos")

            # Botão para gerar os arquivos
            if st.button('Gerar arquivos'):
                with st.spinner('Gerando arquivos... por favor, aguarde'):
                    if baixar_todos:
                        # Gera o arquivo ZIP
                        zip_buffer, unique_values = create_zip_from_subsets(df, selected_column)
                        st.download_button(
                            label="Baixar ZIP",
                            data=zip_buffer,
                            file_name="arquivos_separados.zip",
                            mime="application/zip"
                        )
                    else:
                        # Oferece o download individual
                        generate_individual_files(df, selected_column)
                st.success('Arquivos gerados com sucesso!')
