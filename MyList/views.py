from django.shortcuts import render,redirect, get_object_or_404
from .forms import CreateWListForm, AddwordForm, FileForm, EditwordForm, SharedListAddForm
from .models import Wordlist, Userword, UserKeys, GenerateWord, WordListGenerate
import sqlite3
from .methods import wordyfile
from django.contrib import messages
from django.core.files import File
from random import choice
from string import ascii_letters
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url = "user:login")
def mylist(request):
    wordlist = Wordlist.objects.filter(owner = request.user)
    sharedlist = list()
    createlistform = CreateWListForm(None)
    sharedlistaddform = SharedListAddForm(None)

    keys = UserKeys.objects.filter(user = request.user)

    for i in keys:
        accessing = i.key
        pk = accessing.split("-")[1]
        slist = Wordlist.objects.get(pk=int(pk))
        print(accessing,slist.access_key)
        if accessing == slist.access_key:
            sharedlist.append(slist)
            
    context = {
        "wordlist" : wordlist,
        "sharedlist":sharedlist,
        "createlistform":createlistform,
        "sharedlistaddform":sharedlistaddform,
    }
    return render(request,"mylist.html",context)

@login_required(login_url = "user:login")
@require_POST
def createlist(request):
    form = CreateWListForm(request.POST)
    
    if form.is_valid():
        name = form.cleaned_data["list_name"]
        new_list = Wordlist(list_name = name, owner=request.user )
        new_list.save()
        new_savelist = WordListGenerate(list_name = name,  change_list=new_list)
        new_savelist.save()
        acces_value = "".join(choice(ascii_letters) for i in range(3))
        new_list.access_key = acces_value + "-" + str(new_list.pk)
        new_list.save()
    return redirect("MyList")

   

@login_required(login_url = "user:login")
def listdetails(request, list_id, editword_id = None):
    wordlist = Wordlist.objects.get(pk=list_id)

    if wordlist.owner != request.user:
        keys = UserKeys.objects.filter(user__exact=request.user)
        kick = True
        for i in keys:
            if i.key == wordlist.access_key:
                kick = False
        if kick:
            
            return redirect("MyList")

    
    addform = AddwordForm(request.POST or None)
    addfile = FileForm(None)
    cwform = EditwordForm(None)
    con = sqlite3.connect("WORDS.db")
    cursor = con.cursor()
    listwords = Userword.objects.filter(wlist__exact = wordlist)
    show = "none"
    showedit = None
    editwordform = EditwordForm(None)
    if editword_id:
        edit = get_object_or_404(Userword, id=editword_id)
        if edit.wlist.owner == request.user:
            editwordform = EditwordForm(None,instance = edit)
            showedit = editword_id
        else:
            redirect("MyList")



    if addform.is_valid():
        if wordlist.owner == request.user:
            word = addform.cleaned_data["word"]
            word = word.replace(" ","_")    
            cursor.execute("select Word,Type,Gloss,Similars,Antonyms from Words where Word=?",(word,))
            words = cursor.fetchall()
            if words:
                for i in words:
                    new_word = Userword( wlist= wordlist, word=i[0], Type=i[1], gloss=i[2], similar_list = i[3], antonym_list = i[4] )
                    new_word.save()

                return redirect("/mylist/list/"+list_id)      
            else:    
                cwform = EditwordForm(initial={"word" : word,})
                show = "block"
        else:
            
            return redirect("/mylist/list/"+list_id)  
    con.close()
    context = {
        
        "wordlist":wordlist,
        "addform" : addform,
        "listwords":listwords[::-1],
        "addfile":addfile,
        "cwform":cwform,
        "show":show,
        "showedit":showedit,
        "editwordform":editwordform,
            
    }
    return render(request,"listdetails.html",context)

@login_required(login_url = "user:login")   
@require_POST
def addfromfile(request, list_id):
    wordlist = Wordlist.objects.get(pk=list_id)
    if wordlist.owner == request.user:
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            uploadedfile = request.FILES["wordfile"]
            #geçici dosyanın pathi kod kalabalığını engellemek için methods.py içinde fonksiyon olarak tanımlandı ve oraya eklendi
            words = wordyfile(uploadedfile.temporary_file_path())
            con = sqlite3.connect("WORDS.db")
            cursor = con.cursor()

            for word in words:
                word = word.replace(" ","_")    
                cursor.execute("select Word,Type,Gloss,Similars,Antonyms from Words where Word=?",(word,))
                addedword = cursor.fetchall()
                
                for i in addedword:
                    new_word = Userword( wlist= wordlist, word=i[0], Type=i[1], gloss=i[2], similar_list = i[3], antonym_list = i[4] )
                    new_word.save()
        return redirect("/mylist/list/"+list_id)
    else:
        
        return redirect("/mylist/list/"+list_id)

@login_required(login_url = "user:login")
def deletefromlist(request, list_id, word_id):

    listowner = Wordlist.objects.get(pk=list_id).owner 
    if listowner == request.user:
        Userword.objects.filter(id__exact=word_id).delete()
    else:
        
        return redirect("MyList")

    return redirect("/mylist/list/"+list_id)

@require_POST
@login_required(login_url = "user:login")
def editword(request, word_id):
    word = get_object_or_404(Userword, id=word_id)
    if word.wlist.owner == request.user:
        form = EditwordForm(request.POST,instance = word)
        if form.is_valid():
            form.save()
            
    return redirect("/mylist/list/"+str(word.wlist.id))
        

@login_required(login_url = "user:login")
@require_POST   
def addcustomword(request, list_id):
    wlist = Wordlist.objects.get(pk=list_id)
    if wlist.owner == request.user:
        form = EditwordForm(request.POST)
        if form.is_valid:
            cw = form.save(commit=False)
            cw.wlist = wlist
            cw.save()
            
        return redirect("/mylist/list/"+list_id)
    else:
        
        return redirect("MyList")

@login_required(login_url = "user:login")
def deletelist(request,list_id):
    deletinglist = Wordlist.objects.get(pk=list_id)
    if deletinglist.owner == request.user:
        delkey = deletinglist.access_key
        deleting_key=UserKeys.objects.filter(key__exact = delkey)
        for i in deleting_key:
            i.delete()
        deletinglist.delete()
        
    return redirect("MyList")

@login_required(login_url = "user:login")
def editlist(request,list_id):
    elist = get_object_or_404(Wordlist, id=list_id)
    if elist.owner == request.user:
        form = CreateWListForm(request.POST or None, instance=elist)
        if form.is_valid():
            form.save()
            return redirect("MyList")
        context = {
            "form":form,
        }
        return render(request, "editlist.html",context)
    else:
        
        return redirect("MyList")

@login_required(login_url = "user:login")
def removesharedlist(request,list_key):
    sharedlist = UserKeys.objects.filter(user__exact=request.user)
    for i in sharedlist:
        if i.key == list_key:
            i.delete()
            break
    return redirect("MyList")

@login_required(login_url = "user:login")
@require_POST
def addsharedlist(request):
    form = SharedListAddForm(request.POST)
    if form.is_valid():
        access_key = form.cleaned_data["access_key"]
        try:
            Wordlist.objects.get(access_key=access_key)
            new_key = UserKeys(user=request.user, key=access_key)
            new_key.save()
            return redirect ("MyList")
        except:
            return redirect ("MyList")
    return redirect ("MyList")

@login_required(login_url = "user:login")
def savelist(request,list_id):
    olist = get_object_or_404(Wordlist, id=list_id)
    if olist.owner == request.user:
        words = Userword.objects.filter(wlist__exact = olist)
        genlist = get_object_or_404(WordListGenerate, change_list=olist)
        gwords = GenerateWord.objects.filter(genlist__exact = genlist)
        for i in gwords:
            i.delete()
        for i in words:
            new_word = GenerateWord(genlist=genlist, word= i.word,Type=i.Type ,gloss=i.gloss, similar_list=i.similar_list,antonym_list=i.antonym_list)
            new_word.save()
        return redirect("MyList")
    else:
        return redirect("Index")

@login_required(login_url = "user:login")
def undo(request,list_id):
    olist = get_object_or_404(Wordlist,id=list_id)
    if olist.owner == request.user:
        words = Userword.objects.filter(wlist__exact = olist)
        genlist = get_object_or_404(WordListGenerate, change_list=olist)
        for i in words:
            i.delete()
        gwords = GenerateWord.objects.filter(genlist__exact = genlist)
        for i in gwords:
            new_word = Userword( wlist= olist, word=i.word, Type=i.Type, gloss=i.gloss, similar_list = i.similar_list, antonym_list = i.antonym_list )
            new_word.save()
        return redirect("/mylist/list/"+list_id)
    else:
        return redirect("Index")