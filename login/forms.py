from django import forms

class MudarSenhaForm(forms.Form):
    senha_atual = forms.CharField(widget=forms.PasswordInput(), label='Senha Atual', required=True)
    nova_senha = forms.CharField(widget=forms.PasswordInput(), label='Nova Senha', required=True)
    nova_senha_confirma = forms.CharField(widget=forms.PasswordInput(), label='Confirma Nova Senha', required=True)