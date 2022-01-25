from django.urls import path

from .views import (CompanyList, CompanyDetail,
                    TransactionList, TransactionDetail,
                    HomePageView, ResponsePageView,
                    get_company_list, get_transaction_list,
                    see_summary_overview, get_summary_overview,
                    see_top_10_company_with_more_transaction,
                    get_top_10_company_with_more_transaction,
                    see_company_transaction_detail,
                    get_company_transaction_detail)

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
    path("summary_overview/json/", get_summary_overview, name="json_summary_overview"),
    path(
        "top_10_transactions/", see_top_10_company_with_more_transaction, name="top_10_transactions"
        ),
    path(
        "top_10_transactions/json/", get_top_10_company_with_more_transaction, name="json_top_10_transactions"
        ),
    path("company_detail/<str:company_id>/", see_company_transaction_detail, name="company_transactions"),
    path("company_detail/<str:company_id>/json/", get_company_transaction_detail, name="json_company_transactions"),
]