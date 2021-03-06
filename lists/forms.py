'''
Created on Aug 20, 2015

@author: stefania
'''
from django import forms
from lists.models import Item
from django.core.exceptions import ValidationError

EMPTY_ITEM_ERROR = "You can't have an empty list item"
DUPLICATE_ITEM_ERROR = "You've already got this in your list"

# class ItemForm(forms.Form):
#     item_text = forms.CharField(
#             widget = forms.fields.TextInput(attrs={
#                  'placeholder': "Enter a to-do item",
#                  'class': 'form-control input-lg',
#                 })
#     )
    
class ItemForm(forms.models.ModelForm):
    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(
                attrs={
                       'placeholder': "Enter a to-do item",
                       'class': 'form-control input-lg',
                       })
        }
        error_messages = {
            'text': {'required': EMPTY_ITEM_ERROR}
        }
        
    def save (self, for_list):
        #The .instance attribute on a form represents the database object that is being modified or created. 
        self.instance.list = for_list
        return super().save()
    
class ExistingListItemForm (ItemForm):
    
    # add parameter for_list in the ExistingListItemForm init
    def __init__(self,for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = for_list

        
    def validate_unique(self):
        # That’s a bit of Django voodoo right there, 
        # but we basically take the validation error, 
        # adjust its error message, and then pass it back into the form.
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)
            
    def save(self):
        return forms.models.ModelForm.save(self)