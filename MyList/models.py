from django.db import models

# Create your models here.
class Wordlist(models.Model):
    list_name = models.CharField(max_length= 50)
    owner = models.ForeignKey("auth.User",on_delete=models.CASCADE,verbose_name="User", null=True)
    access_key = models.CharField(max_length = 15)
    


    def __str__(self):
        return self.list_name

class Userword(models.Model):
    wlist = models.ForeignKey(Wordlist, on_delete=models.CASCADE)
    word = models.CharField(max_length= 50)
    Type = models.CharField(max_length = 4 , blank = True, null=True)
    gloss = models.CharField(max_length = 500)
    similar_list = models.CharField(max_length = 500, null=True, blank=True)
    antonym_list = models.CharField(max_length = 100, null=True, blank=True)
   

    def __str__(self):
        return "{} ({})".format(self.word,self.Type) 

class UserKeys(models.Model):
    user = models.ForeignKey("auth.User",on_delete=models.CASCADE,verbose_name="User")
    key = models.CharField(max_length = 15)

class WordListGenerate(models.Model):
    list_name = models.CharField(max_length= 50)
    change_list = models.ForeignKey(Wordlist,on_delete=models.CASCADE)

    def __str__(self):
        return self.list_name

class GenerateWord(models.Model):
    genlist = models.ForeignKey(WordListGenerate, on_delete=models.CASCADE)
    word = models.CharField(max_length= 50)
    Type = models.CharField(max_length = 4 , blank = True, null=True)
    gloss = models.CharField(max_length = 500)
    similar_list = models.CharField(max_length = 500, null=True, blank=True)
    antonym_list = models.CharField(max_length = 100, null=True, blank=True)
