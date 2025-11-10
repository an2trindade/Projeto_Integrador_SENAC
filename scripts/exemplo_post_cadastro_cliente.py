#!/usr/bin/env python3
"""
Exemplo de POST das informações da busca do CNPJ nos campos do cadastro do cliente

Este script demonstra como fazer um POST completo com os dados obtidos da busca
de CNPJ para cadastrar um novo cliente no sistema.

Fluxo:
1. Buscar dados do CNPJ via API externa (GET /linhas/buscar-cnpj-api/)
2. Usar os dados obtidos para fazer POST no cadastro de cliente

Data: 2024
"""

import requests
import json
from datetime import datetime

# Configurações
BASE_URL = "http://localhost:8000"  # Ajuste conforme necessário
SESSION = requests.Session()

def autenticar(username, password):
    """
    Autentica no sistema Django e obtém o CSRF token
    """
    print("🔐 Realizando autenticação...")
    
    # Primeiro, obter a página de login para pegar o CSRF token
    login_page = SESSION.get(f"{BASE_URL}/linhas/login/")
    csrf_token = None
    
    # Extrair CSRF token do cookie ou HTML
    if 'csrftoken' in SESSION.cookies:
        csrf_token = SESSION.cookies['csrftoken']
    
    # Dados de login
    login_data = {
        'username': username,
        'password': password,
        'login_form': '1',
        'csrfmiddlewaretoken': csrf_token
    }
    
    # Fazer login
    response = SESSION.post(f"{BASE_URL}/linhas/login/", data=login_data)
    
    if response.status_code == 200 and 'dashboard' in response.url:
        print("✅ Autenticação realizada com sucesso!")
        return True
    else:
        print(f"❌ Falha na autenticação. Status: {response.status_code}")
        return False

def buscar_dados_cnpj(cnpj):
    """
    Busca dados do CNPJ via API externa
    
    Args:
        cnpj (str): CNPJ para buscar (apenas dígitos)
    
    Returns:
        dict: Dados da empresa ou None se não encontrado
    """
    print(f"🔍 Buscando dados do CNPJ: {cnpj}")
    
    # Limpar CNPJ (apenas dígitos)
    cnpj_limpo = ''.join(filter(str.isdigit, cnpj))
    
    if len(cnpj_limpo) != 14:
        print("❌ CNPJ deve ter 14 dígitos")
        return None
    
    # Fazer requisição GET para buscar dados do CNPJ
    url = f"{BASE_URL}/linhas/buscar-cnpj-api/"
    params = {'cnpj': cnpj_limpo}
    
    try:
        response = SESSION.get(url, params=params)
        print(f"📡 Status da requisição: {response.status_code}")
        
        if response.status_code == 200:
            dados = response.json()
            if dados.get('success'):
                print("✅ Dados do CNPJ obtidos com sucesso!")
                print(f"📋 Fonte: {dados['dados'].get('fonte', 'N/A')}")
                return dados['dados']
            else:
                print(f"❌ Erro na API: {dados.get('error', 'Erro desconhecido')}")
                return None
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Erro na requisição: {str(e)}")
        return None

def cadastrar_cliente_post(dados_cnpj, dados_adicionais=None):
    """
    Faz POST para cadastrar cliente usando dados obtidos da busca CNPJ
    
    Args:
        dados_cnpj (dict): Dados obtidos da API de CNPJ
        dados_adicionais (dict): Dados adicionais do proprietário
    
    Returns:
        dict: Resultado do cadastro
    """
    print("📝 Preparando dados para cadastrar cliente...")
    
    # Obter CSRF token atual
    csrf_token = SESSION.cookies.get('csrftoken')
    
    # Construir endereço completo
    endereco_parts = []
    if dados_cnpj.get('endereco'):
        endereco_parts.append(dados_cnpj['endereco'])
    if dados_cnpj.get('numero'):
        endereco_parts.append(f"Nº {dados_cnpj['numero']}")
    if dados_cnpj.get('complemento'):
        endereco_parts.append(dados_cnpj['complemento'])
    if dados_cnpj.get('bairro'):
        endereco_parts.append(dados_cnpj['bairro'])
    if dados_cnpj.get('municipio'):
        endereco_parts.append(dados_cnpj['municipio'])
    if dados_cnpj.get('uf'):
        endereco_parts.append(dados_cnpj['uf'])
    if dados_cnpj.get('cep'):
        endereco_parts.append(f"CEP: {dados_cnpj['cep']}")
    
    endereco_completo = ', '.join(endereco_parts)
    
    # Dados do formulário para POST
    post_data = {
        'csrfmiddlewaretoken': csrf_token,
        
        # Dados da empresa (obtidos via CNPJ)
        'empresa': dados_cnpj.get('razao_social', ''),
        'cnpj': dados_cnpj.get('cnpj', ''),
        'razao_social': dados_cnpj.get('razao_social', ''),
        'fantasia': dados_cnpj.get('fantasia', ''),
        'endereco_completo': endereco_completo,
        'email': dados_cnpj.get('email', ''),
        
        # Dados do proprietário (informações adicionais)
        'contato': dados_adicionais.get('contato', '') if dados_adicionais else '',
        'telefone': dados_cnpj.get('telefone', ''),
        'nome_dono': dados_adicionais.get('nome_dono', '') if dados_adicionais else '',
        'cpf_dono': dados_adicionais.get('cpf_dono', '') if dados_adicionais else '',
        'data_nascimento_dono': dados_adicionais.get('data_nascimento_dono', '') if dados_adicionais else '',
        
        # Ação do formulário (ficar na página ou ir para nova linha)
        'next_action': 'stay'  # ou 'nova_linha'
    }
    
    print("📊 Dados preparados para POST:")
    for key, value in post_data.items():
        if key != 'csrfmiddlewaretoken':
            print(f"  {key}: {value}")
    
    # Fazer POST para cadastrar cliente
    url = f"{BASE_URL}/linhas/novo-cliente/"
    
    try:
        print("🚀 Enviando POST para cadastrar cliente...")
        response = SESSION.post(url, data=post_data)
        
        print(f"📡 Status da resposta: {response.status_code}")
        
        if response.status_code == 200:
            # Verificar se o cadastro foi bem-sucedido
            if 'cadastrado com sucesso' in response.text:
                print("✅ Cliente cadastrado com sucesso!")
                
                # Tentar extrair ID do cliente da mensagem de sucesso
                # (isso dependeria da implementação específica da view)
                return {
                    'success': True,
                    'message': 'Cliente cadastrado com sucesso',
                    'status_code': response.status_code
                }
            else:
                print("❌ Possível erro no cadastro (verifique formulário)")
                return {
                    'success': False,
                    'message': 'Erro no formulário ou validação',
                    'status_code': response.status_code
                }
        else:
            print(f"❌ Erro HTTP no cadastro: {response.status_code}")
            return {
                'success': False,
                'message': f'Erro HTTP: {response.status_code}',
                'status_code': response.status_code
            }
            
    except Exception as e:
        print(f"❌ Erro na requisição POST: {str(e)}")
        return {
            'success': False,
            'message': f'Erro na requisição: {str(e)}',
            'status_code': None
        }

def exemplo_completo():
    """
    Exemplo completo do fluxo: buscar CNPJ + cadastrar cliente
    """
    print("=" * 60)
    print("🎯 EXEMPLO COMPLETO: BUSCA CNPJ + CADASTRO CLIENTE")
    print("=" * 60)
    
    # Dados de exemplo
    cnpj_exemplo = "19131243000197"  # CNPJ de exemplo
    username = "admin"  # Ajuste conforme necessário
    password = "sua_senha"  # Ajuste conforme necessário
    
    # Dados adicionais do proprietário
    dados_proprietario = {
        'contato': 'João Silva',
        'nome_dono': 'João Silva Santos',
        'cpf_dono': '123.456.789-00',
        'data_nascimento_dono': '1980-05-15'
    }
    
    # 1. Autenticar no sistema
    if not autenticar(username, password):
        print("❌ Não foi possível prosseguir sem autenticação")
        return
    
    print("\n" + "-" * 50)
    
    # 2. Buscar dados do CNPJ
    dados_cnpj = buscar_dados_cnpj(cnpj_exemplo)
    if not dados_cnpj:
        print("❌ Não foi possível obter dados do CNPJ")
        return
    
    print(f"\n📋 Dados obtidos da empresa:")
    print(f"  Razão Social: {dados_cnpj.get('razao_social', 'N/A')}")
    print(f"  Nome Fantasia: {dados_cnpj.get('fantasia', 'N/A')}")
    print(f"  CNPJ: {dados_cnpj.get('cnpj', 'N/A')}")
    print(f"  Situação: {dados_cnpj.get('situacao', 'N/A')}")
    print(f"  Município: {dados_cnpj.get('municipio', 'N/A')}")
    print(f"  UF: {dados_cnpj.get('uf', 'N/A')}")
    
    print("\n" + "-" * 50)
    
    # 3. Cadastrar cliente com os dados obtidos
    resultado = cadastrar_cliente_post(dados_cnpj, dados_proprietario)
    
    print(f"\n📊 Resultado final:")
    print(f"  Sucesso: {resultado['success']}")
    print(f"  Mensagem: {resultado['message']}")
    print(f"  Status HTTP: {resultado['status_code']}")
    
    print("\n" + "=" * 60)
    print("🎉 PROCESSO CONCLUÍDO!")
    print("=" * 60)

def exemplo_dados_json():
    """
    Exemplo de como os dados ficam estruturados em JSON
    """
    print("\n" + "=" * 60)
    print("📋 EXEMPLO DE ESTRUTURA DOS DADOS")
    print("=" * 60)
    
    # Exemplo de dados retornados pela API de CNPJ
    dados_cnpj_exemplo = {
        "cnpj": "19131243000197",
        "nome": "EMPRESA EXEMPLO LTDA",
        "razao_social": "EMPRESA EXEMPLO LTDA",
        "fantasia": "Exemplo Corp",
        "situacao": "ATIVA",
        "endereco": "RUA DAS FLORES",
        "numero": "123",
        "complemento": "SALA 456",
        "bairro": "CENTRO",
        "municipio": "SAO PAULO",
        "uf": "SP",
        "cep": "01234567",
        "telefone": "1134567890",
        "email": "contato@exemplo.com.br",
        "data_abertura": "2020-01-15",
        "fonte": "BrasilAPI"
    }
    
    # Exemplo de dados do POST para cadastro
    dados_post_exemplo = {
        "csrfmiddlewaretoken": "abc123token456",
        "empresa": "EMPRESA EXEMPLO LTDA",
        "cnpj": "19.131.243/0001-97",
        "razao_social": "EMPRESA EXEMPLO LTDA",
        "fantasia": "Exemplo Corp",
        "endereco_completo": "RUA DAS FLORES, Nº 123, SALA 456, CENTRO, SAO PAULO, SP, CEP: 01234567",
        "email": "contato@exemplo.com.br",
        "contato": "João Silva",
        "telefone": "1134567890",
        "nome_dono": "João Silva Santos",
        "cpf_dono": "123.456.789-00",
        "data_nascimento_dono": "1980-05-15",
        "next_action": "stay"
    }
    
    print("📡 Dados retornados pela API de CNPJ:")
    print(json.dumps(dados_cnpj_exemplo, indent=2, ensure_ascii=False))
    
    print("\n📝 Dados enviados no POST para cadastro:")
    print(json.dumps(dados_post_exemplo, indent=2, ensure_ascii=False))
    
    print("\n🔗 URLs envolvidas:")
    print(f"  GET:  {BASE_URL}/linhas/buscar-cnpj-api/?cnpj=19131243000197")
    print(f"  POST: {BASE_URL}/linhas/novo-cliente/")

if __name__ == "__main__":
    print("🚀 SCRIPT DE EXEMPLO: POST CADASTRO CLIENTE COM DADOS CNPJ")
    print("=" * 60)
    
    # Mostrar exemplo dos dados estruturados
    exemplo_dados_json()
    
    print("\n\n💡 Para executar o exemplo completo, descomente a linha abaixo:")
    print("# exemplo_completo()")
    
    # Descomente para executar o exemplo real:
    # exemplo_completo()