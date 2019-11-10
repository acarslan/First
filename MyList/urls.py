from django.urls import path
from . import views

urlpatterns = [
    path("", views.mylist,name="MyList"),
    path("createlist",views.createlist,name="CreateList"),
    path("list/<list_id>", views.listdetails, name="ListDetails"),
    path("list/<list_id>/<editword_id>", views.listdetails, name="WordEditDetails"),
    path("addfromfile/<list_id>",views.addfromfile, name="AddFromFile"),
    path("deletefromlist/<list_id>/<word_id>",views.deletefromlist, name="DeleteFromList"),
    path("editword/<word_id>",views.editword,name="EditWord"),
    path("<list_id>/addcustomword",views.addcustomword, name="AddCustomWord"),
    path("deletelist/<list_id>", views.deletelist, name="DeleteList"),
    path("editlist/<list_id>",views.editlist,name="EditList"),
    path("removesharedlist/<list_key>",views.removesharedlist),
    path("addsharedlist",views.addsharedlist,name="AddSharedList"),
    path("save/<list_id>",views.savelist,name="SaveList"),
    path("undo/<list_id>",views.undo,name="Undo"),
]
