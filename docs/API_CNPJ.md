# API de Busca de CNPJ - Documentação

## Visão Geral

Foi implementada uma funcionalidade completa para buscar dados de CNPJ usando APIs externas brasileiras. O sistema funciona com um modelo de fallback, tentando primeiro a BrasilAPI e depois a ReceitaWS caso a primeira falhe.

## Arquivos Criados/Modificados

### 1. Arquivo de Utilitários (`linhas/utils.py`)

Contém as funções principais para busca de CNPJ:

- `buscar_cnpj_receita_ws(cnpj)` - Busca dados na API ReceitaWS
- `buscar_cnpj_brasil_api(cnpj)` - Busca dados na API BrasilAPI
- `buscar_cnpj_completo(cnpj)` - Função principal com fallback automático
- `limpar_cnpj(cnpj_raw)` - Remove formatação do CNPJ
- `validar_cnpj_formato(cnpj)` - Valida se o CNPJ tem 14 dígitos
- `formatar_cnpj(cnpj)` - Formata CNPJ no padrão XX.XXX.XXX/XXXX-XX

### 2. Nova View (`linhas/views.py`)

Adicionada a função `buscar_cnpj_api_externa(request)` que expõe a funcionalidade via HTTP.

### 3. Nova URL (`linhas/urls.py`)

Adicionada a rota: `path("buscar-cnpj-api/", views.buscar_cnpj_api_externa, name="buscar_cnpj_api_externa")`

### 4. Dependências (`requirements.txt`)

Adicionado: `requests==2.31.0`

## Como Usar

### 1. Via Python (Django Shell)

```python
from linhas.utils import buscar_cnpj_completo

# Exemplo com o CNPJ fornecido
cnpj = "19131243000197"
dados = buscar_cnpj_completo(cnpj)

if dados:
    print(f"Nome: {dados['nome']}")
    print(f"Razão Social: {dados['razao_social']}")
    print(f"Fantasia: {dados['fantasia']}")
    print(f"Situação: {dados['situacao']}")
    print(f"Fonte: {dados['fonte']}")
else:
    print("CNPJ não encontrado")
```

### 2. Via API HTTP

**URL:** `GET /linhas/buscar-cnpj-api/?cnpj=19131243000197`

**Resposta de Sucesso:**
```json
{
    "success": true,
    "dados": {
        "cnpj": "19131243000197",
        "nome": "OPEN KNOWLEDGE BRASIL",
        "razao_social": "OPEN KNOWLEDGE BRASIL",
        "fantasia": "REDE PELO CONHECIMENTO LIVRE",
        "situacao": "ATIVA",
        "endereco": "RUA BELA CINTRA",
        "numero": "986",
        "bairro": "CONSOLACAO",
        "municipio": "SAO PAULO",
        "uf": "SP",
        "cep": "01415002",
        "fonte": "BrasilAPI"
    }
}
```

**Resposta de Erro:**
```json
{
    "success": false,
    "error": "CNPJ não encontrado nas APIs externas"
}
```

### 3. Via JavaScript (Frontend)

```javascript
async function buscarCNPJ(cnpj) {
    try {
        const response = await fetch(`/linhas/buscar-cnpj-api/?cnpj=${cnpj}`);
        const data = await response.json();
        
        if (data.success) {
            console.log('Nome:', data.dados.nome);
            console.log('Razão Social:', data.dados.razao_social);
            // ... outros campos
        } else {
            console.error('Erro:', data.error);
        }
    } catch (error) {
        console.error('Erro de conexão:', error);
    }
}

// Uso
buscarCNPJ('19131243000197');
```

### 4. Página de Teste

Acesse: `http://localhost:8000/linhas/test-cnpj-api/`

Uma página de teste completa foi criada para demonstrar a funcionalidade.

## Funcionalidades Implementadas

### ✅ Código Original Solicitado
O código exato que você forneceu foi implementado na função `buscar_cnpj_receita_ws()`:

```python
import requests

cnpj = "19131243000197"
r = requests.get(f"https://www.receitaws.com.br/v1/cnpj/{cnpj}", timeout=10)
r.raise_for_status()
print(r.json()["nome"])
```

### ✅ Melhorias Adicionadas

1. **Fallback Automático**: Se a ReceitaWS falhar, tenta automaticamente a BrasilAPI
2. **Tratamento de Erros**: Captura timeouts e erros de conexão
3. **Validação de CNPJ**: Verifica se o CNPJ tem 14 dígitos
4. **Padronização de Resposta**: Normaliza os dados de diferentes APIs
5. **Logging**: Registra erros para debugging
6. **API HTTP**: Expõe a funcionalidade via endpoint REST
7. **Formatação de CNPJ**: Utilitário para formatar/limpar CNPJs

## APIs Externas Utilizadas

### BrasilAPI (Principal)
- **URL:** `https://brasilapi.com.br/api/cnpj/v1/{cnpj}`
- **Gratuita e sem limitações conhecidas**
- **Dados mais completos e atualizados**

### ReceitaWS (Fallback)
- **URL:** `https://www.receitaws.com.br/v1/cnpj/{cnpj}`
- **Pode ter limitações de rate limit**
- **Backup confiável**

## Testes

Execute o script de teste:
```bash
python manage.py shell -c "exec(open('scripts/test_simple_cnpj.py').read())"
```

Resultado esperado:
```
Testando busca de CNPJ: 19131243000197
Nome: OPEN KNOWLEDGE BRASIL
Razao Social: OPEN KNOWLEDGE BRASIL
Fantasia: REDE PELO CONHECIMENTO LIVRE
Situacao: ATIVA
Fonte: BrasilAPI
```

## Próximos Passos Sugeridos

1. **Integração no Frontend**: Substituir as chamadas JavaScript atuais pela nova API
2. **Cache**: Implementar cache para evitar consultas repetidas
3. **Rate Limiting**: Adicionar controle de taxa para evitar sobrecarga das APIs
4. **Validação Completa de CNPJ**: Implementar validação com dígitos verificadores
5. **Logs Estruturados**: Melhorar o sistema de logging para monitoramento

## Solução de Problemas

### Erro de Timeout
- As APIs externas podem estar sobrecarregadas
- O sistema automaticamente tenta a API alternativa

### CNPJ Não Encontrado
- Verifique se o CNPJ está correto e tem 14 dígitos
- Alguns CNPJs podem não estar disponíveis nas APIs públicas

### Erro de Conexão
- Verifique a conexão com a internet
- As APIs externas podem estar temporariamente indisponíveis