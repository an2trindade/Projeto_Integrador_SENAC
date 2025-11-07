"""
Utilitários para consulta de APIs externas
"""
import requests
import re
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)


def limpar_cnpj(cnpj_raw):
    """Remove caracteres não numéricos do CNPJ"""
    return re.sub(r'\D', '', cnpj_raw or '')


def validar_cnpj_formato(cnpj):
    """Valida se o CNPJ tem 14 dígitos"""
    cnpj_limpo = limpar_cnpj(cnpj)
    return len(cnpj_limpo) == 14


def buscar_cnpj_receita_ws(cnpj):
    """
    Busca dados do CNPJ na API ReceitaWS
    
    Args:
        cnpj (str): CNPJ com ou sem formatação
        
    Returns:
        dict: Dados da empresa ou None se não encontrado
        
    Example:
        cnpj = "19131243000197"
        dados = buscar_cnpj_receita_ws(cnpj)
        if dados:
            print(dados["nome"])
    """
    cnpj_limpo = limpar_cnpj(cnpj)
    
    if not validar_cnpj_formato(cnpj_limpo):
        logger.warning(f"CNPJ inválido: {cnpj}")
        return None
    
    try:
        url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj_limpo}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        dados = response.json()
        
        # Verifica se a API retornou erro
        if dados.get("status") == "ERROR":
            logger.warning(f"Erro da API ReceitaWS: {dados.get('message', 'Erro desconhecido')}")
            return None
            
        return dados
        
    except requests.exceptions.Timeout:
        logger.error(f"Timeout ao buscar CNPJ {cnpj_limpo}")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao buscar CNPJ {cnpj_limpo}: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Erro inesperado ao buscar CNPJ {cnpj_limpo}: {str(e)}")
        return None


def buscar_cnpj_brasil_api(cnpj):
    """
    Busca dados do CNPJ na API BrasilAPI
    
    Args:
        cnpj (str): CNPJ com ou sem formatação
        
    Returns:
        dict: Dados da empresa ou None se não encontrado
    """
    cnpj_limpo = limpar_cnpj(cnpj)
    
    if not validar_cnpj_formato(cnpj_limpo):
        logger.warning(f"CNPJ inválido: {cnpj}")
        return None
    
    try:
        url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj_limpo}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        dados = response.json()
        return dados
        
    except requests.exceptions.Timeout:
        logger.error(f"Timeout ao buscar CNPJ {cnpj_limpo} na BrasilAPI")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao buscar CNPJ {cnpj_limpo} na BrasilAPI: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Erro inesperado ao buscar CNPJ {cnpj_limpo} na BrasilAPI: {str(e)}")
        return None


def buscar_cnpj_completo(cnpj):
    """
    Busca dados do CNPJ tentando primeiro BrasilAPI e depois ReceitaWS como fallback
    
    Args:
        cnpj (str): CNPJ com ou sem formatação
        
    Returns:
        dict: Dados da empresa padronizados ou None se não encontrado
    """
    # Tenta BrasilAPI primeiro
    dados = buscar_cnpj_brasil_api(cnpj)
    
    if dados:
        # Padroniza resposta da BrasilAPI
        return {
            'cnpj': dados.get('cnpj', ''),
            'nome': dados.get('razao_social', ''),
            'razao_social': dados.get('razao_social', ''),
            'fantasia': dados.get('nome_fantasia', ''),
            'situacao': dados.get('descricao_situacao_cadastral', ''),
            'endereco': dados.get('logradouro', ''),
            'numero': dados.get('numero', ''),
            'complemento': dados.get('complemento', ''),
            'bairro': dados.get('bairro', ''),
            'municipio': dados.get('municipio', ''),
            'uf': dados.get('uf', ''),
            'cep': dados.get('cep', ''),
            'telefone': dados.get('ddd_telefone_1', ''),
            'email': dados.get('email', ''),
            'data_abertura': dados.get('data_inicio_atividade', ''),
            'fonte': 'BrasilAPI'
        }
    
    # Fallback para ReceitaWS
    dados = buscar_cnpj_receita_ws(cnpj)
    
    if dados:
        # Padroniza resposta da ReceitaWS
        return {
            'cnpj': dados.get('cnpj', ''),
            'nome': dados.get('nome', ''),
            'razao_social': dados.get('nome', ''),
            'fantasia': dados.get('fantasia', ''),
            'situacao': dados.get('situacao', ''),
            'endereco': dados.get('logradouro', ''),
            'numero': dados.get('numero', ''),
            'complemento': dados.get('complemento', ''),
            'bairro': dados.get('bairro', ''),
            'municipio': dados.get('municipio', ''),
            'uf': dados.get('uf', ''),
            'cep': dados.get('cep', ''),
            'telefone': dados.get('telefone', ''),
            'email': dados.get('email', ''),
            'data_abertura': dados.get('abertura', ''),
            'fonte': 'ReceitaWS'
        }
    
    return None


def formatar_cnpj(cnpj):
    """
    Formata CNPJ no padrão XX.XXX.XXX/XXXX-XX
    
    Args:
        cnpj (str): CNPJ apenas com números
        
    Returns:
        str: CNPJ formatado ou string vazia se inválido
    """
    cnpj_limpo = limpar_cnpj(cnpj)
    
    if not validar_cnpj_formato(cnpj_limpo):
        return ''
    
    return f"{cnpj_limpo[:2]}.{cnpj_limpo[2:5]}.{cnpj_limpo[5:8]}/{cnpj_limpo[8:12]}-{cnpj_limpo[12:14]}"