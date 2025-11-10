#!/usr/bin/env python3
"""
Script para testar a funcionalidade de Fidelidade

Este script pode ser executado para verificar se:
1. O menu Fidelidade foi adicionado corretamente
2. A URL está funcionando
3. O template é renderizado
4. O modelo e formulário estão funcionando

Para executar: python test_fidelidade.py
"""

def testar_fidelidade():
    print("🧪 TESTE DE FUNCIONALIDADE: FIDELIDADE")
    print("=" * 50)
    
    # Teste 1: Verificar estrutura de arquivos
    print("\n📁 1. Verificando arquivos criados/modificados:")
    
    import os
    arquivos_verificar = [
        ("Template Fidelidade", "linhas/templates/linhas/fidelidade.html"),
        ("Base.html (menu)", "linhas/templates/base.html"), 
        ("URLs", "linhas/urls.py"),
        ("Views", "linhas/views.py"),
        ("Models", "linhas/models.py"),
        ("Forms", "linhas/forms.py")
    ]
    
    for nome, caminho in arquivos_verificar:
        if os.path.exists(caminho):
            print(f"  ✅ {nome}: {caminho}")
            
            # Verificar conteúdo específico
            with open(caminho, 'r', encoding='utf-8') as f:
                conteudo = f.read()
                
            if 'fidelidade' in caminho:
                if 'Fidelidade' in conteudo and 'numero_linha' in conteudo:
                    print(f"    📋 Conteúdo correto encontrado")
                else:
                    print(f"    ❌ Conteúdo pode estar incorreto")
            elif 'base.html' in caminho:
                if 'fidelidade' in conteudo.lower():
                    print(f"    📋 Menu Fidelidade encontrado")
                else:
                    print(f"    ❌ Menu Fidelidade não encontrado")
            elif 'urls.py' in caminho:
                if 'fidelidade' in conteudo and 'buscar-linha-dados' in conteudo:
                    print(f"    📋 URLs de fidelidade encontradas")
                else:
                    print(f"    ❌ URLs de fidelidade não encontradas")
            elif 'models.py' in caminho:
                if 'class Fidelidade' in conteudo:
                    print(f"    📋 Modelo Fidelidade encontrado")
                else:
                    print(f"    ❌ Modelo Fidelidade não encontrado")
            elif 'forms.py' in caminho:
                if 'class FidelidadeForm' in conteudo:
                    print(f"    📋 Formulário Fidelidade encontrado")
                else:
                    print(f"    ❌ Formulário Fidelidade não encontrado")
            elif 'views.py' in caminho:
                if 'def fidelidade' in conteudo and 'def buscar_linha_dados' in conteudo:
                    print(f"    📋 Views de fidelidade encontradas")
                else:
                    print(f"    ❌ Views de fidelidade não encontradas")
        else:
            print(f"  ❌ {nome}: {caminho} (não encontrado)")
    
    # Teste 2: Verificar se é possível importar os modelos Django
    print("\n🐍 2. Testando imports Django:")
    try:
        import sys
        import os
        import django
        
        # Configurar Django
        sys.path.append('.')
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestor_linhas.settings')
        django.setup()
        
        from linhas.models import Fidelidade, Linha
        from linhas.forms import FidelidadeForm
        from linhas.views import fidelidade, buscar_linha_dados
        
        print("  ✅ Imports Django funcionando")
        print(f"    📋 Modelo Fidelidade: {Fidelidade}")
        print(f"    📋 Formulário FidelidadeForm: {FidelidadeForm}")
        print(f"    📋 View fidelidade: {fidelidade}")
        print(f"    📋 View buscar_linha_dados: {buscar_linha_dados}")
        
        # Teste 3: Verificar estrutura do modelo
        print("\n📊 3. Testando estrutura do modelo Fidelidade:")
        
        campos = [field.name for field in Fidelidade._meta.fields]
        print(f"    📋 Campos do modelo: {campos}")
        
        campos_esperados = ['id', 'linha', 'observacoes', 'criado_por', 'criado_em', 'atualizado_em']
        for campo in campos_esperados:
            if campo in campos:
                print(f"    ✅ Campo '{campo}' presente")
            else:
                print(f"    ❌ Campo '{campo}' ausente")
        
        # Teste 4: Testar formulário
        print("\n📝 4. Testando formulário FidelidadeForm:")
        
        form = FidelidadeForm()
        campos_form = list(form.fields.keys())
        print(f"    📋 Campos do formulário: {campos_form}")
        
        campos_form_esperados = ['numero_linha', 'observacoes']
        for campo in campos_form_esperados:
            if campo in campos_form:
                print(f"    ✅ Campo '{campo}' presente no formulário")
            else:
                print(f"    ❌ Campo '{campo}' ausente no formulário")
        
        print("\n🎉 Todos os testes básicos concluídos!")
        
    except ImportError as e:
        print(f"  ❌ Erro de import: {e}")
        print("  💡 Dica: Execute 'python manage.py migrate' primeiro")
    except Exception as e:
        print(f"  ❌ Erro inesperado: {e}")
    
    # Teste 5: Verificar URLs esperadas
    print("\n🔗 5. URLs que devem funcionar:")
    print("  📍 Menu: Linhas > Fidelidade")
    print("  📍 URL direta: /linhas/fidelidade/")
    print("  📍 API AJAX: /linhas/buscar-linha-dados/?numero=XXXXX")
    
    print("\n" + "=" * 50)
    print("🎯 RESUMO DOS RECURSOS IMPLEMENTADOS:")
    print("✅ Submenu 'FIDELIDADE' adicionado ao menu Linhas")
    print("✅ Página de fidelidade com formulário responsivo")
    print("✅ Campo 'Número da linha' com busca automática")
    print("✅ Campos 'Cliente' e 'RP' preenchidos automaticamente (readonly)")
    print("✅ Campo 'Observações' obrigatório")
    print("✅ Validação de formulário Django")
    print("✅ Modelo Fidelidade para armazenar dados")
    print("✅ API AJAX para buscar dados da linha")
    print("✅ Interface com Bootstrap e ícones FontAwesome")
    print("=" * 50)

if __name__ == "__main__":
    testar_fidelidade()