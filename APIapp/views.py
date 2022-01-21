from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import generics

from .models import Company, Transaction

from .serializers import CompanySerializer, TransactionSerializer


class ListCompany(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class DetailCompany(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class ListTransaction(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class DetailTransaction(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class HomePageView(TemplateView):
    template_name = "index.html"