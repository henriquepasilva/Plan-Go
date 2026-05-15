from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


MOEDAS = [
    ('EUR', 'Euro (€)'),
    ('USD', 'Dólar Americano ($)'),
    ('GBP', 'Libra (£)'),
    ('BRL', 'Real (R$)'),
    ('JPY', 'Iene (¥)'),
]


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    telefone = models.CharField(max_length=20, blank=True, default='')
    data_nascimento = models.DateField(null=True, blank=True)
    moeda_preferida = models.CharField(
        max_length=3,
        choices=MOEDAS,
        default='EUR'
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Perfil de {self.user.email}'

    @property
    def iniciais(self):
        """Devolve as iniciais para o avatar fallback."""
        nome = (self.user.first_name or self.user.username or '?').strip()
        partes = nome.split()
        if len(partes) >= 2:
            return (partes[0][0] + partes[-1][0]).upper()
        return nome[:2].upper()


# Cria automaticamente um Profile sempre que se cria um User novo
@receiver(post_save, sender=User)
def criar_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
