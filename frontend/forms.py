from django import forms

class ProductForm(forms.Form):
    name = forms.CharField(max_length=200, label="Product Name")
    description = forms.CharField(widget=forms.Textarea, label="Description")
    price = forms.DecimalField(decimal_places=2, max_digits=10, label="Price",min_value=0.0)
    category = forms.ChoiceField(choices=[], label="Category")
    