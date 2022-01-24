import string
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

    # Generating context to pass to webpage
    summary = {
        "company_with_highest_sales": company_with_highest_sales.iloc[0]["company_id"],
        "company_with_lowest_sales": company_with_lowest_sales.iloc[0]["company_id"],
        "total_price_approved_transaction": str(total_price_approved_transaction.iloc[0]["price"]),
        "total_price_not_approved_transaction": str(total_price_not_approved_transaction.iloc[0]["price"]),
        "company_with_highest_rejected_sales": company_with_highest_rejected_sales.iloc[0]["company_id"],
        "max_number_of_rejected_sales": str(company_with_highest_rejected_sales.iloc[0]["count"]),
    }

    return summary