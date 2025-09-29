def listar_rps_cliente(request):
    cnpj = request.GET.get('cnpj', '')
    empresa = request.GET.get('empresa', '')
    rps = Linha.objects.filter(cnpj=cnpj, empresa=empresa).values_list('rp', flat=True).distinct()
    resultados = [rp for rp in rps if rp]
    return JsonResponse(resultados, safe=False)
def autocomplete_cnpj(request):
    termo = request.GET.get('q', '')
    linhas = Linha.objects.filter(cnpj__icontains=termo).values('cnpj', 'empresa').distinct()
    resultados = [
        {'cnpj': l['cnpj'], 'empresa': l['empresa']}
        for l in linhas[:10]
    ]
    return JsonResponse(resultados, safe=False)
from django.http import JsonResponse
from .models import Linha

def buscar_cliente_por_cnpj(request):
    cnpj = request.GET.get('cnpj', '')
    linha = Linha.objects.filter(cnpj=cnpj).first()
    if linha:
        return JsonResponse({'empresa': linha.empresa})
    return JsonResponse({'empresa': ''})
from django.http import JsonResponse
from .models import Linha

def buscar_linhas_estoque(request):
    termo = request.GET.get('q', '')
    empresa = request.GET.get('empresa', '')
    linhas = Linha.objects.filter(origem='ESTOQUE', empresa__icontains=empresa, numero__icontains=termo)
    resultados = [
        {'id': l.id, 'numero': l.numero, 'iccid': l.iccid}
        for l in linhas[:10]
    ]
    return JsonResponse(resultados, safe=False)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Linha
from .forms import LinhaForm, BuscaLinhaForm

@login_required
def lista_linhas(request):
    form_busca = BuscaLinhaForm(request.GET)
    linhas = Linha.objects.all()
    
    if form_busca.is_valid():
        busca = form_busca.cleaned_data.get('busca')
        operadora = form_busca.cleaned_data.get('operadora')
        tipo_plano = form_busca.cleaned_data.get('tipo_plano')
        ativa = form_busca.cleaned_data.get('ativa')
        
        if busca:
            linhas = linhas.filter(
                Q(numero__icontains=busca) |
                Q(empresa__icontains=busca) |
                Q(cnpj__icontains=busca) |
                Q(rp__icontains=busca)
            )
        
        if operadora:
            linhas = linhas.filter(operadora=operadora)
            
        if tipo_plano:
            linhas = linhas.filter(tipo_plano=tipo_plano)
            
        if ativa:
            if ativa == 'ativa':
                linhas = linhas.filter(ativa=True)
            elif ativa == 'inativa':
                linhas = linhas.filter(ativa=False)
            else:
                linhas = linhas.filter(acao__iexact=ativa)
    
    paginator = Paginator(linhas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'form_busca': form_busca,
        'total_linhas': linhas.count(),
        'linhas_ativas': linhas.filter(ativa=True).count(),
        'linhas_inativas': linhas.filter(ativa=False).count(),
    }
    
    return render(request, 'linhas/lista_linhas.html', context)

@login_required
def nova_linha(request):
    if request.method == 'POST':
        form = LinhaForm(request.POST, request.FILES)
        observacoes_lateral = request.POST.get('observacoes_lateral', '')
        anexos = request.FILES.getlist('anexos')
        if form.is_valid():
            linha = form.save(commit=False)
            linha.criado_por = request.user
            # Adiciona observações da lateral se ação for TT ou PORTABILIDADE
            if linha.acao in ['TT', 'PORTABILIDADE'] and observacoes_lateral:
                if linha.observacoes:
                    linha.observacoes += '\n' + observacoes_lateral
                else:
                    linha.observacoes = observacoes_lateral
            linha.save()
            # Salvar anexos (exemplo: salvar em pasta e registrar caminho, adaptar conforme modelo)
            for arquivo in anexos:
                with open(f'media/anexos/{arquivo.name}', 'wb+') as dest:
                    for chunk in arquivo.chunks():
                        dest.write(chunk)
            messages.success(request, f'Linha {linha.numero} cadastrada com sucesso!')
            return redirect('linhas:listalinhas')
    else:
        form = LinhaForm()
    return render(request, 'linhas/nova_linha.html', {'form': form})

@login_required
def editar_linha(request, pk):
    linha = get_object_or_404(Linha, pk=pk)
    
    if request.method == 'POST':
        form = LinhaForm(request.POST, instance=linha)
        if form.is_valid():
            form.save()
            messages.success(request, f'Linha {linha.numero} atualizada com sucesso!')
            return redirect('linhas:detalheslinha', pk=linha.pk)
    else:
        form = LinhaForm(instance=linha)
    
    return render(request, 'linhas/editar_linha.html', {'form': form, 'linha': linha})

@login_required
def detalhes_linha(request, pk):
    linha = get_object_or_404(Linha, pk=pk)
    return render(request, 'linhas/detalhes_linha.html', {'linha': linha})

@login_required
def excluir_linha(request, pk):
    linha = get_object_or_404(Linha, pk=pk)
    
    if request.method == 'POST':
        numero = linha.numero
        linha.delete()
        messages.success(request, f'Linha {numero} excluída com sucesso!')
        return redirect('linhas:listalinhas')
    
    return render(request, 'linhas/excluir_linha.html', {'linha': linha})

