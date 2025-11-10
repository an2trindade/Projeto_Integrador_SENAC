# Fluxo POST - Cadastro de Cliente com Dados CNPJ

## Visão Geral

Este documento detalha o fluxo completo de POST das informações obtidas através da busca de CNPJ para o cadastro de novos clientes no sistema.

## Fluxo Completo

### 1. Busca de Dados CNPJ (GET)

**Endpoint:** `GET /linhas/buscar-cnpj-api/`

**Parâmetros:**
- `cnpj`: String com 14 dígitos (apenas números)

**Exemplo de Requisição:**
```http
GET /linhas/buscar-cnpj-api/?cnpj=19131243000197
Content-Type: application/json
X-Requested-With: XMLHttpRequest
```

**Exemplo de Resposta de Sucesso:**
```json
{
  "success": true,
  "dados": {
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
}
```

### 2. Cadastro de Cliente (POST)

**Endpoint:** `POST /linhas/novo-cliente/`

**Content-Type:** `multipart/form-data`

**Headers Obrigatórios:**
- `X-CSRFToken`: Token CSRF obtido do cookie `csrftoken`
- `Referer`: URL da página de origem

## Campos do Formulário POST

### Campos da Empresa (obtidos via CNPJ)

| Campo | Tipo | Obrigatório | Origem | Exemplo |
|-------|------|-------------|---------|---------|
| `empresa` | string | ✅ | `razao_social` da API | "EMPRESA EXEMPLO LTDA" |
| `cnpj` | string | ✅ | `cnpj` da API | "19.131.243/0001-97" |
| `razao_social` | string | ❌ | `razao_social` da API | "EMPRESA EXEMPLO LTDA" |
| `fantasia` | string | ❌ | `fantasia` da API | "Exemplo Corp" |
| `endereco_completo` | text | ❌ | Concatenação de múltiplos campos | "RUA DAS FLORES, Nº 123, SALA 456, CENTRO, SAO PAULO, SP, CEP: 01234567" |
| `email` | email | ❌ | `email` da API | "contato@exemplo.com.br" |
| `telefone` | string | ❌ | `telefone` da API | "1134567890" |

### Campos do Proprietário (informados pelo usuário)

| Campo | Tipo | Obrigatório | Exemplo |
|-------|------|-------------|---------|
| `contato` | string | ❌ | "João Silva" |
| `nome_dono` | string | ❌ | "João Silva Santos" |
| `cpf_dono` | string | ❌ | "123.456.789-00" |
| `data_nascimento_dono` | date | ❌ | "1980-05-15" |

### Campos de Controle

| Campo | Tipo | Obrigatório | Valores | Descrição |
|-------|------|-------------|---------|-----------|
| `csrfmiddlewaretoken` | string | ✅ | Token CSRF | Token de segurança Django |
| `next_action` | string | ❌ | `stay` ou `nova_linha` | Define ação após cadastro |

## Exemplo Completo de POST

### Dados Enviados

```http
POST /linhas/novo-cliente/
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW
X-CSRFToken: abc123token456def
Referer: http://localhost:8000/linhas/novo-cliente/

------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="csrfmiddlewaretoken"

abc123token456def
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="empresa"

EMPRESA EXEMPLO LTDA
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="cnpj"

19.131.243/0001-97
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="razao_social"

EMPRESA EXEMPLO LTDA
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="fantasia"

Exemplo Corp
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="endereco_completo"

RUA DAS FLORES, Nº 123, SALA 456, CENTRO, SAO PAULO, SP, CEP: 01234567
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="email"

contato@exemplo.com.br
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="contato"

João Silva
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="telefone"

1134567890
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="nome_dono"

João Silva Santos
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="cpf_dono"

123.456.789-00
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="data_nascimento_dono"

1980-05-15
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="next_action"

stay
------WebKitFormBoundary7MA4YWxkTrZu0gW--
```

### Resposta de Sucesso

```http
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Set-Cookie: messages=...

<!DOCTYPE html>
<html>
<!-- HTML da página com mensagem de sucesso -->
<!-- Contém: "Cliente 'EMPRESA EXEMPLO LTDA' cadastrado com sucesso!" -->
</html>
```

## Código JavaScript para POST

### Função Completa

```javascript
async function cadastrarClienteComCnpj(dadosCnpj, dadosProprietario = {}) {
    // 1. Obter CSRF token
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value ||
                     getCookie('csrftoken');
    
    // 2. Construir endereço completo
    const enderecoPartes = [];
    if (dadosCnpj.endereco) enderecoPartes.push(dadosCnpj.endereco);
    if (dadosCnpj.numero) enderecoPartes.push(`Nº ${dadosCnpj.numero}`);
    if (dadosCnpj.complemento) enderecoPartes.push(dadosCnpj.complemento);
    if (dadosCnpj.bairro) enderecoPartes.push(dadosCnpj.bairro);
    if (dadosCnpj.municipio) enderecoPartes.push(dadosCnpj.municipio);
    if (dadosCnpj.uf) enderecoPartes.push(dadosCnpj.uf);
    if (dadosCnpj.cep) enderecoPartes.push(`CEP: ${dadosCnpj.cep}`);
    
    // 3. Preparar FormData
    const formData = new FormData();
    formData.append('csrfmiddlewaretoken', csrfToken);
    
    // Dados da empresa (obtidos via CNPJ)
    formData.append('empresa', dadosCnpj.razao_social || dadosCnpj.nome || '');
    formData.append('cnpj', dadosCnpj.cnpj || '');
    formData.append('razao_social', dadosCnpj.razao_social || dadosCnpj.nome || '');
    formData.append('fantasia', dadosCnpj.fantasia || dadosCnpj.nome_fantasia || '');
    formData.append('endereco_completo', enderecoPartes.join(', '));
    formData.append('email', dadosCnpj.email || '');
    formData.append('telefone', dadosCnpj.telefone || '');
    
    // Dados do proprietário (informados pelo usuário)
    formData.append('contato', dadosProprietario.contato || '');
    formData.append('nome_dono', dadosProprietario.nome_dono || '');
    formData.append('cpf_dono', dadosProprietario.cpf_dono || '');
    formData.append('data_nascimento_dono', dadosProprietario.data_nascimento_dono || '');
    
    // Controle
    formData.append('next_action', 'stay');
    
    // 4. Fazer POST
    try {
        const response = await fetch('/linhas/novo-cliente/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken
            }
        });
        
        if (response.ok) {
            // Verificar se contém mensagem de sucesso no HTML
            const html = await response.text();
            if (html.includes('cadastrado com sucesso')) {
                return { success: true, message: 'Cliente cadastrado com sucesso!' };
            } else {
                return { success: false, message: 'Erro na validação do formulário' };
            }
        } else {
            return { success: false, message: `Erro HTTP: ${response.status}` };
        }
        
    } catch (error) {
        return { success: false, message: `Erro na requisição: ${error.message}` };
    }
}

// Função auxiliar para obter cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
```

### Exemplo de Uso

```javascript
// 1. Primeiro, buscar dados do CNPJ
const response = await fetch('/linhas/buscar-cnpj-api/?cnpj=19131243000197');
const result = await response.json();

if (result.success) {
    // 2. Dados do proprietário (informados pelo usuário)
    const dadosProprietario = {
        contato: 'João Silva',
        nome_dono: 'João Silva Santos',
        cpf_dono: '123.456.789-00',
        data_nascimento_dono: '1980-05-15'
    };
    
    // 3. Cadastrar cliente
    const cadastro = await cadastrarClienteComCnpj(result.dados, dadosProprietario);
    
    if (cadastro.success) {
        alert('✅ Cliente cadastrado com sucesso!');
    } else {
        alert(`❌ Erro: ${cadastro.message}`);
    }
}
```

## Validações no Backend

### View `cliente_novo` (views.py linha 289-327)

A view processa o POST da seguinte forma:

1. **Validação CSRF**: Automática pelo Django
2. **Validação do Form**: Usando `ClienteForm(request.POST)`
3. **Salvamento**: `form.save()` se válido
4. **Redirect/Response**: Baseado no `next_action`

### Campos Obrigatórios no Model

Conforme `models.py`, apenas o campo `empresa` é obrigatório:

```python
class Cliente(models.Model):
    empresa = models.CharField(max_length=150, verbose_name='Empresa')  # OBRIGATÓRIO
    cnpj = models.CharField(max_length=18, verbose_name='CNPJ', blank=True, default='')
    # ... outros campos são opcionais (blank=True)
```

## Tratamento de Erros

### Possíveis Erros no POST

1. **403 Forbidden**: Token CSRF inválido/ausente
2. **400 Bad Request**: Dados do formulário inválidos
3. **500 Internal Server Error**: Erro no servidor

### Exemplo de Tratamento

```javascript
try {
    const response = await fetch('/linhas/novo-cliente/', {
        method: 'POST',
        body: formData,
        headers: { 'X-CSRFToken': csrfToken }
    });
    
    if (response.status === 403) {
        throw new Error('Token CSRF inválido. Recarregue a página.');
    } else if (response.status === 400) {
        throw new Error('Dados do formulário inválidos. Verifique os campos.');
    } else if (!response.ok) {
        throw new Error(`Erro HTTP: ${response.status}`);
    }
    
    // Processar resposta de sucesso...
    
} catch (error) {
    console.error('Erro no cadastro:', error);
    alert(`Erro: ${error.message}`);
}
```

## Resumo do Fluxo

1. **GET** `/linhas/buscar-cnpj-api/?cnpj=XXXXXXXXXX` → Obter dados da empresa
2. **Preencher** formulário com dados obtidos + dados do proprietário
3. **POST** `/linhas/novo-cliente/` → Cadastrar cliente
4. **Processar** resposta (sucesso/erro)

Este fluxo garante que as informações do CNPJ sejam automaticamente preenchidas e enviadas corretamente para o cadastro do cliente.