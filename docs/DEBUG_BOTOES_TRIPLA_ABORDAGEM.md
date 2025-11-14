# Debug Intensivo - Botões PJ/PF com Múltiplas Abordagens

## Problema Persistente
Os botões ainda não estavam funcionando após várias tentativas.

## Estratégia de Debug Implementada

### 1. **Tripla Abordagem JavaScript**
```javascript
// ✅ 1. Onclick direto no HTML
<button onclick="mostrarFormularioPJ()">

// ✅ 2. Event listener no DOM ready  
btnPJ.onclick = function() { mostrarFormularioPJ(); };

// ✅ 3. Listener de emergência no body
document.body.addEventListener('click', function(e) {
    if (e.target.id === 'btn-pessoa-juridica') {
        mostrarFormularioPJ();
    }
});
```

### 2. **Logs Detalhados para Diagnóstico**
```javascript
console.log('=== SCRIPT INICIADO ===');
console.log('form-pessoa-juridica existe:', !!document.getElementById('form-pessoa-juridica'));
console.log('btn-pessoa-juridica existe:', !!document.getElementById('btn-pessoa-juridica'));

// Dentro das funções
console.log('=== EXECUTANDO mostrarFormularioPJ ===');
console.log('Elementos na função PJ:', {formPJ, formPF, btnPJ, btnPF});
```

### 3. **Alertas de Erro Visíveis**
```javascript
if (!formPJ || !formPF) {
    console.error('ERRO: Elementos não encontrados');
    alert('Erro: Formulários não encontrados. Verifique o console.');
}
```

### 4. **Classes CSS Dinâmicas**
```javascript
// Destaque do botão ativo
btnPJ.classList.remove('btn-outline-primary');
btnPJ.classList.add('btn-primary');

// Reset ao fechar
btnPJ.classList.remove('btn-primary');
btnPJ.classList.add('btn-outline-primary');
```

### 5. **Scroll Automático com Delay**
```javascript
setTimeout(function() {
    formPJ.scrollIntoView({ behavior: 'smooth', block: 'start' });
}, 100); // Aguarda display ser aplicado
```

## Como Usar para Debug

### **Passo 1: Abrir Console**
1. F12 → Console
2. Recarregar página
3. Verificar logs iniciais

### **Passo 2: Verificar Elementos**
```javascript
// No console, testar:
console.log(document.getElementById('btn-pessoa-juridica'));
console.log(document.getElementById('form-pessoa-juridica'));
```

### **Passo 3: Testar Função Diretamente**
```javascript
// No console, executar:
mostrarFormularioPJ();
```

### **Passo 4: Clicar nos Botões**
- Observe logs detalhados
- Verifique se 3 listeners são executados
- Confirme mudança visual dos formulários

## Possíveis Problemas Identificados

### ❌ **Problema 1: Elementos não existem**
- **Sintoma**: `null` nos logs de elementos
- **Causa**: IDs incorretos ou HTML não carregado
- **Solução**: Verificar estrutura HTML

### ❌ **Problema 2: JavaScript não carrega**
- **Sintoma**: Nenhum log aparece
- **Causa**: Erro de sintaxe ou arquivo bloqueado
- **Solução**: Verificar erros no console

### ❌ **Problema 3: CSS sobrescrevendo display**
- **Sintoma**: `display: block` não funciona
- **Causa**: CSS com `!important` ou maior especificidade
- **Solução**: Inspecionar elemento e verificar CSS

### ❌ **Problema 4: Conflito de bibliotecas**
- **Sintoma**: Listeners não funcionam
- **Causa**: Bootstrap/jQuery interferindo
- **Solução**: Usar delegação de eventos

## Benefícios da Abordagem

### ✅ **Detecção Precisa**
- Logs mostram exatamente onde está o problema
- Múltiplos listeners garantem funcionamento
- Alertas avisam sobre erros

### ✅ **Robustez**
- 3 maneiras diferentes de capturar cliques
- Funciona mesmo com conflitos de JS
- Fallback para qualquer situação

### ✅ **Debug Visual**
- Classes CSS mostram estado ativo
- Scroll automático confirma funcionamento
- Alertas informam problemas

## Próximos Passos

1. **Testar todas as 3 abordagens**
2. **Verificar logs no console**
3. **Identificar qual abordagem funciona**
4. **Remover logs e manter apenas a solução**

## Arquivo Modificado
- `linhas/templates/linhas/novo_cliente.html`

## Data do Debug
13 de novembro de 2025