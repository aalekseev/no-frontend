from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from notes.models import Note


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    fields = ["title", "text"]
    template_name = "notes/notes_detail.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    fields = ["text"]
    template_name = "notes/notes_detail.html"


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    success_url = reverse_lazy("notes:list")


class NoteListView(LoginRequiredMixin, ListView):
    model = Note

    paginate_by = 3
    template_name = "notes/notes_list.html"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(created_by=self.request.user)
