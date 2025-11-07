"""
Script de teste para a API de busca de CNPJ
Para executar: python manage.py shell < test_cnpj_api.py
"""

# Importa as funções utilitárias
from linhas.utils import buscar_cnpj_receita_ws, buscar_cnpj_brasil_api, buscar_cnpj_completo

def test_cnpj_api():
    """Testa a API de busca de CNPJ"""
    
    # CNPJ de teste
    cnpj = "19131243000197"
    
    print("=" * 50)
    print("TESTE DA API DE BUSCA DE CNPJ")
    print("=" * 50)
    print(f"CNPJ de teste: {cnpj}")
    print()
    
    # Teste da ReceitaWS
    print("1. Testando ReceitaWS...")
    try:
        dados_receita = buscar_cnpj_receita_ws(cnpj)
        if dados_receita:
            print(f"✓ Nome/Razão Social: {dados_receita.get('nome', 'N/A')}")
            print(f"✓ Fantasia: {dados_receita.get('fantasia', 'N/A')}")
            print(f"✓ Situação: {dados_receita.get('situacao', 'N/A')}")
        else:
            print("✗ Não foi possível obter dados da ReceitaWS")
    except Exception as e:
        print(f"✗ Erro na ReceitaWS: {e}")
    
    print()
    
    # Teste da BrasilAPI
    print("2. Testando BrasilAPI...")
    try:
        dados_brasil = buscar_cnpj_brasil_api(cnpj)
        if dados_brasil:
            print(f"✓ Razão Social: {dados_brasil.get('razao_social', 'N/A')}")
            print(f"✓ Nome Fantasia: {dados_brasil.get('nome_fantasia', 'N/A')}")
            print(f"✓ Situação: {dados_brasil.get('descricao_situacao_cadastral', 'N/A')}")
        else:
            print("✗ Não foi possível obter dados da BrasilAPI")
    except Exception as e:
        print(f"✗ Erro na BrasilAPI: {e}")
    
    print()
    
    # Teste da função completa (com fallback)
    print("3. Testando função completa (com fallback)...")
    try:
        dados_completos = buscar_cnpj_completo(cnpj)
        if dados_completos:
            print(f"✓ Nome: {dados_completos.get('nome', 'N/A')}")
            print(f"✓ Razão Social: {dados_completos.get('razao_social', 'N/A')}")
            print(f"✓ Fantasia: {dados_completos.get('fantasia', 'N/A')}")
            print(f"✓ Situação: {dados_completos.get('situacao', 'N/A')}")
            print(f"✓ Endereço: {dados_completos.get('endereco', 'N/A')}")
            print(f"✓ Município: {dados_completos.get('municipio', 'N/A')}")
            print(f"✓ UF: {dados_completos.get('uf', 'N/A')}")
            print(f"✓ CEP: {dados_completos.get('cep', 'N/A')}")
            print(f"✓ Fonte: {dados_completos.get('fonte', 'N/A')}")
        else:
            print("✗ Não foi possível obter dados de nenhuma API")
    except Exception as e:
        print(f"✗ Erro na função completa: {e}")
    
    print()
    print("=" * 50)
    print("TESTE CONCLUÍDO")
    print("=" * 50)

# Executa o teste
if __name__ == "__main__":
    test_cnpj_api()