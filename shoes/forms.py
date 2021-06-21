from django import forms
from shoes.models import Commentary

class Get_commentary(forms.ModelForm):
    class Meta:
        model = Commentary
        fields = ['shoes', 'user', 'text', 'value']
        widgets = {'shoes': forms.Select(attrs={'class': 'form-control'}),
                   'user': forms.Select(attrs={'class': 'form-control'}),
                 #  'parent': forms.Select(attrs={'class': 'form-control'}),
                   'text': forms.Textarea(attrs={'class': 'form-control'}),
                   'value': forms.TextInput(attrs={'class': 'form-control'})
                   }

    def add_error(self, field, error):
        if field is not None:
            print('Error on field {}: {}'.format(field, error))
        else:
            print('Error on form: {}'.format(error))  # non field error
        super().add_error(field, error)

# class Get_rating(forms.ModelForm):
#     class Meta:
#         model = Rating
#         fields = ['user_id', 'shoes', 'value']