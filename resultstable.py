# Tokouete Brice
# 1651006


# import of datetime library and mysql connector
import requests
import json
import datetime
from datetime import date
import mysql.connector
from mysql.connector import Error


# defined the creation of the connection to the database from inclass lecture
def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

# defined the query and read execution function from inclass lecture
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

# Let make the connection to the cis3368 database on mysql
connection = create_connection("cis3368.c3rczxv5d35n.us-east-1.rds.amazonaws.com", "admin", "99Nav&Har14$", "cis3368db")

# create menu list for the results table database
menu = ('\nMENU\n'
        'n - Company Name: \n'
        'a - Display Currency: \n'
        'g - Display Gross Profit: \n'
        'b - Display Profit Margin: \n'
        'k - Quarterly Earnings Growth: \n'
        'l - Latest Quarter Date: \n' 
        's - Store to DataBase: \n'
        'o - Output all data from table: \n'
        'd - Delete entry: \n'
        'm - Summary: \n'
        'q - Quit\n')


select_symbol = input("Enter the symbol for which company data should be retrieved (e.g. BA, IBM, BAC, BABA, AWS, SAIC): \n")

# call of the API with the use of key, display the header and the json format content of the API 
company_result = requests.get("https://www.alphavantage.co/query?function=OVERVIEW&symbol="+ str(select_symbol) +"&apikey=OTR0R9KB5I9EOBT0") 
print(company_result)
print(company_result.json())

# Storing json object in variable
json_company_result = company_result.json()

# Used of option for the user to select from
option = ''
while option != 'q':
    print(menu)
    option = input('Choose an option: ')
    if option == 'n':
        name = json_company_result["Name"]
        print("Company Name: %s" % (name))

    elif option == 'a':
        currency = json_company_result["Currency"]
        print("Currency: %s" % (currency))

    elif option == 'g':
        gros = json_company_result["GrossProfitTTM"]
        print("Gross Profit: %s" % (gros))

    elif option == 'b':
        margin = json_company_result["ProfitMargin"]
        print("Profit Margin: %s" % (margin))

    elif option == 'k':
        earning = json_company_result["QuarterlyEarningsGrowthYOY"]
        print("QuarterlyEarnings Growth: %s" % (earning))

    elif option == 'l':
        latest = json_company_result["LatestQuarter"]
        print("Latest Quarter Date: %s" % (latest))

    elif option == 'm':

        print("Company Summary: \n")
        name = json_company_result["Name"]
        print("Company Name: %s" % (name))
        gros = json_company_result["GrossProfitTTM"]
        print("Gross Profit: %s" % (gros))

    # adding the selected input to the result table in to the DataBase
    elif option == 's':
        CompanyName = json_company_result["Name"]
        CurrencyVal = json_company_result["Currency"]
        CompanyGross = json_company_result["GrossProfitTTM"]
        CompanyMargin = json_company_result["ProfitMargin"]
        CompanyEarning = json_company_result["QuarterlyEarningsGrowthYOY"]
        latest_date = json_company_result["LatestQuarter"]

        query = "INSERT INTO results (Name, Currency, GrossProfitTTM, ProfitMargin, QuarterlyEarningsGrowthYOY, LatestQuarter) VALUES ('%s','%s', %s, %s, %s, '%s')" % (CompanyName, CurrencyVal, CompanyGross, CompanyMargin, CompanyEarning, latest_date)
        execute_query(connection, query)

    # outputing all data from the results table in the DataBase
    elif option == 'o':
        select_results = "SELECT * FROM results"
        results = execute_read_query(connection, select_results)
        for i in results:
            print(i)

    # deleting the data from the result table in the DAtaBase
    elif option == 'd':
        result_delete = input('Enter id number:\n')
        delete_query = 'DELETE FROM results WHERE id = %s' % (result_delete)
        execute_query(connection, delete_query)



