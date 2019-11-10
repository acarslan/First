from django.shortcuts import render
from random import randint
from MyList.models import Userword,UserKeys, Wordlist, WordListGenerate,GenerateWord

# Create your views here.

def index(request):
    if request.user.is_authenticated:    
        ownlist = Wordlist.objects.filter(owner__exact=request.user)
        listkeys = UserKeys.objects.filter(user__exact=request.user)
        
        selectlist = list()
        for i in ownlist:
            selectlist.append(i)
        for i in listkeys:
            accessing = i.key
            pk = accessing.split("-")[1]
            slist = Wordlist.objects.get(pk=int(pk))
            if accessing == slist.access_key:
                selectlist.append(slist)
        

    else:
        #Kendi kullanıcı girişi olmadanki listemizi göndericez şimdilik None yayınlamadan önce liste oluştur
        selectlist = None


    selected=None
    word = None
    selectedname = None

    
    if request.POST:
        list_id = request.POST.get("selectedlist")
        if list_id:
            selected = Wordlist.objects.get(pk=list_id)
            request.session["selectedlist"]=selected.id
            request.session["selectedname"]=selected.list_name
        selected = request.session["selectedlist"]
        selectedname = request.session["selectedname"]
        gen = request.POST.get("wlist")
        if gen and gen.isdigit():
            wlist = Wordlist.objects.get(pk=gen)
            genlist = WordListGenerate.objects.get(change_list=wlist)
            allwords = GenerateWord.objects.filter(genlist__exact=genlist)
            if len(allwords):
                randno = randint(0, len(allwords)-1)
                randword = allwords[randno]
                word = {
                    "word":randword.word,
                    "type":randword.Type,
                    "gloss":randword.gloss,
                }

                if randword.similar_list:
                    similars = randword.similar_list.strip()
                    similars = similars.split(",")
                    for i in similars:
                        i = i.strip()
                        i = i.replace("_"," ")
                    word["similars"]=similars
                if randword.antonym_list:
                    antonyms = randword.antonym_list.strip()
                    antonyms = antonyms.split(",")
                    for i in antonyms:
                        i = i.strip()
                        i = i.replace("_"," ")
                    word["antonyms"]=antonyms

    context={
        "selectlist":selectlist,
        "selected":selected,
        "word":word,
        "selectedname":selectedname,

    }
    return render(request,"index.html",context)


def settings(request):
    pass

def notfound(request):
    return render(request,"404.html")