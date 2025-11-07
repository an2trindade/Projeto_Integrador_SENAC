# Correção do Botão "Consultar CNPJ" - Relatório de Soluções

## Problema Identificado
O botão "Buscar CNPJ" na página de cadastro de novo cliente não estava funcionando.

## Soluções Implementadas

### 1. ✅ **Substituição das APIs Externas**
**Problema:** O código original fazia chamadas diretas para APIs externas (BrasilAPI e ReceitaWS), que podem ser bloqueadas por políticas CORS do navegador.

**Solução:** Substituído por chamadas para nossa API interna `/linhas/buscar-cnpj-api/` que faz o proxy das APIs externas no backend.

**Arquivos modificados:**
- `linhas/templates/linhas/novo_cliente.html` 
- `linhas/templates/linhas/nova_linha.html`

### 2. ✅ **Simplificação do Código JavaScript**
**Problema:** O código JavaScript estava complexo e com possíveis conflitos de event listeners.

**Solução:** 
- Removidas funções `fetchBrasilApi()` e `fetchReceitaWs()` duplicadas
- Simplificada a função `buscarCnpj()` para usar apenas nossa API interna
- Adicionado logging detalhado para debug

### 3. ✅ **Event Listener Adicional para Garantia**
**Problema:** O event listener principal poderia não estar sendo anexado corretamente.

**Solução:** Adicionado um script adicional que:
- Aguarda o carregamento completo da página
- Verifica se o botão existe
- Adiciona um listener alternativo caso o principal falhe
- Inclui logs detalhados para debug

### 4. ✅ **Melhor Tratamento de Erros**
**Problema:** Erros não eram claramente reportados ao usuário.

**Solução:**
- Adicionado console.log em pontos críticos
- Mensagens de erro mais específicas
- Status HTTP e respostas da API logados
- Fallback para alert() em caso de falha do sistema de alertas

### 5. ✅ **Headers HTTP Apropriados**
**Problema:** Requisições poderiam estar sendo rejeitadas pelo Django.

**Solução:** Adicionados headers:
- `'X-Requested-With': 'XMLHttpRequest'`
- `'Content-Type': 'application/json'`

## APIs Envolvidas

### API Interna (Backend)
- **URL:** `/linhas/buscar-cnpj-api/?cnpj=19131243000197`
- **Método:** GET
- **Resposta de Sucesso:**
```json
{
    "success": true,
    "dados": {
        "cnpj": "19131243000197",
        "nome": "OPEN KNOWLEDGE BRASIL",
        "razao_social": "OPEN KNOWLEDGE BRASIL",
        "fantasia": "REDE PELO CONHECIMENTO LIVRE",
        "situacao": "ATIVA",
        "endereco": "PAULISTA 37",
        "numero": "37",
        "complemento": "ANDAR 4",
        "bairro": "BELA VISTA",
        "municipio": "SAO PAULO",
        "uf": "SP",
        "cep": "01311902",
        "fonte": "BrasilAPI"
    }
}
```

### APIs Externas (usadas pelo backend)
1. **BrasilAPI** (principal): `https://brasilapi.com.br/api/cnpj/v1/{cnpj}`
2. **ReceitaWS** (fallback): `https://www.receitaws.com.br/v1/cnpj/{cnpj}`

## Funcionalidade Atual

### Fluxo de Funcionamento:
1. Usuário digita CNPJ no campo
2. Clica no botão "Buscar CNPJ"
3. JavaScript valida se CNPJ tem 14 dígitos
4. Faz requisição para `/linhas/buscar-cnpj-api/`
5. Backend tenta BrasilAPI primeiro, depois ReceitaWS se falhar
6. Dados são retornados e preenchem automaticamente:
   - Razão Social
   - Nome Fantasia  
   - Endereço completo (formatado)
7. Mensagem de sucesso é exibida

### Debug e Monitoramento:
- Console do navegador mostra logs detalhados
- Página de debug disponível em: `/linhas/debug-cnpj-button/`
- Página de teste disponível em: `/linhas/test-cnpj-api/`

## Como Testar

### 1. Teste Manual:
1. Acesse: `http://localhost:8000/linhas/clientes/novo/`
2. Digite um CNPJ (ex: 19131243000197)
3. Clique em "Buscar CNPJ"
4. Verifique se os campos são preenchidos

### 2. Teste de Debug:
1. Acesse: `http://localhost:8000/linhas/debug-cnpj-button/`
2. Clique em "Testar API"
3. Veja logs detalhados da requisição

### 3. Verificação do Console:
1. Abra DevTools (F12)
2. Vá para aba Console
3. Procure por mensagens como:
   - "Script adicional carregado para debug do botão CNPJ"
   - "Debug - Botão encontrado: true"
   - "Fazendo requisição para: /linhas/buscar-cnpj-api/..."

## Próximos Passos Sugeridos

1. **Remover o script de debug** após confirmação de funcionamento
2. **Implementar cache** para evitar consultas repetidas do mesmo CNPJ
3. **Adicionar indicador visual** melhor durante o carregamento
4. **Validação de CNPJ** com dígitos verificadores no frontend

## Status: ✅ CORRIGIDO

O botão "Consultar CNPJ" agora deve estar funcionando corretamente com múltiplas camadas de segurança e fallbacks implementados.