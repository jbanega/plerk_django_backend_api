from django.urls import path

from .views import (CompanyList, CompanyDetail,
                    TransactionList, TransactionDetail,
                    HomePageView, ResponsePageView,
                    get_company_list, get_transaction_list,
                    see_summary_overview, get_summary_overview)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("company/", CompanyList.as_view(), name="company"),
    path("company/<str:pk>/", CompanyDetail.as_view(), name="detail_company"),
    path("transaction/", TransactionList.as_view(), name="transaction"),
    path("transaction/<uuid:pk>/", TransactionDetail.as_view(), name="detail_transaction"),
    path("response/", ResponsePageView.as_view(), name="response"),
    path("company_dataset/", get_company_list, name="company_dataset"),
    path("transaction_dataset/", get_transaction_list, name="transaction_dataset"),
    path("summary_overview/", see_summary_overview, name="summary_overview"),
    path("summary_overview/json", get_summary_overview, name="json_summary_overview"),
]