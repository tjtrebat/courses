from django import forms

class LoginForm(forms.Form):
    username = forms.RegexField(regex=r'^\w+$', max_length=30, 
        widget=forms.TextInput(), 
        error_messages={'invalid': "This value must contain only letters, numbers and underscores."})
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))