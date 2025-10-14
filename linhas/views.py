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
from django.http import JsonResponse, HttpResponse
from .models import Linha, Protocolo
import csv

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


# Placeholder pages for top-level menu
@login_required
def dashboard(request):
    from django.db.models import Count, Avg
    from django.utils import timezone
    from datetime import timedelta

    # Compute billing cycle period: 19th -> 18th
    from datetime import datetime, date
    hoje = timezone.now().date()
    if hoje.day >= 19:
        ciclo_start = date(hoje.year, hoje.month, 19)
        # next month
        if hoje.month == 12:
            ciclo_end = date(hoje.year + 1, 1, 18)
        else:
            ciclo_end = date(hoje.year, hoje.month + 1, 18)
    else:
        # previous month start
        if hoje.month == 1:
            ciclo_start = date(hoje.year - 1, 12, 19)
        else:
            ciclo_start = date(hoje.year, hoje.month - 1, 19)
        ciclo_end = date(hoje.year, hoje.month, 18)

    # Use ciclo_start (00:00) to ciclo_end (23:59:59)
    from datetime import time
    dt_start = datetime.combine(ciclo_start, time.min)
    dt_end = datetime.combine(ciclo_end, time.max)

    qs = Linha.objects.filter(criado_em__gte=dt_start, criado_em__lte=dt_end)

    total_linhas = qs.count()
    linhas_ativas = qs.filter(ativa=True).count()
    linhas_inativas = qs.filter(ativa=False).count()
    media_valor_plano = qs.aggregate(avg_valor=Avg('valor_plano'))['avg_valor'] or 0

    # Novas linhas no período do ciclo: only from ESTOQUE (movimentadas) and PORTABILIDADE
    action_values = ['ESTOQUE', 'PORTABILIDADE']
    action_qs = qs.filter(acao__in=action_values)
    novas_30 = action_qs.count()

    # Distribuição por tipo de plano (top 10)
    tipo_plano_qs = qs.values('tipo_plano').annotate(count=Count('id')).order_by('-count')
    # Top 5, aggregate the rest as 'Outros'
    tipo_plano_list = list(tipo_plano_qs)
    top = tipo_plano_list[:5]
    outros = tipo_plano_list[5:]
    outros_count = sum([t['count'] for t in outros])
    tipo_plano_labels = [t['tipo_plano'] for t in top]
    tipo_plano_data = [t['count'] for t in top]
    if outros_count:
        tipo_plano_labels.append('Outros')
        tipo_plano_data.append(outros_count)

    # Novas linhas por dia (últimos 30 dias)
    dias = []
    contagens_dias = []
    # Series per day for the cycle period (from ciclo_start to ciclo_end)
    total_days = (ciclo_end - ciclo_start).days + 1
    for i in range(total_days):
        dia = ciclo_start + timedelta(days=i)
        # count only actions ESTOQUE or PORTABILIDADE on that day
        dia_qs = Linha.objects.filter(criado_em__date=dia, acao__in=action_values)
        count = dia_qs.count()
        dias.append(dia.strftime('%d/%m'))
        contagens_dias.append(count)

    # Protocol counts per day by status for the ciclo period
    protocolo_statuses = ['pendente', 'resolvido', 'cancelado']
    protocolos_por_status = {s: [] for s in protocolo_statuses}
    for i in range(total_days):
        dia = ciclo_start + timedelta(days=i)
        for s in protocolo_statuses:
            c = Protocolo.objects.filter(status=s, criado_em__date=dia).count()
            protocolos_por_status[s].append(c)

    # Pending protocols
    protocolos_pendentes_qs = Protocolo.objects.filter(status='pendente').order_by('-criado_em')
    protocolos_pendentes_count = protocolos_pendentes_qs.count()

    import json

    # format average as float or zero
    try:
        media_valor_num = float(media_valor_plano)
    except Exception:
        media_valor_num = 0.0

    context = {
        'total_linhas': total_linhas,
        'linhas_ativas': linhas_ativas,
        'linhas_inativas': linhas_inativas,
        # explicit alias for cancelled lines (business wants "canceladas")
        'linhas_canceladas': linhas_inativas,
        'novas_30': novas_30,
        'media_valor_plano': f"R$ {media_valor_num:,.2f}",
    'ciclo_start': ciclo_start.strftime('%Y-%m-%d'),
    'ciclo_end': ciclo_end.strftime('%Y-%m-%d'),
        # also provide JSON-serialized strings to safely embed in JS without json_script
        'tipo_plano_labels_json': json.dumps(tipo_plano_labels, ensure_ascii=False),
        'tipo_plano_data_json': json.dumps(tipo_plano_data),
        'dias_json': json.dumps(dias, ensure_ascii=False),
        'contagens_dias_json': json.dumps(contagens_dias),
    'protocolos_pendentes_count': protocolos_pendentes_count,
    # protocol time series for charts
    'protocolos_dias_labels_json': json.dumps(dias, ensure_ascii=False),
    'protocolos_pendente_series_json': json.dumps(protocolos_por_status['pendente']),
    'protocolos_resolvido_series_json': json.dumps(protocolos_por_status['resolvido']),
    'protocolos_cancelado_series_json': json.dumps(protocolos_por_status['cancelado']),
    }
    return render(request, 'dashboard.html', context)


@login_required
def protocolo(request):
    return render(request, 'protocolo.html')


@login_required
def relatorios(request):
    return render(request, 'relatorios.html')


@login_required
def configuracoes(request):
    return render(request, 'configuracoes.html')


@login_required
def export_linhas_cycle_csv(request):
    # compute ciclo as in dashboard
    from django.utils import timezone
    from datetime import datetime, date, time
    hoje = timezone.now().date()
    if hoje.day >= 19:
        ciclo_start = date(hoje.year, hoje.month, 19)
        if hoje.month == 12:
            ciclo_end = date(hoje.year + 1, 1, 18)
        else:
            ciclo_end = date(hoje.year, hoje.month + 1, 18)
    else:
        if hoje.month == 1:
            ciclo_start = date(hoje.year - 1, 12, 19)
        else:
            ciclo_start = date(hoje.year, hoje.month - 1, 19)
        ciclo_end = date(hoje.year, hoje.month, 18)

    # default period is the billing cycle
    dt_start = datetime.combine(ciclo_start, time.min)
    dt_end = datetime.combine(ciclo_end, time.max)

    # Allow overrides from GET params: periodo_start / periodo_end (YYYY-MM-DD)
    periodo_start = request.GET.get('periodo_start')
    periodo_end = request.GET.get('periodo_end')
    from datetime import datetime as _dt
    try:
        if periodo_start:
            dt_start = _dt.combine(_dt.strptime(periodo_start, '%Y-%m-%d').date(), time.min)
        if periodo_end:
            dt_end = _dt.combine(_dt.strptime(periodo_end, '%Y-%m-%d').date(), time.max)
    except Exception:
        # ignore parse errors and keep the cycle defaults
        pass

    qs = Linha.objects.filter(criado_em__gte=dt_start, criado_em__lte=dt_end)

    # Apply optional filters: empresa, cnpj, tipo_plano, numero, status
    empresa = request.GET.get('empresa')
    cnpj = request.GET.get('cnpj')
    tipo_plano = request.GET.get('tipo_plano')
    numero = request.GET.get('numero')
    status = request.GET.get('status')

    if empresa:
        qs = qs.filter(empresa__icontains=empresa)
    if cnpj:
        qs = qs.filter(cnpj__icontains=cnpj)
    if tipo_plano:
        qs = qs.filter(tipo_plano__icontains=tipo_plano)
    if numero:
        qs = qs.filter(numero__icontains=numero)
    if status:
        # map status to active flag
        if status == 'ativa':
            qs = qs.filter(ativa=True)
        elif status == 'cancelada':
            qs = qs.filter(ativa=False)

    # CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="linhas_{ciclo_start}_{ciclo_end}.csv"'
    writer = csv.writer(response)
    writer.writerow(['Numero', 'ICCID', 'Empresa', 'CNPJ', 'RP', 'Tipo Plano', 'Valor Plano', 'Ação', 'Ativa', 'Criado Em'])
    for l in qs:
        writer.writerow([l.numero, l.iccid, l.empresa, l.cnpj, l.rp, l.tipo_plano, str(l.valor_plano), l.acao, l.ativa, l.criado_em.strftime('%Y-%m-%d %H:%M')])
    return response


@login_required
def export_protocolos_pendentes_csv(request):
    # Allow optional date filters when exporting protocolos
    periodo_start = request.GET.get('periodo_start')
    periodo_end = request.GET.get('periodo_end')
    qs = Protocolo.objects.filter(status='pendente')
    from datetime import datetime
    try:
        if periodo_start:
            ds = datetime.strptime(periodo_start, '%Y-%m-%d')
            qs = qs.filter(criado_em__gte=ds)
        if periodo_end:
            de = datetime.strptime(periodo_end, '%Y-%m-%d')
            # include end of day
            from datetime import time as _time
            de = datetime.combine(de.date(), _time.max)
            qs = qs.filter(criado_em__lte=de)
    except Exception:
        # ignore parse errors
        pass
    qs = qs.order_by('-criado_em')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="protocolos_pendentes.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Titulo', 'Descricao', 'Criado Por', 'Criado Em', 'Status'])
    for p in qs:
        writer.writerow([p.id, p.titulo, (p.descricao or '')[:200], (p.criado_por.username if p.criado_por else ''), p.criado_em.strftime('%Y-%m-%d %H:%M'), p.status])
    return response

