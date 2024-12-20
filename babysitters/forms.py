
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'password-field', 'id': 'babysitter-password'}),
        label="Mot de passe"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'password-field', 'id': 'babysitter-confirm-password'}),
        label="Confirmez le mot de passe"
    )

    class Meta:
        model = Babysitter
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'experience_years', 'hourly_rate', 'bio', 'certifications', 'availability']

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        # Vérification des mots de passe
        if password != confirm_password:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")

        # Vérifier si l'email existe déjà dans le modèle `User`
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Un compte avec cet email existe déjà.")

        return cleaned_data

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'password-field', 'id': 'babysitter-password'}),
        label="Mot de passe"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'password-field', 'id': 'babysitter-confirm-password'}),
        label="Confirmez le mot de passe"
    )
 
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cet email est déjà utilisé pour un autre compte.")
        return email