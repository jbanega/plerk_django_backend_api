from django.urls import path

from .views import (ListCompany, DetailCompany,
                    ListTransaction, DetailTransaction, HomePageView)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("company/", ListCompany.as_view(), name="company"),
    path("company/<uuid:pk>/", DetailCompany.as_view(), name="detail_company"),
    path("transaction/", ListTransaction.as_view(), name="transaction"),
    path("transaction/<uuid:pk>/", DetailTransaction.as_view(), name="detail_transaction"),
]