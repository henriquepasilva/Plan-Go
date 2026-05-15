from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def login_view(request):
    # Se já estiver autenticado, manda para o dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        # -------- REGISTO --------
        if 'register' in request.POST:
            name = request.POST.get('name', '').strip()
            email = request.POST.get('register_email', '').strip().lower()
            password = request.POST.get('register_password', '')
            confirm = request.POST.get('confirm_password', '')

            # Validações
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

            # Criar utilizador (usamos o email como username para garantir unicidade)
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=name,
            )
            login(request, user)
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
    return render(request, 'accounts/dashboard.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Sessão terminada.')
    return redirect('login')
