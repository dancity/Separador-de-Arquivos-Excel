import re

def limpar_nome_arquivo(nome):
    """
    Remove caracteres não seguros de nomes de arquivo.
    
    :param nome: O nome do arquivo a ser limpo.
    :return: Uma string com o nome do arquivo limpo.
    """
    # Lista de caracteres que você deseja permitir
    # Neste exemplo, estamos permitindo letras, números, espaços, hífens e sublinhados
    nome_limpo = re.sub(r'[^\w\s\-_]', '', str(nome))
    
    # Substitui espaços por sublinhados para evitar problemas com nomes de arquivo
    nome_limpo = re.sub(r'\s+', '_', nome_limpo)
    
    return nome_limpo