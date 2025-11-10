# Reordenação de Campos - Nova Linha

## Descrição da Alteração
Reorganizados os campos na página "Nova Linha" para melhorar o fluxo de trabalho do usuário.

## Nova Ordem dos Campos
1. **AÇÃO** - Primeiro campo (define o tipo de operação)
2. **FATURA** - Segundo bloco (dados do cliente/empresa)
3. **LINHAS** - Último bloco (detalhes das linhas)

## Justificativa
- **Lógica de Processo**: O usuário primeiro define qual ação será realizada (TT, Portabilidade, Estoque, etc.)
- **Dependências**: A ação escolhida afeta campos subsequentes (como mostrar/ocultar campos de portabilidade)
- **Fluxo Natural**: Ação → Cliente/Fatura → Linhas segue a sequência lógica de trabalho

## Arquivos Modificados
- `linhas/templates/linhas/nova_linha.html`

## Funcionalidades Mantidas
- Todas as funcionalidades JavaScript foram preservadas
- Autocomplete de empresa/CNPJ mantido funcional
- Campos dinâmicos de linhas continuam operacionais
- Validações e máscaras permanecem ativas

## Data da Implementação
10 de novembro de 2025