


def categorise_transaction(description):

    description = str(description).upper().strip()

    if any(shop in description for shop in ["ALDI", "TESCO"]):
        return "Groceries"

    elif any(shop in description for shop in ["MCDONALDS", "KFC"]):
        return "Food"

    elif "TOYOTA FIN SERV" in description:
        return "Car Finance"

    elif "DVLA" in description:
        return "Vehicle Tax"

    elif any(shop in description for shop in [
        "SHELL", "RONTEC"
    ]):
        return "Petrol"

    elif "TFL TRAVEL CH" in description:
        return "Public Transport"

    elif "NCP LIMITED" in description:
        return "Parking"

    elif "GLL BETTER" in description:
        return "Leisure / Gym"

    elif "B&M" in description:
        return "Shopping"

    elif "AQUA" in description or "PLATINUM M/C" in description:
        return "Credit Card Payment"

    elif "SKY TV" in description:
        return "TV / Entertainment"

    elif "TV LICENCE" in description:
        return "TV Licence"

    elif "O2" == description:
        return "Phone Bill"

    elif "VIRGIN MEDIA" in description:
        return "Broadband / TV"

    elif "APPLE.COM/BILL" in description:
        return "Digital Services"

    elif "OPENAI" in description:
        return "Software Subscription"

    elif "NON-GBP" in description or "DAILY OD INT" in description:
        return "Bank Charges"

    elif "HELP TO SAVE" in description:
        return "Savings Transfer"

    elif "HANIFA G MUHAMMAD" in description:
        return "Personal Transfer"

    elif "UBER" in description:
        return "Income"

    elif "PAYPAL" in description or "HALIFAX" in description:
        return "Review"

    else:
        return "Other"


def add_categories(df):

    df = df.copy()

    df["Category"] = df["Description"].apply(
        categorise_transaction
    )

    return df


def add_categories(df):

    df = df.copy()

    df["Category"] = df["Description"].apply(
        categorise_transaction
    )

    return df