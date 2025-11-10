# Teste da Funcionalidade de Cadastro de Cliente

## Como Testar:

1. **Acesse a página:** http://localhost:8000/linhas/clientes/novo/

2. **Preencha os dados do cliente:**
   - CNPJ: 19131243000197 (use o botão "Buscar CNPJ" para preencher automaticamente)
   - Ou preencha manualmente:
     - Razão Social: Empresa Teste
     - Fantasia: Teste Ltda
     - Endereço: Rua Teste, 123
     - Contato: João Silva
     - Email: teste@empresa.com
     - Nome do Titular: João Silva
     - CPF: 12345678901
     - Data de Nascimento: 01/01/1980

3. **Escolha uma das opções de salvamento:**
   - **"Salvar e Continuar"**: Salva o cliente e mantém na página para cadastrar outro
   - **"Salvar e Criar Linha"**: Salva o cliente e vai para a página de criar linha

4. **Verifique as mensagens:**
   - Uma mensagem de sucesso deve aparecer
   - Os dados devem ser salvos no banco
   - Deve aparecer um card com informações do cliente salvo

## Funcionalidades Implementadas:

✅ **Mensagem de Operação Concluída**
- Mensagem verde de sucesso no topo da página
- Card com detalhes do cliente salvo
- Link direto para criar linha para o cliente

✅ **Duas Opções de Salvamento**
- Salvar e continuar na página (formulário é limpo para novo cadastro)
- Salvar e ir para criar linha (com dados pré-preenchidos)

✅ **Tratamento de Erros**
- Mensagem de erro se houver problemas na validação
- Campos obrigatórios destacados

✅ **Integração com API CNPJ**
- Botão "Buscar CNPJ" preenche dados automaticamente
- Dados são salvos corretamente mesmo quando preenchidos pela API

## Dados de Teste:

**CNPJ Válido para Teste:** 19131243000197
Este CNPJ retorna dados reais da empresa "OPEN KNOWLEDGE BRASIL"

**Cliente Manual de Teste:**
- Empresa: Empresa Teste LTDA
- CNPJ: 12345678000195
- Razão Social: Empresa Teste LTDA
- Fantasia: Teste
- Email: teste@empresa.com