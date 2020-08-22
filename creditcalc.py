import math
import argparse


def calc_periods(a, i, p):
    periods = math.log(a / (a - i * p), 1 + i)
    return math.ceil(periods)


def calc_annuity(p, i, n):
    a = p * (i * math.pow(1 + i, n)) / (math.pow(1 + i, n) - 1)
    return a


def calc_principal(a, i, n):
    p = a / ((i * math.pow(1 + i, n)) / (math.pow(1 + i, n) - 1))
    return p


def diff_payment(p, n, i, m):
    d = p / n + i * (p - (p*(m-1))/n)
    return d


def round_print(number):
    number_rounded = number
    if 0.5 <= number - int(number) < 1:
        number_rounded = math.ceil(number)
    elif 0 < number - int(number) < 0.5:
        number_rounded = math.floor(number)
    elif number - int(number) == 0:
        number_rounded = number
    return number_rounded


def overpayment_print(payment_monthly, periods, principal):
    payment_total = math.ceil(payment_monthly) * periods
    overpayment = math.ceil(payment_total - principal)
    print("Overpayment = " + str(int(overpayment)))
    return None


ap = argparse.ArgumentParser()
ap.add_argument("--type", required=True, type=str, help="Calculation type")
ap.add_argument("--payment", required=False, type=float, help="Monthly payment")
ap.add_argument("--principal", required=False, type=float, help="Principal")
ap.add_argument("--periods", required=False, type=int, help="Periods")
ap.add_argument("--interest", required=False, type=float, help="Interest")
args = vars(ap.parse_args())
calculation_type = args["type"]

if calculation_type == "annuity":
    if args["periods"] is not None and args["interest"] is not None and args["principal"]:
        credit_principal = args["principal"]
        credit_interest_monthly = args["interest"] / 1200
        credit_periods = args["periods"]
        credit_payment_monthly = calc_annuity(credit_principal, credit_interest_monthly, credit_periods)
        overpayment_print(credit_payment_monthly, credit_periods, credit_principal)
        print("Monthly payment: "+str(math.ceil(credit_payment_monthly)))
    elif args["principal"] is not None and args["payment"] is not None and args["interest"] is not None:
        credit_principal = args["principal"]
        credit_payment_monthly = args["payment"]
        credit_interest_monthly = args["interest"] / 1200
        credit_periods = calc_periods(credit_payment_monthly, credit_interest_monthly, credit_principal)
        credit_time_years = int(math.floor(credit_periods // 12))
        credit_time_months = int(math.ceil((credit_periods % 12)))
        if credit_time_months == 12:
            credit_time_years += 1
            credit_time_months = 0
        if credit_time_years == 1 and credit_time_months == 0:
            print("You need 1 year to repay this credit")
        elif credit_time_years == 0 and credit_time_months == 1:
            print("You need 1 month to repay this credit")
        elif credit_time_years == 0 and credit_time_months > 1:
            print("You need " + str(credit_time_months) + " months to repay this credit!")
        elif credit_time_years == 1 and credit_time_months == 1:
            print("You need 1 year and 1 month to repay this credit!")
        elif credit_time_years > 1 and credit_time_months == 0:
            print("You need " + str(credit_time_years) + " years to repay this credit!")
        elif credit_time_years > 1 and credit_time_months > 1:
            print("You need " + str(credit_time_years) + " years and " + str(
                credit_time_months) + "months to repay this credit!")
        overpayment_print(credit_payment_monthly, credit_periods, credit_principal)
    elif args["payment"] is not None and args["periods"] is not None and args["principal"]:
        print("test2")
    elif args["payment"] is not None and args["periods"] is not None and args["interest"] is not None:
        credit_payment_monthly = args["payment"]
        credit_interest_monthly = args["interest"] / 1200
        credit_periods = args["periods"]
        credit_principal = calc_principal(credit_payment_monthly, credit_interest_monthly, credit_periods)
        credit_principal_print = round_print(credit_principal)
        print("Your credit principal = " + str(credit_principal_print) + "!")
        overpayment_print(credit_payment_monthly, credit_periods, credit_principal)
    else:
        print(args["principal"])
        print(args["payment"])
        print(args["interest"])
        print(args["periods"])
        print("1Incorrect parameters")
elif calculation_type == "diff":
    if args["principal"] is not None and args["periods"] is not None and args["interest"]:
        credit_principal = args["principal"]
        credit_periods = args["periods"]
        credit_interest_monthly = args["interest"] / 1200
        credit_payment = 0
        credit_payment_total = 0
        for month in range(1, credit_periods+1):
            credit_payment = diff_payment(credit_principal, credit_periods, credit_interest_monthly, month)
            credit_payment_total = credit_payment_total + math.ceil(credit_payment)
            print("Month " + str(month) + ": paid out " + str(math.ceil(credit_payment)))
        print("\nOverpayment = "+str(credit_payment_total-credit_principal))
    else:
        print("2Incorrect parameters")
else:
    print("3Incorrect parameters")