from django.shortcuts import render

# Create your views here.
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Entry
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin


#redirect to admin login when user is not loggen in
class LockedView(LoginRequiredMixin):
    login_url = "admin:login"

class EntryListView(LockedView,ListView):
    model = Entry
    queryset = Entry.objects.all().order_by("-date_created")

class EntryDetailView(LockedView,DetailView):
    model = Entry

#classes to add on task list
class EntryCreateView(LockedView,SuccessMessageMixin, CreateView):
    model = Entry
    fields = ["title", "content"]
    success_url = reverse_lazy("entry-list")
    success_message = "New entry sucessifully created!"

class EntryUpdateView(LockedView,SuccessMessageMixin,UpdateView):
    model = Entry
    fields = ["title", "content"]
    success_message = "Your entry was updated!"

    

    def get_success_url(self):
        return reverse_lazy(
            "entry-detail",
            kwargs={"pk": self.entry.id}
        )

class EntryDeleteView(LockedView,DeleteView):
    model = Entry
    success_url = reverse_lazy("entry-list")
    success_message = "Your entry was deleted!"

def delete(self, request, *args, **kwargs):
    messages.success(self.request, self.success_message)
    return super().delete(request, *args, **kwargs)