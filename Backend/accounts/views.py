from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from .models import Profile


def _get_or_create_profile(user):
    """Garante que o utilizador tem um Profile (útil para users criados antes do signal)."""
    profile, _ = Profile.objects.get_or_create(user=user)
    return profile


# ---------------------------------------------------------------
# LOGIN / REGISTO / LOGOUT
# ---------------------------------------------------------------

@ensure_csrf_cookie
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        # -------- REGISTO --------
        if 'register' in request.POST:
            name = request.POST.get('name', '').strip()
            email = request.POST.get('register_email', '').strip().lower()
            password = request.POST.get('register_password', '')
            confirm = request.POST.get('confirm_password', '')

            if not name or not email or not password:
                messages.error(request, 'Preenche todos os campos do registo.')
                return redirect('login')

            if password != confirm:
                messages.error(request, 'As passwords não coincidem.')
                return redirect('login')

            if len(password) < 8:
                messages.error(request, 'A password tem de ter pelo menos 8 caracteres.')
                return redirect('login')

            if User.objects.filter(username=email).exists() or User.objects.filter(email=email).exists():
                messages.error(request, 'Já existe uma conta com esse email.')
                return redirect('login')

            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=name,
            )
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f'Bem-vindo, {name}!')
            return redirect('dashboard')

        # -------- LOGIN --------
        elif 'login' in request.POST:
            email = request.POST.get('login_email', '').strip().lower()
            password = request.POST.get('login_password', '')

            if not email or not password:
                messages.error(request, 'Preenche o email e a password.')
                return redirect('login')

            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Email ou password inválidos.')
                return redirect('login')

    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def dashboard_view(request):
    _get_or_create_profile(request.user)
    return render(request, 'accounts/dashboard.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Sessão terminada.')
    return redirect('login')


# ---------------------------------------------------------------
# DEFINIÇÕES DA CONTA
# ---------------------------------------------------------------

@login_required(login_url='login')
def settings_view(request):
    profile = _get_or_create_profile(request.user)
    return render(request, 'accounts/settings.html', {
        'profile': profile,
    })


@login_required(login_url='login')
@require_POST
def update_profile(request):
    user = request.user
    profile = _get_or_create_profile(user)

    nome = request.POST.get('nome', '').strip()
    telefone = request.POST.get('telefone', '').strip()
    data_nasc = request.POST.get('data_nascimento', '').strip()
    moeda = request.POST.get('moeda_preferida', 'EUR').strip()

    if nome:
        user.first_name = nome
        user.save()

    profile.telefone = telefone
    profile.data_nascimento = data_nasc if data_nasc else None
    profile.moeda_preferida = moeda

    # Upload de avatar (se enviado)
    if 'avatar' in request.FILES:
        avatar = request.FILES['avatar']
        if avatar.size > 5 * 1024 * 1024:  # 5 MB
            messages.error(request, 'A imagem é demasiado grande (máx. 5 MB).')
            return redirect('settings')
        if not avatar.content_type.startswith('image/'):
            messages.error(request, 'O ficheiro tem de ser uma imagem.')
            return redirect('settings')
        profile.avatar = avatar

    profile.save()
    messages.success(request, 'Perfil atualizado.')
    return redirect('settings')


@login_required(login_url='login')
@require_POST
def remove_avatar(request):
    profile = _get_or_create_profile(request.user)
    if profile.avatar:
        profile.avatar.delete(save=False)
        profile.avatar = None
        profile.save()
        messages.success(request, 'Foto de perfil removida.')
    return redirect('settings')


@login_required(login_url='login')
@require_POST
def change_password(request):
    user = request.user
    atual = request.POST.get('password_atual', '')
    nova = request.POST.get('password_nova', '')
    confirmar = request.POST.get('password_confirmar', '')

    if not user.check_password(atual):
        messages.error(request, 'A password atual está incorreta.')
        return redirect('settings')

    if len(nova) < 8:
        messages.error(request, 'A nova password tem de ter pelo menos 8 caracteres.')
        return redirect('settings')

    if nova != confirmar:
        messages.error(request, 'As novas passwords não coincidem.')
        return redirect('settings')

    user.set_password(nova)
    user.save()
    # Mantém o user logado depois de mudar a password
    update_session_auth_hash(request, user)
    messages.success(request, 'Password alterada com sucesso.')
    return redirect('settings')


@login_required(login_url='login')
@require_POST
def delete_account(request):
    user = request.user
    password = request.POST.get('password_confirmar_delete', '')

    if not user.check_password(password):
        messages.error(request, 'Password incorreta. Conta não foi apagada.')
        return redirect('settings')

    email = user.email
    logout(request)
    user.delete()
    messages.success(request, f'A conta {email} foi apagada.')
    return redirect('login')
