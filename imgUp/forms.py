from django import forms
from .models import Detection, Img
from datetime import datetime

class RegionForm(forms.ModelForm):
    class Meta:
        model = Img
        fields = ('County', 'City', 'altitude')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['City'].queryset = City.objects.none()

    if 'county' in self.data:
            try:
                county_id = int(self.data.get('county'))
                self.fields['city'].queryset = City.objects.filter(county_id=county_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.county.city_set.order_by('name')

class Feedbacks(forms.Form):
    det = forms.ModelChoiceField(queryset=Detection.objects.all(), label='pred_id')
    dtime = forms.DateTimeField(label='time', initial=datetime.now)
    feedback = forms.CharField(label='feedback', widget=forms.Textarea)