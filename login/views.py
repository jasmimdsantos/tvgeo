from django.shortcuts import RequestContext, HttpResponse, redirect, loader
from django.utils import http
from django.views.decorators import cache
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.core.mail import send_mail
import random
import string
from django.conf import settings
from .forms import MudarSenhaForm
from django.shortcuts import render
from toolbox.sitetools import sitemap

@cache.never_cache
def loginusr(request):
    """
    View da página de Login

    Tem duas funções: Processar o reset de senha e fazer o Login.
    LOGIN: Verifica se o usuário e senhas estão no sistema, caso contrário, informa respectivas mensagens de erro.
    PASS RESET: Reseta a senha de acordo com o usuário informado, enviando por email a nova senha gerada randomicamente.
    @param request:
    @return:
    """
    template = loader.get_template('login/login.html')

    page = sitemap ( request.get_full_path ( ) ).context

    context = {}
    if request.POST:
        username = request.POST['mail']
        password = request.POST['password']

        if 'email-reset' in request.POST:
            reset_mail = request.POST['email-reset']
            try:
                user_reset = User.objects.get(username__exact=reset_mail)
                if user_reset:
                    pass_reset = pass_generator()
                    user_reset.set_password(pass_reset)
                    user_reset.save()

                    email_corpo = u"Sua senha foi alterada no sistema. SUA NOVA SENHA É: "+pass_reset
                    email_titulo = u"Senha Resetada"
                    email_destino = [user_reset.email]
                    send_mail(email_titulo, email_corpo, settings.EMAIL_HOST_USER, email_destino)
                    state = {'msg': u"Um email foi enviado para sua caixa de entrada contendo sua nova senha.", 'mode': 'sucess'}
                else:
                    state = {'msg': u'Usuário não existe no banco de dados.', 'mode': 'error'}
            except:
                state = {'msg': u"Ocorreu um erro ao redefinir sua senha.", 'mode': 'error'}

        else:
            redirect_to = request.POST.get('next', request.GET.get('next', ''))

            if not http.is_safe_url(redirect_to, request.get_host()):
                redirect_to = '/home/'

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect(redirect_to)
                else:
                    state = {'msg': u"Sua conta esta desativada, por favor entre em contato com o administrador..", 'mode': 'warning'}
            else:
                state = {'msg': u"Usuário ou senha incorretos.", 'mode': 'error'}

        context['state'] = state
        context['username'] = username
        context.update(page)

    req_context = RequestContext(request, context)
    return HttpResponse(template.render(req_context))



def pass_generator(size=8, chars=string.ascii_uppercase + string.digits):
    """
    Gera senha para usuários no sistema.

    @param size: Tamanho da senha. Padrão: 8 Caracteres
    @param chars: Métodos de string para gerar a senha. Padrão: Letras maíusculas e dígitos.
    @return: Senha gerada de acordo com os parametros passados ou pré definidos.
    """
    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))


def mudasenha(request):
    """
    View para mudar a senha do usuário logado.

    Verifica se o formulário é valido, então prossegue verificando se
    a nova senha e nova senha confirma são iguais, verifica se a senha antiga é a mesma no sistema. Se não
    passar em alguma verificação, então retorna seus respectivos erros em state em forma de mensagem para usuário.

    @param request:
    @return:
    """
    page = sitemap ( request.get_full_path ( ) ).context
    form = MudarSenhaForm(request.POST or None)
    context = {}
    state=''
    context['page'] = "Muda Senha"
    if request.POST:
        senha_atual = request.POST['senha_atual']
        nova_senha = request.POST['nova_senha']
        nova_senha_confirma = request.POST['nova_senha_confirma']
        if form.is_valid():
            if nova_senha == nova_senha_confirma:
                user_auth = User.objects.get(username__exact=request.user.username)
                if user_auth.check_password(senha_atual):
                    user_auth.set_password(nova_senha)
                    user_auth.save()
                    state = {'msg': "A sua senha foi alterada com sucesso!", 'mode': 'sucess'}
                else:
                    state = {'msg': "A Senha Atual digitada não confere com a do sistema.", 'mode': 'error'}
            else:
                state = {'msg': "A confirmação de senha não confere.", 'mode': 'warning'}

        context['state'] = state

    context['form'] = form
    context.update(page)
    return render(request, 'login/mudasenha.html', context)

def webhome(request):
    """
    View que renderiza conteúdo a ser mostrado em todas as páginas do home.

    @param request:
    @return:
    """
    page = sitemap ( request.get_full_path ( ) ).context
    context = {'username' : request.user.username }
    context.update(page)
    return render(request, 'login/webhome.html', context)

def home(request):
    """
    View para fazer logout do sistema

    @param request:
    @return:
    """
    request.session.items = []
    request.session.modified = True
    logout(request)
    return render(request, 'login/home.html')