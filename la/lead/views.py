import csv
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, DeleteView, UpdateView, CreateView, View,)

from .forms import AddCommentForm, AddFileForm, AddLeadForm
from .models import Lead

from client.models import Client, Comment as ClientComment
from team.models import Team

def leads_export(request):
    leads = Lead.objects.filter(created_by=request.user)

    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="clients.csv"'},
    )

    # Cambiar el delimitador a punto y coma
    writer = csv.writer(response, delimiter=';')

    # Escribir la fila de encabezado
    writer.writerow(['Lead', 'Description', 'Created at', 'Created by'])

    # Escribir datos de clientes
    for lead in leads:
        writer.writerow([lead.name, lead.description, lead.created_at, lead.created_by])

    return response

class LeadListView(LoginRequiredMixin, ListView):
    model = Lead

    def get_queryset(self):
        queryset = super(LeadListView, self).get_queryset()
        return queryset.filter(created_by=self.request.user, converted_to_client=False)

class LeadDetailView(LoginRequiredMixin, DetailView):
    model = Lead

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AddCommentForm()
        context['fileform'] = AddFileForm

        return context

    def get_queryset(self):
        queryset = super(LeadDetailView, self).get_queryset()
        team = self.request.user.userprofile.active_team

        return queryset.filter(team=team, pk=self.kwargs.get('pk'))

class LeadDeleteView(LoginRequiredMixin, DeleteView):
    model = Lead
    success_url = reverse_lazy("leads:list")


    def get_queryset(self):
        queryset = super(LeadDeleteView, self).get_queryset()
        team = self.request.user.userprofile.active_team
        messages.success(self.request, 'El prospecto ha sido eliminado exitosamente.')  # Mensaje que se mostrará

        return queryset.filter(team=team, pk=self.kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
        
        return self.post(request, *args, **kwargs)

class LeadUpdateView(LoginRequiredMixin, UpdateView):
    model = Lead
    form_class = AddLeadForm
    success_url = reverse_lazy("leads:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit lead"
        return context

    def form_valid(self, form):
        messages.success(self.request, 'El prospecto ha sido actualizado exitosamente.')
        return super().form_valid(form)

    def get_queryset(self):
        queryset = super(LeadUpdateView, self).get_queryset()
        team = self.request.user.userprofile.active_team
        return queryset.filter(team=team, pk=self.kwargs.get('pk'))
        
class LeadCreateView(LoginRequiredMixin, CreateView):
    model = Lead
    form_class = AddLeadForm  # Utiliza tu formulario personalizado aquí
    success_url = reverse_lazy("leads:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = self.request.user.userprofile.get_active_team()
        context["team"] = team
        context["title"] = "Agregar Cliente Potencial"
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.team = self.request.user.userprofile.get_active_team()
        messages.success(self.request, "Cliente potencial creado exitosamente!")
        return super().form_valid(form)
        

class AddFileView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')

        form = AddFileForm(request.POST, request.FILES)

        if form.is_valid():
            file = form.save(commit=False)
            file.team = self.request.user.userprofile.get_active_team()
            file.lead_id = pk
            file.created_by = request.user
            file.save()

        return redirect('leads:detail', pk=pk)
 
class AddCommentView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')

        form = AddCommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.team = self.request.user.userprofile.get_active_team()
            comment.created_by = request.user
            comment.lead_id = pk
            comment.save()

        return redirect('leads:detail', pk=pk)

class ConverToClientView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")

        team = self.request.user.userprofile.active_team

        lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
        team = self.request.user.userprofile.get_active_team()
        
        client = Client.objects.create(
            name=lead.name,
            email=lead.email,
            description=lead.description,
            created_by=request.user,
            team=team,
        )
        lead.converted_to_client = True
        lead.save()

        #convertir comentarios de clientes potenciales para convertir comentarios de clientes

        comments = lead.comments.all()

        for comment in comments:
            ClientComment.objects.create(
                client=client,
                content=comment.content,
                created_by=comment.created_by,
                team=team
            )

        messages.success(request, "El cliente potencial ha sido convertido en cliente.")

        return redirect("leads:list")
