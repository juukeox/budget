import pandas as pd
from typing import List, Dict, Any

# import budget.xlsx from root
csv = pd.read_excel("src/budget.xlsx")


class Transaction:
    def __init__(self, name, amount, category, date, frequency):
        self.name = name
        self.amount = amount
        self.category = category
        self.date = date
        self.frequency = frequency

    def calc_monthly_cost(self):
        return (self.amount / self.frequency) * 30

    def calc_yearly_cost(self):
        return (self.amount / self.frequency) * 365

    def calc_weekly_cost(self):
        return (self.amount / self.frequency) * 7

    def calc_daily_cost(self):
        return self.amount / self.frequency


class Income(Transaction):
    def __init__(self, name, amount, category, date, frequency):
        print("Working on income")
        super().__init__(name, amount, category, date, frequency)


class Expense(Transaction):
    def __init__(self, name, amount, category, date, frequency):
        print("Working on expense")
        super().__init__(
            name, -abs(amount), category, date, frequency
        )  # Ensure amount is negative
        # Ensure calc_daily_cost is negative
        self.daily_cost = -abs(self.calc_daily_cost())
        self.weekly_cost = -abs(self.calc_weekly_cost())
        self.monthly_cost = -abs(self.calc_monthly_cost())
        self.yearly_cost = -abs(self.calc_yearly_cost())


def check_columns(csv) -> pd.DataFrame:
    """
    Checks if columns are of the correct type
    """
    # Check all rows in the first column are strings:
    for row in csv["name"]:
        if not isinstance(row, str):
            raise TypeError("Name must be a string")

    for row in csv["amount"]:
        if not isinstance(row, (float, int)):
            raise TypeError("Amount must be a float")

    # for row in csv['category']:
    #     if not isinstance(row, str):
    #         raise TypeError('Category must be a string')

    for row in csv["income/expense"]:
        if row not in ["income", "expense"]:
            raise ValueError(
                'Income/Expense must be either "income" or "expense"'
            )

    for row in csv["frequency"]:
        if not isinstance(row, int):
            raise ValueError(
                'Frequency must be either "daily", "weekly", "monthly", or "yearly".'
            )

    for row in csv["date"]:
        if not isinstance(row, int):
            raise TypeError("Date must be a month")

def create_report(csv):
    output_rows = []

    for _, row in csv.iterrows():
        # Create an Income or Expense object based on the "income/expense" column
        transaction = (
            Income(
                row["name"],
                row["amount"],
                row["category"],
                row["date"],
                row["frequency"],
            )
            if row["income/expense"] == "income"
            else Expense(
                row["name"],
                row["amount"],
                row["category"],
                row["date"],
                row["frequency"],
            )
        )

        # Create dictionary from object attributes
        output_row = {
            "name": transaction.name,
            "amount": transaction.amount,
            "category": transaction.category,
            "date": transaction.date,
            "frequency_days": transaction.frequency,
            "monthly_spend": transaction.calc_monthly_cost(),
            "yearly_spend": transaction.calc_yearly_cost(),
            "weekly_spend": transaction.calc_weekly_cost(),
            "daily_spend": transaction.calc_daily_cost(),
        }
        output_rows.append(output_row)

    output_df = pd.DataFrame(output_rows)

    # Save output_df to CSV
    output_df.to_csv("src/new_budget.csv", index=False)

    return output_df
    

def create_summary(dataframe):
    # Calculate net income and expenses
    summary = (
        dataframe.groupby("frequency_days")
        .agg(
            total_income=("amount", lambda x: x[x > 0].sum()),
            total_expense=("amount", lambda x: x[x < 0].sum()),
            total_monthly_spend=("monthly_spend", "sum"),
            total_yearly_spend=("yearly_spend", "sum"),
            total_weekly_spend=("weekly_spend", "sum"),
            total_daily_spend=("daily_spend", "sum"),
        )
        .reset_index()
    )

    summary["net_income"] = summary["total_income"] + summary["total_expense"]

    # Save dataframe to CSV
    # dataframe.to_csv("new_budget.csv", index=False)
    summary.to_csv("src/summary.csv", index=False)


def handler(csv):
    if not isinstance(csv, pd.DataFrame):
        raise TypeError("CSV must be a pandas dataframe")
    check_columns(csv)

    report = create_report(csv)

    create_summary(report)


if __name__ == "__main__":
    handler(csv)
