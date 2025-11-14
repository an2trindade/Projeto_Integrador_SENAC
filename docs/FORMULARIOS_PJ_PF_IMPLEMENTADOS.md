# Formulários Pessoa Jurídica e Pessoa Física - Novo Cliente

## Descrição da Implementação
Implementados dois formulários distintos na aba "Novo Cliente" com seleção através de botões específicos para cada tipo de pessoa.

## Interface de Seleção
- **Tela inicial**: Card com dois botões grandes
- **Pessoa Jurídica**: Botão azul com ícone de prédio
- **Pessoa Física**: Botão verde com ícone de pessoa

## Formulário Pessoa Jurídica
### Campos Implementados:
1. **CNPJ*** - Com botão "Buscar CNPJ" integrado
2. **Razão Social*** - Campo obrigatório
3. **Nome Fantasia** - Campo opcional
4. **Endereço Completo*** - Textarea
5. **Contato Principal*** - Nome do responsável
6. **E-mail** - Campo opcional
7. **Nome do Proprietário*** - Campo obrigatório
8. **CPF do Proprietário*** - Com máscara
9. **Data de Nascimento do Proprietário*** - Campo data

### Funcionalidades PJ:
- ✅ Busca automática de dados por CNPJ
- ✅ Máscaras de entrada (CNPJ, CPF)
- ✅ Validação de campos obrigatórios

## Formulário Pessoa Física
### Campos Implementados:
1. **CPF*** - Com máscara 000.000.000-00
2. **Nome Completo*** - Campo texto
3. **Data de Nascimento*** - Campo data
4. **Endereço Completo*** - Textarea
5. **Contato Principal*** - Telefone com máscara
6. **E-mail** - Campo opcional

### Funcionalidades PF:
- ✅ Máscaras de entrada (CPF, Telefone)
- ✅ Validação de campos obrigatórios
- ✅ Interface simplificada

## Controles de Navegação
- **Voltar**: Retorna à seleção de tipo
- **Cancelar**: Retorna à seleção de tipo
- **Salvar e Continuar**: Salva e permite novo cadastro
- **Salvar e Criar Linha**: Salva e vai para nova linha

## JavaScript Implementado
### Controle de Telas:
- Alternância entre formulários
- Botões de navegação
- Ocultação/exibição de seções

### Máscaras Cleave.js:
- CNPJ: 00.000.000/0000-00
- CPF: 000.000.000-00
- Telefone: (00) 00000-0000

## Integração com Backend
- Campo `tipo_pessoa` hidden para identificar o tipo
- Campos mapeados para model existente
- Compatibilidade com views atuais

## Arquivo Modificado
- `linhas/templates/linhas/novo_cliente.html`

## Data da Implementação
13 de novembro de 2025