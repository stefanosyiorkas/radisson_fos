from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Foods


class Registration(UserCreationForm):
    # username = forms.CharField(label='Username', required=True, help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",max_length="50", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'jsmith'}))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control form-control-sm rounded-0', 'placeholder': "Enter a username"})
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

    dish_image = forms.ImageField(help_text="""
    <button id="removeItemImage" type="button" class="btn btn-danger btn-sm mx-auto mt-2" onclick="removeImageAdmin()">Remove Image</button>
    <script>
    if (document.getElementsByClassName('field-dish_image')[0].innerText.includes('media/no-img-available.png')) {
        document.getElementById("removeItemImage").style.display = "none";
    }
    function getCookie(name) {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) return parts.pop().split(';').shift();
    }

    
    function removeImageAdmin() {
        var r = confirm("Remove image for this item?");
        if (r == true) {
            var item_id = window.location.pathname.split("/")[4];
            var csrftoken = getCookie('csrftoken');
            $.ajax({
                url: "/set_default_image",
                type: "POST",
                data: { id: item_id, csrfmiddlewaretoken: csrftoken },
        
                success: function(json) {
                    location.reload();
                },
                error: function(xhr, errmsg, err) {
                    console.log("Unable to remove image due to error: " + xhr.responseText);
                }
            });
        }
        
    }
    </script>
    """, required=False)
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
        <div class="mx-auto" style="width: 300px;">
        <table class="table">
        <thead>
        <tr>
            <th>#</th>
            <th>Allergen</th>
        </tr>
        </thead>
        <tbody>
        <tr>
            <td>1</td>
            <td>Peanuts</td>
        </tr>
        <tr>
            <td>2</td>
            <td>Nuts</td>
        </tr>
        <tr>
            <td>3</td>
            <td>Crustaceans (Shellfish)</td>
        </tr>
        <tr>
            <td>4</td>
            <td>Molluscs (Shellfish)</td>
        </tr>
        <tr>
            <td>5</td>
            <td>Fish<br></td>
        </tr>
        <tr>
            <td>6</td>
            <td>Eggs</td>
        </tr>
        <tr>
            <td>7</td>
            <td>Milk</td>
        </tr>
        <tr>
            <td>8</td>
            <td>Cereals Containing Gluten</td>
        </tr>
        <tr>
            <td>9</td>
            <td>Soya</td>
        </tr>
        <tr>
            <td>10</td>
            <td>Sesame Seeds</td>
        </tr>
        <tr>
            <td>11</td>
            <td>Celery</td>
        </tr>
        <tr>
            <td>12</td>
            <td>Mustard<br></td>
        </tr>
        <tr>
            <td>13</td>
            <td>Lupin</td>
        </tr>
        <tr>
            <td>14</td>
            <td>Sulphur Dioxide</td>
        </tr>
        <tbody>
    </table>
    </div>
    """)
