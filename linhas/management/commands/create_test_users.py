from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Cria ou atualiza dois usuários normais para testes de bloqueio de login"

    def handle(self, *args, **options):
        users = [
            ("teste1", "SenhaTeste123"),
            ("teste2", "SenhaTeste123"),
        ]
        for username, password in users:
            user, created = User.objects.get_or_create(username=username, defaults={'is_staff': False, 'is_superuser': False})
            if not created:
                # garante que não é staff/admin
                user.is_staff = False
                user.is_superuser = False
            user.set_password(password)
            user.save()
            status = 'criado' if created else 'atualizado'
            self.stdout.write(self.style.SUCCESS(f"Usuário {username} {status} com senha '{password}'"))

        self.stdout.write(self.style.WARNING("Use estes usuários para testar 3 tentativas de login incorretas e o desbloqueio."))
