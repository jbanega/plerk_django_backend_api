from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from rest_framework import generics, serializers, status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from .models import Company, Transaction

from .serializers import CompanySerializer, TransactionSerializer

from .utils import generate_summary

import requests
import json


# Views and serializers for RESTFul 
class CompanyList(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class CompanyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class TransactionList(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class HomePageView(TemplateView):
    template_name = "index.html"


class ResponsePageView(TemplateView):
    template_name = "response.html"


# Views functions to render results
def get_company_list(request):
    if request.method == "GET":
        company = Company.objects.all()
        company_serializer = CompanySerializer(company, many=True)
        return JsonResponse(company_serializer.data, safe=False)


def get_company_detail(request, pk):
    try:
        company = Company.objects.get(pk=pk)
    except Company.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        company_serializer = CompanySerializer(company)
        return JsonResponse(company_serializer.data, safe=False)


def get_transaction_list(request):
    if request.method == "GET":
        transaction = Transaction.objects.all()
        transaction_serializer = TransactionSerializer(transaction, many=True)
        return JsonResponse(transaction_serializer.data, safe=False)


def see_summary_overview(request):
    if request.method == "GET":
        transaction = Transaction.objects.all()
        summary = generate_summary(transaction)
        context_string = json.dumps(summary) 
        context = json.loads(context_string)

        return render(
            request,
            "response.html",
            context={
                "title": "General Summary",
                "company_highest_sales": context["company_with_highest_sales"],
                "company_lowest_sales": context["company_with_lowest_sales"],
                "total_price_approved": context["total_price_approved_transaction"],
                "total_price_not_approved": context["total_price_not_approved_transaction"],
                "company_highest_rejected_sales": context["company_with_highest_rejected_sales"],
            }
        )


def get_summary_overview(request):
    if request.method == "GET":
        transaction = Transaction.objects.all()
        summary = generate_summary(transaction)
        context = json.loads(json.dumps(summary))

        return JsonResponse(context, safe=False)
