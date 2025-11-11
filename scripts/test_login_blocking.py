"""
Script para testar o bloqueio de login após 3 tentativas incorretas.
"""
import requests
from bs4 import BeautifulSoup

BASE_URL = "http://127.0.0.1:8000/linhas/login/"

def test_login_blocking():
    print("=" * 60)
    print("TESTE DE BLOQUEIO DE LOGIN")
    print("=" * 60)
    
    session = requests.Session()
    
    # Tentativa 1
    print("\n[Tentativa 1] Enviando credenciais incorretas...")
    response = session.get(BASE_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
    
    data = {
        'csrfmiddlewaretoken': csrf_token,
        'login_form': '1',
        'username': 'teste1',
        'password': 'senhaerrada123'
    }
    
    response = session.post(BASE_URL, data=data)
    if 'Usuário ou senha incorretos' in response.text:
        print("✓ Mensagem de erro exibida: 'Usuário ou senha incorretos'")
    else:
        print("✗ ERRO: Mensagem de erro não encontrada!")
        print(f"Status: {response.status_code}")
    
    # Tentativa 2
    print("\n[Tentativa 2] Enviando credenciais incorretas...")
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
    data['csrfmiddlewaretoken'] = csrf_token
    
    response = session.post(BASE_URL, data=data)
    if 'Usuário ou senha incorretos' in response.text:
        print("✓ Mensagem de erro exibida: 'Usuário ou senha incorretos'")
    else:
        print("✗ ERRO: Mensagem de erro não encontrada!")
    
    # Tentativa 3
    print("\n[Tentativa 3] Enviando credenciais incorretas...")
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
    data['csrfmiddlewaretoken'] = csrf_token
    
    response = session.post(BASE_URL, data=data)
    if 'Conta bloqueada por 15 minutos' in response.text:
        print("✓ BLOQUEIO ATIVADO! Mensagem exibida: 'Conta bloqueada por 15 minutos'")
        print("✓ Ícone de suporte deve estar visível")
    elif 'Usuário ou senha incorretos' in response.text:
        print("✗ ERRO: Deveria estar bloqueado mas ainda mostra erro de senha!")
    else:
        print("✗ ERRO: Nenhuma mensagem esperada encontrada!")
        print(f"Conteúdo parcial: {response.text[:500]}")
    
    # Tentativa 4 (deve continuar bloqueado)
    print("\n[Tentativa 4] Testando se bloqueio persiste...")
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_input = soup.find('input', {'name': 'csrfmiddlewaretoken'})
    if csrf_input:
        csrf_token = csrf_input['value']
        data['csrfmiddlewaretoken'] = csrf_token
        
        response = session.post(BASE_URL, data=data)
        if 'Conta bloqueada' in response.text:
            print("✓ Usuário continua bloqueado corretamente")
        else:
            print("✗ ERRO: Bloqueio não persistiu!")
    
    print("\n" + "=" * 60)
    print("TESTE CONCLUÍDO")
    print("=" * 60)
    print("\nPróximos passos:")
    print("1. Acesse http://127.0.0.1:8000/linhas/configuracoes/")
    print("2. Use o formulário 'Desbloquear Usuário'")
    print("3. Digite: teste1")
    print("4. Tente fazer login novamente com: teste1 / SenhaTeste123")

if __name__ == "__main__":
    try:
        test_login_blocking()
    except requests.exceptions.ConnectionError:
        print("ERRO: Não foi possível conectar ao servidor.")
        print("Certifique-se de que o servidor Django está rodando em http://127.0.0.1:8000/")
    except Exception as e:
        print(f"ERRO INESPERADO: {e}")
        import traceback
        traceback.print_exc()
