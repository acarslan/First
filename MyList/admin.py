from django.contrib import admin
from .models import Wordlist, Userword, UserKeys, GenerateWord, WordListGenerate
# Register your models here.

admin.site.register(Wordlist)
admin.site.register(Userword)
admin.site.register(UserKeys)
admin.site.register(GenerateWord)
admin.site.register(WordListGenerate)