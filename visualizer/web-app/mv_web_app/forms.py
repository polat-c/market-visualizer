from django import forms

class DateInput(forms.DateInput):

    input_type = 'date'

class TickerForm(forms.Form):

    ticker = forms.CharField(max_length=20)
    name = forms.CharField(max_length=100)

    start_t = forms.DateTimeField(widget=DateInput, required=False)
    end_t = forms.DateTimeField(widget=DateInput, required=False)

    interval = forms.CharField(max_length=10, required=False)

    def process(self):
        cleaned = self.cleaned_data