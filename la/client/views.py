import csv

from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import AddClientForm, AddCommentForm, AddFileForm
from .models import Client

from team.models import Team

from .serializers import ClientSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.http import Http404

@login_required
def clients_export(request):
    clients = Client.objects.filter(created_by=request.user)

    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="clients.csv"'},
    )

    # Cambiar el delimitador a punto y coma
    writer = csv.writer(response, delimiter=';')

    # Escribir la fila de encabezado
    writer.writerow(['Client', 'Description', 'Created at', 'Created by'])

    # Escribir datos de clientes
    for client in clients:
        writer.writerow([client.name, client.description, client.created_at, client.created_by])

    return response

class ClientList(LoginRequiredMixin, APIView):
    def get(self, request):
        if request.method == 'GET':
            team = request.user.userprofile.active_team
            clients = team.clients.all()
            serializer = ClientSerializer(clients, many=True)
            return Response(serializer.data)

    def post(self, request):
        if request.method == 'POST':
            serializer = ClientSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Redireccionar a otra página
        return redirect('otra_pagina')

@login_required
def clients_list(request):
    team = request.user.userprofile.active_team
    clients = team.clients.all()

    return render(request, "client/clients_list.html", {"clients": clients})    

@login_required
def clients_add_file(request, pk):
    if request.method == 'POST':
        form = AddFileForm(request.POST, request.FILES)

        if form.is_valid():
            file = form.save(commit=False)
            file.team = request.user.userprofile.active_team
            file.client_id = pk
            file.created_by = request.user
            file.save()
        
            return redirect('clients:detail', pk=pk)
    return redirect('clients:detail', pk=pk)    

class Client_DetApi(LoginRequiredMixin, APIView):
    def get_object(self, pk):
        team = self.request.user.userprofile.active_team
        return get_object_or_404(Client, created_by=self.request.user, pk=pk)

    def get(self, request, pk):
        client = self.get_object(pk)
        serializer = ClientSerializer(client)
        return Response(serializer.data)

    def put(self, request, pk):
        client = self.get_object(pk)
        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        client = self.get_object(pk)
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, pk):
        client = self.get_object(pk)
        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Devuelve una respuesta JSON en lugar de redirigir o renderizar plantillas
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required
def clients_detail(request, pk):
    team = request.user.userprofile.active_team
    client = get_object_or_404(Client, created_by=request.user, pk=pk)

    if request.method == 'POST':
        form = AddCommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.team = request.user.userprofile.get_active_team()
            comment.created_by = request.user
            comment.client = client
            comment.save()

            return redirect('clients:detail', pk=pk)
    
    else:
        form = AddCommentForm()

    return render(request, "client/clients_detail.html", {
        "client": client, 
        "form": form, 
        "fileform" : AddFileForm(),
    })

@login_required
def clients_add(request):
    team = request.user.userprofile.get_active_team()

    if request.method == "POST":
        form = AddClientForm(request.POST)

        if form.is_valid():            
            client = form.save(commit=False)
            client.created_by = request.user
            client.team = team
            client.save()

            messages.success(request, "El cliente fue creado.")

            return redirect("clients:list")
    else:
        form = AddClientForm()

    return render(request, "client/clients_add.html", {"form": form, "team": team})


@login_required
def clients_delete(request, pk):
    team = request.user.userprofile.active_team
    client = get_object_or_404(Client, created_by=request.user, pk=pk)
    client.delete()

    messages.success(request, "El cliente fue eliminado")

    return redirect("clients:list")


@login_required
def clients_edit(request, pk):
    team = request.user.userprofile.active_team
    client = get_object_or_404(Client, created_by=request.user, pk=pk)

    if request.method == "POST":
        form = AddClientForm(request.POST, instance=client)

        if form.is_valid():
            form.save()

            messages.success(request, "Los cambios fueron guardados.")

            return redirect("clients:list")
    else:
        form = AddClientForm(instance=client)

    return render(request, "client/clients_edit.html", {"form": form})
