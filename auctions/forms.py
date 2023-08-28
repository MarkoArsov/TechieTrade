from django import forms
from . import models


class ListingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ListingForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control login-input"

    class Meta:
        model = models.Listing
        exclude = ['datetime', 'user', 'watchListUsers', 'winner', 'losers', 'isOpen']
