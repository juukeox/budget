def budget(daily_increase=1, years_forward=5):
    total_increase = 0  # Total increase over all the years
    yearly_increase = 0  # Increase in a single year

    for year in range(1, years_forward + 1):
        print(f"\n--- Year {year} ---")
        for month in range(
            1, 13
        ):  # Iterate from 1 to 12 (representing months)
            monthly_increase = (
                daily_increase  # The increase for the current month
            )
            months_remaining_in_year = (
                13 - month
            )  # Number of months this increase will be active in the current year

            # Calculate this month's contribution for the current year
            current_year_contribution = months_remaining_in_year * (
                monthly_increase * 30
            )
            yearly_increase += current_year_contribution

            # Log the contribution for the current year
            print(f"Month {month}:")
            print(f"  - Increase for this month: £{monthly_increase}")
            print(
                f"  - Current year contribution (for {months_remaining_in_year} months): £{current_year_contribution}"
            )

            # Calculate the contribution of this month's increase for future years
            future_year_contribution = 0
            for future_year in range(1, years_forward - year + 1):
                future_year_contribution += 12 * (
                    monthly_increase * 30
                )  # Each month's increase lasts 12 months in future years

            yearly_increase += future_year_contribution

            # Log the contribution for future years
            if future_year_contribution > 0:
                print(
                    f"  - Future year contribution: £{future_year_contribution}"
                )

            print(f"  - Yearly increase so far: £{yearly_increase}")

        total_increase += (
            yearly_increase  # Add the yearly increase to the total increase
        )
        print(f"Total increase by the end of Year {year}: £{total_increase}")
        yearly_increase = 0  # Reset yearly increase for the next year
        daily_increase += 1  # Increase daily increment for the next year

    return f"Total increase over {years_forward} years: £{total_increase}"


# Call the function
print(budget(daily_increase=1, years_forward=5))


def budget(daily_increase=1):
    yearly_increase = 0

    for month in range(1, 13):  # Iterate from 1 to 12 (representing months)
        monthly_increase = daily_increase  # The increase for the current month
        yearly_increase += (13 - month) * (
            monthly_increase * 30
        )  # Add this to the yearly total

        print(
            f"Month {month}: Increased by £{monthly_increase}, Yearly increase so far: £{yearly_increase}"
        )

    return f"Total yearly increase: £{yearly_increase}"
