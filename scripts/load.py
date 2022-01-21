import os
import pandas as pd
import pathlib

from APIapp.models import Company, Transaction


def run():

    def read_csv_dataset():
        # Reading csv dataset as pandas dataframe
        dir_name = pathlib.Path(__file__).parent.resolve()
        file_name = "test_database.csv"
        dataset = os.path.join(dir_name, "datasets", file_name)
        df = pd.read_csv(dataset)

        return df


    def fix_price_format(df):
        # Fixing price format.
        # All values have the same currency. Values with more than 3 digits are not
        # taking decimal into consideration and require conversion (division by 100,
        # that's mean two decimal position)
        revised_prices = []
        for price in df["price"]:
            if len(str(price)) >= 3:
                price = price/100
            revised_prices.append(price)
        df["price"] = revised_prices

        return df


    def pass_initial_values_to_database(df):
        # Cleaning postgres database before load dataset
        Company.objects.all().delete()
        Transaction.objects.all().delete()

        # Company objects
        # Unique company. All lowercaso to check for uniqueness 
        companies = pd.Series(df["company"].str.lower().unique())
        # Turning the company names to capitalize format
        companies = companies.str.title()
        # Creating and saving company in postgres database using django model
        for company in companies:
            company = Company.objects.create(name=company, status="ACTIVE")

        # Transaction objects
        for transaction in df.itertuples():
            # Setting company name format to match Company database
            company = str(transaction[1]).title()
            # Retrieve company instance to reference foreign key
            try:
                company_reference = Company.objects.get(name=company)
            except:
                print(f"{company} doesn't exist in database. Creating new record for it...")
                # Creating new company reference
                company_reference = Company.objects.create(name=company, status="ACTIVE")
            # Creating and saving transaction in postgres database using django model
            transaction = Transaction.objects.create(
                company_id=company_reference,
                price=transaction[2],
                date=transaction[3],
                status_transaction=transaction[4].upper(),
                status_approved=transaction[5],
            )


    # Loading dataset in database
    dataset_df = read_csv_dataset()
    corrected_dataset = fix_price_format(dataset_df)
    pass_initial_values_to_database(corrected_dataset)