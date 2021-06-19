from django import forms
from shoes.models import Commentary, Rating

class Get_commentary(forms.ModelForm):
    class Meta:
        model = Commentary
        fields = ['shoes','user_id', 'parent', 'title', 'text']


class Get_rating(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['user_id', 'shoes', 'value']