# -*- coding: utf-8 -*-
"""
Script de teste simples para a API de busca de CNPJ
"""

from linhas.utils import buscar_cnpj_receita_ws, buscar_cnpj_completo

def test_cnpj():
    cnpj = "19131243000197"
    
    print("Testando busca de CNPJ:", cnpj)
    
    # Teste da funcao completa
    dados = buscar_cnpj_completo(cnpj)
    
    if dados:
        print("Nome:", dados.get('nome', 'N/A'))
        print("Razao Social:", dados.get('razao_social', 'N/A'))
        print("Fantasia:", dados.get('fantasia', 'N/A'))
        print("Situacao:", dados.get('situacao', 'N/A'))
        print("Fonte:", dados.get('fonte', 'N/A'))
    else:
        print("CNPJ nao encontrado")

test_cnpj()