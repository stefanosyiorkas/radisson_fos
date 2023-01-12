from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Foods


class Registration(UserCreationForm):
    # username = forms.CharField(label='Username', required=True, help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",max_length="50", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'jsmith'}))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control form-control-sm rounded-0', 'placeholder': "jsmith"})
        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control form-control-sm rounded-0', 'placeholder': "*******"})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control form-control-sm rounded-0', 'placeholder': "*******"})


class Login(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control form-control-sm rounded-0', 'placeholder': "Enter username"})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control form-control-sm rounded-0', 'placeholder': "Enter password"})


class FoodsForm(forms.ModelForm):
    class Meta:
        model = Foods
        fields = '__all__'

    allergies = forms.CharField(required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter allergen number and seperate with a comma (e.g. 1,2,3)'}),
        help_text="""
        <style>
            .table td,
             .table th {
                font-size: 1rem;
                padding: 0.1rem;
            }
        </style>
        <div class="container">
        <table class="table">
        <thead>
        <tr>
            <th>#</th>
            <th>Allergen</th>
            <th>Αλλεργιογόνο</th>
        </tr>
        </thead>
        <tbody>
        <tr>
            <td>1</td>
            <td>Peanuts</td>
            <td>Φιστίκια</td>
        </tr>
        <tr>
            <td>2</td>
            <td>Nuts</td>
            <td>Ξηροί Καρποί</td>
        </tr>
        <tr>
            <td>3</td>
            <td>Crustaceans (Shellfish)</td>
            <td>Οστρακοειδή</td>
        </tr>
        <tr>
            <td>4</td>
            <td>Molluscs (Shellfish)</td>
            <td>Μαλάκια</td>
        </tr>
        <tr>
            <td>5</td>
            <td>Fish<br></td>
            <td>Ψάρι</td>
        </tr>
        <tr>
            <td>6</td>
            <td>Eggs</td>
            <td>Αυγά</td>
        </tr>
        <tr>
            <td>7</td>
            <td>Milk</td>
            <td>Γάλα</td>
        </tr>
        <tr>
            <td>8</td>
            <td>Cereals Containing Gluten</td>
            <td>Δημητριακά με Γλουτένη</td>
        </tr>
        <tr>
            <td>9</td>
            <td>Soya</td>
            <td>Σόγια</td>
        </tr>
        <tr>
            <td>10</td>
            <td>Sesame Seeds</td>
            <td>Σπόροι σησαμιού</td>
        </tr>
        <tr>
            <td>11</td>
            <td>Celery</td>
            <td>Σέλινο</td>
        </tr>
        <tr>
            <td>12</td>
            <td>Mustard<br></td>
            <td>Μουστάρδα</td>
        </tr>
        <tr>
            <td>13</td>
            <td>Lupin</td>
            <td>Λούπινο</td>
        </tr>
        <tr>
            <td>14</td>
            <td>Sulphur Dioxide</td>
            <td>Διοξείδιο του θείου</td>
        </tr>
        <tbody>
    </table>
    </div>
    """)
