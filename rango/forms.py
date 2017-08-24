from django import forms
from rango.models import Category, Page


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name ")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # Additional information on the form
    class Meta:
        # Provide association between ModelForm and ModelForm and fields to include in form
        model = Category
        fields = ('name',)


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the title of the page ")
    url = forms.URLField(max_length=128, help_text="Please enter the the URL of the page ")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    # Additional information on the form
    class Meta:
        # Provide association between ModelForm and ModelForm and fields to include in form
        model = Page
        # Exclude the category field from the form
        exclude = ('category', )
        fields = ('title', 'url',)

# How to overide the clean method to correct user input

# def clean(self):
#     cleaned_data = self.cleaned_data
#     url = cleaned_data.get('url')
#     # If url is not empty and doesn't start with 'http://',
#     # then prepend 'http://'.
#     if url and not url.startswith('http://'):
#         url = 'http://' + url
#         cleaned_data['url'] = url
#         return cleaned_data
