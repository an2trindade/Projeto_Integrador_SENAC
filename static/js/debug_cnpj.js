// Script simplificado para teste do botão CNPJ
document.addEventListener('DOMContentLoaded', function() {
    console.log('Script carregado');
    
    var cnpjInput = document.getElementById('id_cnpj');
    var btnBuscar = document.getElementById('btn-buscar-cnpj');
    var razaoEl = document.getElementById('id_razao_social');
    var fantasiaEl = document.getElementById('id_fantasia');
    var enderecoEl = document.getElementById('id_endereco_completo');
    var alertEl = document.getElementById('cnpj-alert');
    
    console.log('Elementos encontrados:', {
        cnpjInput: !!cnpjInput,
        btnBuscar: !!btnBuscar,
        razaoEl: !!razaoEl,
        fantasiaEl: !!fantasiaEl,
        enderecoEl: !!enderecoEl,
        alertEl: !!alertEl
    });
    
    function showAlert(msg, isError) {
        if (!alertEl) return;
        alertEl.style.display = msg ? '' : 'none';
        alertEl.textContent = msg || '';
        alertEl.classList.toggle('text-danger', !!isError);
        alertEl.classList.toggle('text-success', !isError && !!msg);
    }
    
    async function buscarCnpj() {
        console.log('buscarCnpj chamada');
        showAlert('', false);
        
        if (!cnpjInput) {
            console.error('Input CNPJ não encontrado');
            return;
        }
        
        var digits = (cnpjInput.value || '').replace(/\D/g, '');
        console.log('CNPJ digits:', digits);
        
        if (digits.length !== 14) {
            showAlert('Digite o CNPJ completo (14 dígitos).', true);
            return;
        }
        
        if (btnBuscar) btnBuscar.disabled = true;
        showAlert('Buscando dados do CNPJ...', false);
        
        try {
            var url = '/linhas/buscar-cnpj-api/?cnpj=' + digits;
            console.log('Fazendo requisição para:', url);
            
            var response = await fetch(url);
            console.log('Resposta recebida:', response.status);
            
            if (!response.ok) {
                throw new Error('Erro na requisição: ' + response.status);
            }
            
            var result = await response.json();
            console.log('Resultado:', result);
            
            if (!result.success) {
                throw new Error(result.error || 'CNPJ não encontrado');
            }
            
            var data = result.dados;
            
            // Preencher campos
            if (razaoEl && data.razao_social) {
                razaoEl.value = data.razao_social;
                console.log('Razão social preenchida:', data.razao_social);
            }
            
            if (fantasiaEl && data.fantasia) {
                fantasiaEl.value = data.fantasia;
                console.log('Fantasia preenchida:', data.fantasia);
            }
            
            if (enderecoEl) {
                var endParts = [];
                if (data.endereco) endParts.push(data.endereco);
                if (data.numero) endParts.push(data.numero);
                if (data.complemento) endParts.push(data.complemento);
                if (data.bairro) endParts.push(data.bairro);
                if (data.municipio) endParts.push(data.municipio);
                if (data.uf) endParts.push(data.uf);
                if (data.cep) endParts.push('CEP: ' + data.cep);
                var endereco = endParts.join(', ');
                enderecoEl.value = endereco;
                console.log('Endereço preenchido:', endereco);
            }
            
            showAlert('Dados carregados com sucesso! Fonte: ' + (data.fonte || 'API'), false);
            
        } catch (error) {
            console.error('Erro ao buscar CNPJ:', error);
            showAlert('Erro: ' + error.message, true);
        } finally {
            if (btnBuscar) btnBuscar.disabled = false;
        }
    }
    
    // Event listener
    if (btnBuscar) {
        console.log('Adicionando event listener ao botão');
        btnBuscar.addEventListener('click', function(ev) {
            console.log('Botão clicado');
            ev.preventDefault();
            buscarCnpj();
        });
    } else {
        console.error('Botão não encontrado');
    }
});