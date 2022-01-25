from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from rest_framework import generics, status

from .models import Company, Transaction

from .serializers import CompanySerializer, TransactionSerializer

from .utils import generate_summary, generate_company_summary

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company_id"] = "#"
        return context


class ResponsePageView(TemplateView):
    template_name = "response.html"


# View functions to render results
def get_company_list(request):
    if request.method == "GET":
        company = Company.objects.all()
        company_serializer = CompanySerializer(company, many=True)
        return JsonResponse(company_serializer.data, safe=False)


def get_transaction_list(request):
    if request.method == "GET":
        transaction = Transaction.objects.all()
        transaction_serializer = TransactionSerializer(transaction, many=True)
        return JsonResponse(transaction_serializer.data, safe=False)


def see_summary_overview(request):
    if request.method == "GET":
        transaction = Transaction.objects.all()
        summary, _ = generate_summary(transaction) 
        context = json.loads(json.dumps(summary))

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
        summary, _ = generate_summary(transaction)
        context = json.loads(json.dumps(summary))

        return JsonResponse(context, safe=False)


def see_top_10_company_with_more_transaction(request):
    if request.method == "GET":
        transaction = Transaction.objects.all()
        _, summary = generate_summary(transaction)
        context = json.loads(json.dumps(summary))

        return render(
            request,
            "response.html",
            context={
                "title": "Top 10 Companies with The Mayor Transactions",
                "top_10_companies_transaction": context["top_10_companies_with_the_most_transaction"],
            }
        )


def get_top_10_company_with_more_transaction(request):
    if request.method == "GET":
        transaction = Transaction.objects.all()
        _, summary = generate_summary(transaction)
        context = json.loads(json.dumps(summary))

        return JsonResponse(
            context["top_10_companies_with_the_most_transaction"]["count"],
            safe=False)


def see_company_transaction_detail(request, company_id):
    if request.method == "POST":
        company_id = request.POST.get("company_id")
        if company_id == "":
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                company_transactions = Transaction.objects.filter(company_id=company_id)
            except Transaction.DoesNotExist:
                return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        
        if not company_transactions.exists():
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        
        company_summary = generate_company_summary(company_transactions)
        context = json.loads(json.dumps(company_summary))

        return render(
            request,
            "response.html",
            context={
                "title": "Company Transactions",
                "company_name": context["company_name"],
                "company_id": company_id,
                "number_approved_transactions": context["number_approved_transactions"],
                "number_rejected_transactions": context["number_rejected_transactions"],
                "date_max_n_transactions": context["date_max_n_transactions"],
            }
        )


def get_company_transaction_detail(request, company_id):
    if request.method == "GET":
        company_transactions = Transaction.objects.filter(company_id=company_id)
        company_summary = generate_company_summary(company_transactions)
        context = json.loads(json.dumps(company_summary))

        return JsonResponse(context, safe=False)