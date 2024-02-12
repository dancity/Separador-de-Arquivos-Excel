# Separador de Arquivos Excel com Streamlit

## Descrição
Este projeto é um aplicativo web construído com Streamlit que permite aos usuários carregar um arquivo Excel (suportando formatos `.xlsx`, `.xls`, e `.csv`) e separá-lo em vários arquivos com base nos valores únicos de uma coluna selecionada. O aplicativo oferece a opção de baixar os arquivos separados individualmente ou todos juntos em um arquivo `.zip`.

## Funcionalidades
- Carregamento de arquivos Excel ou CSV.
- Seleção da coluna base para separação dos dados.
- Pré-visualização dos dados carregados.
- Geração de arquivos Excel separados com base no valor único da coluna selecionada.
- Opção para baixar todos os arquivos gerados de uma vez como um `.zip`.
- Interface de usuário amigável com progresso de processamento.

## Tecnologias Utilizadas
- Streamlit
- Pandas
- Python 3
- OpenPyXL (para manipulação de arquivos Excel)