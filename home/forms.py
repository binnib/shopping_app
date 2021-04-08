from django import forms
from .models import Product,Category,Customer

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','description','price','category','unit_measure','image']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'price': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.TextInput(attrs={'class':'form-control'}),
            'category': forms.Select(attrs={'class':'form-control'}),
            'unit_measure': forms.Select(attrs={'class':'form-control'}),
            'image': forms.FileInput(attrs={'class':'form-control'}),
        }
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name','description']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.TextInput(attrs={'class':'form-control'}),
        }
        
# class CustomerForm(forms.ModelForm):
#     class Meta:
#         model = Customer
#         # fields = ['phone_no', 'gender', 'date_of_birth']
#         fields = ['phone_no', 'gender']
#         CHOICES = [('F', 'Female'), ('M', 'Male')]
        
#         widgets = {
#             'phone_no': forms.TextInput(attrs={'class':'form-control'}),
#             'gender': forms.Select(attrs={'class':'form-control'},choices=CHOICES),
#             # 'date_of_birth': forms.DateInput(attrs={'class':'form-control'}),
#         }