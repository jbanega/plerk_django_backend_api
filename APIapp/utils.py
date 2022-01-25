from datetime import date
import string
import pandas as pd
from random import choices
from django_pandas.io import read_frame


def generate_random_company_id():
    characters = string.digits + string.ascii_letters
    id = "".join(choices(characters, k=8))

    return id


def generate_summary(transaction):
    # Reading all transaction objects as dataframe
    df = read_frame(transaction)

    # Grouping by company name and final charge done
    df_group_by_company = df.groupby(
        ["company_id", "final_charge_done"]).price.sum().reset_index()
    
    # Filtering by company with only approved transactions
    approved_transactions_by_company = df_group_by_company[
        df_group_by_company["final_charge_done"] == True]

    # BASE SERVICE
    # Company with highest and lowest sales
    company_with_highest_sales = approved_transactions_by_company[
        (approved_transactions_by_company["price"].max() == approved_transactions_by_company["price"])]

    company_with_lowest_sales = approved_transactions_by_company[
        (approved_transactions_by_company["price"].min() == approved_transactions_by_company["price"])]
    
    # Total price of approved transactions
    df_group_by_approved_transaction = df_group_by_company.groupby(
        ["final_charge_done"]).price.sum().reset_index()
    
    total_price_approved_transaction = df_group_by_approved_transaction[
        df_group_by_approved_transaction["final_charge_done"] == True]

    total_price_not_approved_transaction = df_group_by_approved_transaction[
        df_group_by_approved_transaction["final_charge_done"] == False]

    # Company with highest rejected sales
    number_approved_transaction_by_company = df.groupby(
        ["company_id", "final_charge_done"]).size().to_frame("count").reset_index()
    
    rejected_sales_by_company = number_approved_transaction_by_company[
        number_approved_transaction_by_company["final_charge_done"] == False]

    company_with_highest_rejected_sales = rejected_sales_by_company[
        rejected_sales_by_company["count"].max() == rejected_sales_by_company["count"]]

    # PROPOSAL SERVICE
    top_10_companies_with_the_most_transaction = number_approved_transaction_by_company[
        number_approved_transaction_by_company["final_charge_done"] == True].sort_values(
        by="count", ascending=False)[["company_id","count"]].set_index("company_id").head(10)
    
    # Generating context summary to pass to webpage
    general_summary = {
        # Summary base service
        "company_with_highest_sales": company_with_highest_sales.iloc[0]["company_id"],
        "company_with_lowest_sales": company_with_lowest_sales.iloc[0]["company_id"],
        "total_price_approved_transaction": str(total_price_approved_transaction.iloc[0]["price"]),
        "total_price_not_approved_transaction": str(total_price_not_approved_transaction.iloc[0]["price"]),
        "company_with_highest_rejected_sales": company_with_highest_rejected_sales.iloc[0]["company_id"]
        }

    top_10_company_summary = {
        # Proposal service
        "top_10_companies_with_the_most_transaction": top_10_companies_with_the_most_transaction.to_dict(),
    }

    return general_summary, top_10_company_summary


def generate_company_summary(company_transactions):
    # Reading all transaction objects of the selected company
    df = read_frame(company_transactions)

    # Grouping dataset by company name and final charge done
    df_company = df.groupby(
        ["company_id", "final_charge_done"]).size().to_frame("count").reset_index()

    # Company name
    company_name = df_company["company_id"].iloc[0]

    # Number of approved and rejected transactions of the company
    number_approved_transactions = df_company[
        df_company["final_charge_done"] == True]["count"]
    number_rejected_transactions = df_company[
        df_company["final_charge_done"] == False]["count"]

    # Checking non empty value for number of approved transactions:
    if number_approved_transactions.size == 0:
        number_approved_transactions = 0
    else:
        number_approved_transactions = number_approved_transactions.iloc[0]

    if number_rejected_transactions.size == 0:
        number_rejected_transactions = 0
    else:
        number_rejected_transactions = number_rejected_transactions.iloc[0]

    # Dataframe Group by date
    df_groupby_date = df[["date", "status_transaction"]].groupby(
        ["date"]).size().to_frame("count").reset_index()

    # Date of max number of transactions
    date_max_n_transaction = df_groupby_date[
        df_groupby_date["count"].max() == df_groupby_date["count"]].iloc[0]["date"]

    # Generating context summary to pass to webpage
    company_summary = {
        "company_name": company_name,
        "number_approved_transactions": str(number_approved_transactions), 
        "number_rejected_transactions": str(number_rejected_transactions),
        "date_max_n_transactions": str(date_max_n_transaction), 
    }

    return company_summary