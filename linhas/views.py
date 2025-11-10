from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.utils import timezone
from datetime import timedelta
from .models import LoginAttempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def login_view(request):
    if request.method == 'POST' and request.POST.get('login_form'):
        username = request.POST.get('username')
        password = request.POST.get('password')
        ip_address = get_client_ip(request)
        
        print(f"Login attempt - Username: {username}, IP: {ip_address}")
        print(f"POST data: {request.POST}")
        
        # Check if user is blocked
        login_attempt = LoginAttempt.objects.filter(
            username=username,
            ip_address=ip_address,
            is_blocked=True
        ).first()

        if login_attempt and login_attempt.is_currently_blocked():
            remaining_time = login_attempt.blocked_until - timezone.now()
            minutes = int(remaining_time.total_seconds() / 60)
            return render(request, 'login.html', {
                'error': f'Conta bloqueada. Tente novamente em {minutes} minutos ou entre em contato com o suporte.',
                'show_support': True
            })

        user = authenticate(username=username, password=password)
        
        if user is not None:
            # Reset login attempts on successful login
            LoginAttempt.objects.filter(username=username, ip_address=ip_address).delete()
            login(request, user)
            return redirect('dashboard')
        else:
            # Track failed login attempt
            login_attempt = LoginAttempt.objects.filter(
                username=username,
                ip_address=ip_address,
                is_blocked=False
            ).first()

            print(f"Failed login - Current attempt: {login_attempt}")

            if login_attempt:
                login_attempt.attempt_count += 1
                print(f"Incrementing attempt count to: {login_attempt.attempt_count}")
                
                if login_attempt.attempt_count >= 3:
                    print("Blocking user - 3 or more attempts")
                    login_attempt.is_blocked = True
                    login_attempt.blocked_until = timezone.now() + timedelta(minutes=15)
                    login_attempt.save()
                    return render(request, 'login.html', {
                        'error': 'Conta bloqueada por 15 minutos devido a múltiplas tentativas incorretas.',
                        'show_support': True
                    })
                login_attempt.save()
                print(f"Saved attempt count: {login_attempt.attempt_count}")
            else:
                print("Creating new login attempt record")
                login_attempt = LoginAttempt.objects.create(
                    username=username,
                    ip_address=ip_address
                )
                print(f"Created new attempt record: {login_attempt.id}")

            return render(request, 'login.html', {
                'error': 'Usuário ou senha incorretos'
            })

    return render(request, 'login.html')

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

def buscar_cnpj_api_externa(request):
    """
    View para buscar dados de CNPJ usando APIs externas (ReceitaWS e BrasilAPI)
    
    Usage: GET /linhas/buscar-cnpj-api/?cnpj=19131243000197
    """
    import requests
    import re
    
    cnpj = request.GET.get('cnpj', '')
    
    if not cnpj:
        return JsonResponse({
            'success': False, 
            'error': 'CNPJ não informado'
        }, status=400)
    
    # Limpar CNPJ
    cnpj_limpo = re.sub(r'\D', '', cnpj)
    
    if len(cnpj_limpo) != 14:
        return JsonResponse({
            'success': False,
            'error': 'CNPJ deve ter 14 dígitos'
        }, status=400)
    
    try:
        # Tentar BrasilAPI primeiro
        url_brasil = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj_limpo}"
        response = requests.get(url_brasil, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            dados_padronizados = {
                'cnpj': data.get('cnpj', cnpj_limpo),
                'nome': data.get('razao_social', ''),
                'razao_social': data.get('razao_social', ''),
                'fantasia': data.get('nome_fantasia', ''),
                'situacao': data.get('descricao_situacao_cadastral', ''),
                'endereco': data.get('logradouro', ''),
                'numero': data.get('numero', ''),
                'complemento': data.get('complemento', ''),
                'bairro': data.get('bairro', ''),
                'municipio': data.get('municipio', ''),
                'uf': data.get('uf', ''),
                'cep': data.get('cep', ''),
                'telefone': data.get('ddd_telefone_1', ''),
                'email': data.get('email', ''),
                'data_abertura': data.get('data_inicio_atividade', ''),
                'fonte': 'BrasilAPI'
            }
            
            return JsonResponse({
                'success': True,
                'dados': dados_padronizados
            })
        
    except Exception as e:
        pass  # Fallback para ReceitaWS
    
    try:
        # Fallback ReceitaWS
        url_receita = f"https://www.receitaws.com.br/v1/cnpj/{cnpj_limpo}"
        response = requests.get(url_receita, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Verificar se a API retornou erro
            if data.get("status") == "ERROR":
                return JsonResponse({
                    'success': False,
                    'error': data.get('message', 'Erro na consulta CNPJ')
                }, status=404)
            
            dados_padronizados = {
                'cnpj': data.get('cnpj', cnpj_limpo),
                'nome': data.get('nome', ''),
                'razao_social': data.get('nome', ''),
                'fantasia': data.get('fantasia', ''),
                'situacao': data.get('situacao', ''),
                'endereco': data.get('logradouro', ''),
                'numero': data.get('numero', ''),
                'complemento': data.get('complemento', ''),
                'bairro': data.get('bairro', ''),
                'municipio': data.get('municipio', ''),
                'uf': data.get('uf', ''),
                'cep': data.get('cep', ''),
                'telefone': data.get('telefone', ''),
                'email': data.get('email', ''),
                'data_abertura': data.get('abertura', ''),
                'fonte': 'ReceitaWS'
            }
            
            return JsonResponse({
                'success': True,
                'dados': dados_padronizados
            })
        
    except Exception as e:
        pass
    
    return JsonResponse({
        'success': False,
        'error': 'CNPJ não encontrado nas APIs externas'
    }, status=404)

def test_cnpj_api_view(request):
    """
    View para página de teste da API de CNPJ
    """
    return render(request, 'test_cnpj_api.html')

def debug_cnpj_button_view(request):
    """
    View para debug do botão CNPJ
    """
    return render(request, 'debug_cnpj_button.html')

def debug_cnpj_complete_view(request):
    """
    View para debug completo do CNPJ
    """
    return render(request, 'debug_cnpj_complete.html')

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


def buscar_empresas(request):
    """AJAX: retornar lista de empresas (empresa, cnpj) que contenham o termo q
    Retorna JSON: [{ 'empresa': 'Nome', 'cnpj': '00000000000000' }, ...]
    """
    q = request.GET.get('q', '').strip()
    # buscar por empresa parcialmente
    empresas_qs = Linha.objects.filter(empresa__icontains=q).values('empresa', 'cnpj').distinct()[:50]
    # deduplicate by empresa keeping first cnpj
    seen = set()
    results = []
    for row in empresas_qs:
        nome = row.get('empresa') or ''
        cnpj = row.get('cnpj') or ''
        if not nome:
            continue
        if nome in seen:
            continue
        seen.add(nome)
        results.append({'empresa': nome, 'cnpj': cnpj})
    return JsonResponse(results, safe=False)


def buscar_clientes(request):
    """AJAX: retornar lista de clientes existentes que contenham o termo q
    Retorna JSON: [{ 'id': 1, 'empresa': 'Nome', 'cnpj': '00000000000000', 'fantasia': '...', 'razao_social': '...'}, ...]
    """
    q = request.GET.get('q', '').strip()
    qs = Cliente.objects.all()
    if q:
        qs = qs.filter(models.Q(empresa__icontains=q) | models.Q(cnpj__icontains=q) | models.Q(fantasia__icontains=q) | models.Q(razao_social__icontains=q))
    results = []
    for c in qs[:50]:
        results.append({'id': c.id, 'empresa': c.empresa, 'cnpj': c.cnpj, 'fantasia': c.fantasia, 'razao_social': c.razao_social})
    return JsonResponse(results, safe=False)
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Linha, Protocolo, Cliente
from .forms import LinhaForm, BuscaLinhaForm, ClienteForm
from django.urls import reverse

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
def cliente_novo(request):
    """Criar novo cliente (form simples)."""
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            # Verifica se deve redirecionar para nova linha ou ficar na página
            next_action = request.POST.get('next_action', 'stay')
            
            if next_action == 'nova_linha':
                # Adiciona mensagem antes do redirect
                messages.success(request, f'Cliente "{cliente.empresa}" cadastrado com sucesso!')
                # Redireciona para a página de nova linha e já preenche empresa/cnpj via GET
                url = reverse('linhas:novalinha')
                params = f'?empresa={cliente.empresa}&cnpj={cliente.cnpj}'
                return redirect(url + params)
            else:
                # Fica na página atual, limpa o formulário para novo cadastro
                messages.success(request, f'Cliente "{cliente.empresa}" cadastrado com sucesso! Operação concluída.')
                form = ClienteForm()
                return render(request, 'linhas/novo_cliente.html', {
                    'form': form,
                    'cliente_salvo': cliente
                })
        else:
            messages.error(request, 'Erro ao cadastrar cliente. Verifique os dados informados.')
    else:
        form = ClienteForm()
    return render(request, 'linhas/novo_cliente.html', {'form': form})


@login_required
def cliente_create_ajax(request):
    """Receive AJAX POST to create a Cliente and return JSON response."""
    from django.http import JsonResponse
    if request.method != 'POST':
        return JsonResponse({'success': False, 'errors': {'__all__': 'Método inválido.'}}, status=400)
    form = ClienteForm(request.POST)
    if form.is_valid():
        cliente = form.save()
        return JsonResponse({'success': True, 'cliente': {
            'id': cliente.id,
            'empresa': cliente.empresa,
            'cnpj': cliente.cnpj,
            'razao_social': cliente.razao_social,
            'fantasia': cliente.fantasia,
        }})
    else:
        # format errors as dict
        errors = {k: v for k, v in form.errors.items()}
        return JsonResponse({'success': False, 'errors': errors}, status=400)

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
            # Attempt to attach a Cliente if one exists with the same CNPJ or empresa
            try:
                import re
                cliente = None
                if linha.cnpj:
                    cnpj_digits = re.sub(r"\D", "", linha.cnpj)
                    cliente = Cliente.objects.filter(cnpj__icontains=cnpj_digits).first()
                if not cliente and linha.empresa:
                    cliente = Cliente.objects.filter(empresa__iexact=linha.empresa).first()
                if cliente:
                    linha.cliente = cliente
                    linha.save()
            except Exception:
                # don't block save on any lookup error
                pass
            # Salvar anexos (exemplo: salvar em pasta e registrar caminho, adaptar conforme modelo)
            for arquivo in anexos:
                with open(f'media/anexos/{arquivo.name}', 'wb+') as dest:
                    for chunk in arquivo.chunks():
                        dest.write(chunk)
            messages.success(request, f'Linha {linha.numero} cadastrada com sucesso!')
            return redirect('linhas:listalinhas')
    else:
        # Allow prefilling empresa/cnpj when redirected after creating a Cliente
        initial = {}
        empresa_prefill = request.GET.get('empresa')
        cnpj_prefill = request.GET.get('cnpj')
        if empresa_prefill:
            initial['empresa'] = empresa_prefill
        if cnpj_prefill:
            initial['cnpj'] = cnpj_prefill
        form = LinhaForm(initial=initial)
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
    # Provide distinct tipo_plano values so template can render a select
    tipo_planos = Linha.objects.order_by('tipo_plano').values_list('tipo_plano', flat=True).distinct()
    context = {
        'tipo_plano_choices': list(tipo_planos),
    }
    return render(request, 'relatorios.html', context)


@login_required
def configuracoes(request):
    # Lista simples de usuários atualmente bloqueados (se houver)
    bloqueados = LoginAttempt.objects.filter(is_blocked=True, blocked_until__gt=timezone.now()) \
        .values_list('username', flat=True).distinct()
    return render(request, 'configuracoes.html', { 'bloqueados': list(bloqueados) })

@login_required
def desbloquear_usuario(request):
    """Desbloqueia manualmente um usuário removendo registros de LoginAttempt bloqueados.

    Regras:
    - Apenas usuários staff podem executar.
    - Recebe POST com campo 'username'.
    - Remove tentativas para aquele username e IP (todas) marcadas como bloqueadas.
    - Exibe mensagem de sucesso ou erro e redireciona para configurações.
    """
    if not request.user.is_staff:
        messages.error(request, 'Você não tem permissão para desbloquear usuários.')
        return redirect('linhas:configuracoes')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        if not username:
            messages.error(request, 'Informe o nome de usuário para desbloquear.')
            return redirect('linhas:configuracoes')

        # Remover todas as tentativas para o username (independente do IP) para reset total
        attempts = LoginAttempt.objects.filter(username=username)
        count = attempts.count()
        if count == 0:
            messages.warning(request, f'Nenhum bloqueio ativo encontrado para "{username}".')
        else:
            attempts.delete()
            messages.success(request, f'Usuário "{username}" desbloqueado. ({count} registro(s) removido(s))')
        return redirect('linhas:configuracoes')

    return redirect('linhas:configuracoes')


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
        # server-side validation: start must not be after end
        if periodo_start and periodo_end and dt_start > dt_end:
            messages.error(request, 'Período inválido: data de início posterior à data fim.')
            return redirect('linhas:relatorios')
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

    # server-side CNPJ validation (if provided)
    if cnpj:
        import re
        cnpj_digits = re.sub(r'\D', '', cnpj)
        if len(cnpj_digits) != 14:
            messages.error(request, 'CNPJ inválido: verifique o número informado.')
            return redirect('linhas:relatorios')
        # normalize to the stored format by filtering with contains on digits
        qs = qs.filter(cnpj__icontains=cnpj_digits)

    if empresa:
        qs = qs.filter(empresa__icontains=empresa)
    if tipo_plano:
        qs = qs.filter(tipo_plano__icontains=tipo_plano)

    # Behavior requirement: when a CNPJ or empresa is provided, numero filter should only
    # be applied if the given numero actually belongs to that CNPJ/empresa. Otherwise
    # return all lines linked to that CNPJ/empresa (ignore numero filter).
    if numero:
        if cnpj or empresa:
            # check within the already filtered qs (which contains only lines for that cnpj/empresa)
            if qs.filter(numero__icontains=numero).exists():
                qs = qs.filter(numero__icontains=numero)
            else:
                # numero not associated with this CNPJ/empresa — ignore numero filter
                pass
        else:
            # no cnpj/empresa context — apply numero filter globally
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
def export_linhas_cycle_xlsx(request):
    """Generate an XLSX file with the same filters as CSV export."""
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
        if periodo_start and periodo_end and dt_start > dt_end:
            messages.error(request, 'Período inválido: data de início posterior à data fim.')
            return redirect('linhas:relatorios')
    except Exception:
        pass

    qs = Linha.objects.filter(criado_em__gte=dt_start, criado_em__lte=dt_end)

    # same optional filters as CSV
    empresa = request.GET.get('empresa')
    cnpj = request.GET.get('cnpj')
    tipo_plano = request.GET.get('tipo_plano')
    numero = request.GET.get('numero')
    status = request.GET.get('status')

    if cnpj:
        import re
        cnpj_digits = re.sub(r'\D', '', cnpj)
        if len(cnpj_digits) != 14:
            messages.error(request, 'CNPJ inválido: verifique o número informado.')
            return redirect('linhas:relatorios')
        qs = qs.filter(cnpj__icontains=cnpj_digits)

    if empresa:
        qs = qs.filter(empresa__icontains=empresa)
    if tipo_plano:
        qs = qs.filter(tipo_plano__icontains=tipo_plano)

    # Same business rule as CSV: if CNPJ or empresa provided, only apply numero filter
    # when the numero exists for that CNPJ/empresa; otherwise ignore numero and return
    # all lines for that CNPJ/empresa.
    if numero:
        if cnpj or empresa:
            if qs.filter(numero__icontains=numero).exists():
                qs = qs.filter(numero__icontains=numero)
            else:
                pass
        else:
            qs = qs.filter(numero__icontains=numero)

    if status:
        if status == 'ativa':
            qs = qs.filter(ativa=True)
        elif status == 'cancelada':
            qs = qs.filter(ativa=False)

    # generate xlsx in-memory
    from io import BytesIO
    try:
        from openpyxl import Workbook
    except Exception:
        # openpyxl not installed; return a helpful message
        messages.error(request, 'openpyxl não está instalado no servidor. Instale via pip install openpyxl')
        return redirect('linhas:relatorios')

    wb = Workbook()
    ws = wb.active
    ws.title = 'Linhas'
    headers = ['Numero', 'ICCID', 'Empresa', 'CNPJ', 'RP', 'Tipo Plano', 'Valor Plano', 'Ação', 'Ativa', 'Criado Em']
    ws.append(headers)
    for l in qs:
        ws.append([l.numero, l.iccid, l.empresa, l.cnpj, l.rp, l.tipo_plano, float(l.valor_plano or 0), l.acao, 'Sim' if l.ativa else 'Não', l.criado_em.strftime('%Y-%m-%d %H:%M')])

    bio = BytesIO()
    wb.save(bio)
    bio.seek(0)

    response = HttpResponse(bio.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="linhas_{ciclo_start}_{ciclo_end}.xlsx"'
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
        # server-side validation: if both provided, ensure start <= end
        if periodo_start and periodo_end:
            # compare by date
            ds_check = datetime.strptime(periodo_start, '%Y-%m-%d')
            de_check = datetime.strptime(periodo_end, '%Y-%m-%d')
            if ds_check > de_check:
                messages.error(request, 'Período inválido: data de início posterior à data fim.')
                return redirect('linhas:relatorios')
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

@login_required
def fidelidade(request):
    """
    Página de fidelidade com formulário para número da linha,
    cliente e RP (campos automáticos) e observações
    """
    if request.method == 'POST':
        from .forms import FidelidadeForm
        form = FidelidadeForm(request.POST)
        
        if form.is_valid():
            fidelidade = form.save(user=request.user)
            messages.success(request, f'Fidelidade da linha {fidelidade.linha.numero} cadastrada com sucesso!')
            
            # Redirecionar para a mesma página limpo ou para lista de fidelidades
            return redirect('linhas:fidelidade')
        else:
            messages.error(request, 'Erro ao cadastrar fidelidade. Verifique os dados informados.')
    else:
        from .forms import FidelidadeForm
        form = FidelidadeForm()
    
    return render(request, 'linhas/fidelidade.html', {'form': form})

def buscar_linha_dados(request):
    """
    AJAX endpoint para buscar dados da linha (cliente e RP)
    baseado no número da linha selecionado
    """
    numero = request.GET.get('numero', '')
    
    if not numero:
        return JsonResponse({
            'success': False,
            'error': 'Número da linha não informado'
        })
    
    try:
        linha = Linha.objects.filter(numero=numero).first()
        
        if linha:
            # Buscar nome do cliente baseado no CNPJ da linha
            cliente_nome = ""
            if linha.cliente:
                cliente_nome = linha.cliente.empresa
            elif linha.empresa:
                cliente_nome = linha.empresa
            
            return JsonResponse({
                'success': True,
                'dados': {
                    'cliente': cliente_nome,
                    'rp': linha.rp or '',
                    'empresa': linha.empresa or '',
                    'cnpj': linha.cnpj or '',
                    'ativa': linha.ativa,
                    'tipo_plano': linha.tipo_plano or '',
                    'operadora': linha.operadora or '',
                    'valor_plano': str(linha.valor_plano) if linha.valor_plano else '',
                    'iccid': linha.iccid or '',
                    'status': 'Ativa' if linha.ativa else 'Inativa'
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'Linha não encontrada'
            })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Erro ao buscar dados da linha: {str(e)}'
        })

