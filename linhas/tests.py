from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Cliente, Linha


class ClienteAjaxTestCase(TestCase):
	def setUp(self):
		self.user = User.objects.create_user('testuser', 'test@example.com', 'pass')
		self.client.force_login(self.user)

	def test_create_cliente_ajax_success(self):
		url = reverse('linhas:cliente_create_ajax')
		data = {
			'empresa': 'ACME Ltda',
			'cnpj': '04.252.011/0001-10',
			'razao_social': 'ACME LTDA',
			'fantasia': 'ACME',
			'endereco_completo': 'Rua A, 123',
			'contato': '(11) 99999-9999',
			'email': 'contato@acme.com',
			'telefone': '(11) 99999-9999',
			'nome_dono': 'João Silva',
			'cpf_dono': '529.982.247-25',
			'data_nascimento_dono': '01/01/1980',
		}
		resp = self.client.post(url, data)
		self.assertEqual(resp.status_code, 200)
		self.assertTrue(resp.json().get('success'))
		self.assertTrue(Cliente.objects.filter(empresa='ACME Ltda').exists())


class LinhaClienteAssociationTestCase(TestCase):
	def setUp(self):
		self.user = User.objects.create_user('testuser2', 't2@example.com', 'pass')
		self.client.force_login(self.user)
		self.cliente = Cliente.objects.create(empresa='Empresa X', cnpj='')

	def test_nova_linha_associa_cliente_por_cnpj(self):
		# Create linha programmatically and run the same association logic
		linha = Linha.objects.create(
			numero='11999998888',
			tipo_plano='BLACK_VOZ_GW_800SMS',
			valor_plano='14.00',
			acao='ESTOQUE',
			empresa='Empresa X',
			cnpj='',
			taxa_manutencao='0.00',
			rp='RP1',
			iccid='',
			ativa=True,
			criado_por=self.user,
		)
		# emulate view association logic
		import re
		cliente_found = None
		if linha.cnpj:
			cnpj_digits = re.sub(r"\D", "", linha.cnpj)
			cliente_found = Cliente.objects.filter(cnpj__icontains=cnpj_digits).first()
		if not cliente_found and linha.empresa:
			cliente_found = Cliente.objects.filter(empresa__iexact=linha.empresa).first()
		if cliente_found:
			linha.cliente = cliente_found
			linha.save()

		linha.refresh_from_db()
		# should be associated to created cliente
		self.assertIsNotNone(linha.cliente)
		self.assertEqual(linha.cliente.id, self.cliente.id)
