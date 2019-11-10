from django import forms
from .models import Wordlist,Userword

class CreateWListForm(forms.ModelForm):
    class Meta:
        model = Wordlist
        fields = ["list_name"]
        widgets= {
            "list_name" : forms.TextInput(attrs={"class" : "form-control", "placeholder" : "Enter New List Name"}),
            }

class AddwordForm(forms.Form):
    word = forms.CharField(max_length=50,label="Word",widget=forms.TextInput(
        attrs={"class" : "form-control", "placeholder" : "Enter New Word"}
    ))

class FileForm(forms.Form):
    wordfile = forms.FileField()

#Aynı zamanda custom word eklerken kullanıldı
class EditwordForm(forms.ModelForm):
    class Meta:
        model = Userword
        exclude = ["wlist"]
        widgets= {
            "word" : forms.TextInput(attrs={"class" : "form-control", "placeholder" : "Enter New Word"}),
            "Type" : forms.TextInput(attrs={"class" : "form-control", "placeholder" : "For example : Enter v for Verbs (not required)"}),
            "gloss" : forms.Textarea(attrs={"class" : "form-control", "placeholder" : "This area required!\nYou can also describe it with your words"}),
            "similar_list" : forms.TextInput(attrs={"class" : "form-control", "placeholder" : "Enter Your Similar Words (not required)"}),
            "antonym_list" : forms.TextInput(attrs={"class" : "form-control", "placeholder" : "Enter Your Antonym Words (not required)"}),

            }

class SharedListAddForm(forms.Form):
    access_key = forms.CharField(max_length=12,min_length=5, widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Share Code"}))