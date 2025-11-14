# Correção dos Botões PJ/PF - Formulários Novo Cliente

## Problema Identificado
Os botões "Pessoa Jurídica" e "Pessoa Física" não estavam funcionando para abrir os respectivos formulários.

## Causa Raiz
- Possível conflito de eventos JavaScript
- Elementos não encontrados no momento da inicialização DOM
- URL incorreta do CDN Cleave.js

## Soluções Implementadas

### 1. Debug JavaScript Aprimorado
```javascript
console.log('Inicializando controle de formulários...');
console.log('Elementos encontrados:', {btnPJ, btnPF, tipoSelection});

if (!tipoSelection || !formPJ || !formPF || !btnPJ || !btnPF) {
    console.error('Alguns elementos não foram encontrados!');
    return;
}
```

### 2. Delegação de Eventos como Fallback
```javascript
document.body.addEventListener('click', function(e) {
    if (e.target.id === 'btn-pessoa-juridica' || e.target.closest('#btn-pessoa-juridica')) {
        // Abrir formulário PJ
    }
    if (e.target.id === 'btn-pessoa-fisica' || e.target.closest('#btn-pessoa-fisica')) {
        // Abrir formulário PF  
    }
});
```

### 3. Correção URL Cleave.js
- **Corrigido**: `https://cdn.jsdelivr.net/npm/cleave.js@1.6.0/dist/cleave.min.js`

### 4. Tratamento Robusto de Cliques
- Verifica `e.target.id` e `e.target.closest()`
- Previne comportamento padrão com `e.preventDefault()`
- Logs detalhados de debugging

## Funcionalidade Esperada
1. **Clicar PJ**: Oculta seleção, mostra formulário Pessoa Jurídica
2. **Clicar PF**: Oculta seleção, mostra formulário Pessoa Física  
3. **Voltar/Cancelar**: Retorna à tela de seleção

## Como Testar
1. Abrir "Novo Cliente"
2. F12 → Console
3. Clicar botões e verificar logs
4. Confirmar mudança de formulários

## Benefícios
- ✅ **Dupla proteção**: Listener direto + delegação
- ✅ **Debug completo**: Logs para diagnóstico
- ✅ **Robustez**: Funciona mesmo com conflitos JS
- ✅ **CDN correto**: Cleave.js funcionando

## Arquivo Modificado
- `linhas/templates/linhas/novo_cliente.html`

## Data da Correção
13 de novembro de 2025