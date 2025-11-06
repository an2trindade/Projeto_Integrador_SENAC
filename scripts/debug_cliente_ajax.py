import os
import sys
import django
# ensure project root is on path so gestor_linhas package can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestor_linhas.settings')
django.setup()
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse

c = Client()
user = User.objects.create_user('debuguser', 'd@example.com', 'pass')
c.force_login(user)
url = reverse('linhas:cliente_create_ajax')
data = {
    'empresa': 'ACME Ltda',
    'cnpj': '04.252.011/0001-10',
    'razao_social': 'ACME LTDA',
    'fantasia': 'ACME',
    'endereco_completo': 'Rua A, 123',
    'nome_dono': 'João Silva',
    'cpf_dono': '529.982.247-25',
}
resp = c.post(url, data)
print('status:', resp.status_code)
try:
    print('json:', resp.json())
except Exception:
    print('content:', resp.content)
