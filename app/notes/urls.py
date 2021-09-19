from django.urls import path

from notes.views import NoteCreateView, NoteDeleteView, NoteListView, NoteUpdateView


app_name = "notes"
urlpatterns = [
    path("notes/add/", NoteCreateView.as_view(), name="add"),
    path("notes/<int:pk>/", NoteUpdateView.as_view(), name="update"),
    path("notes/<int:pk>/delete/", NoteDeleteView.as_view(), name="delete"),
    path("", NoteListView.as_view(), name="list"),
]
