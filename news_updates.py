from configparser import ConfigParser
import yaml
import json
import sys
import requests
import csv
from openpyxl import Workbook
from tabulate import tabulate
from datetime import datetime

q = None


def select_config():
    print("Select type of config\n1. ini file\n2. yaml file\n3. json file")
    while True:
        select_val = input("Enter a config file from above : ")
        if select_val in ['1', '2', '3']:
            return select_val
        else:
            print("Entered value must be given data only")


def output_format():
    file_name = None
    print("1. Console\n2. Text file\n3. CSV file\n4. Excel file")
    while True:
        new_choice = input("Select one of the output format : ")
        if new_choice in ['2', '3', '4']:
            file_name = input("Enter file name: ")
            return new_choice, file_name
        elif new_choice == "1":
            return new_choice, file_name
        else:
            print("Entered data must be in displayed numbers only.")


def creating_multiple_sheets(my_dict, file_name):
    try:
        wb = Workbook()
        wb.remove_sheet(wb.active)
        for key, val in my_dict.items():
            ws = wb.create_sheet(key)
            for row in val:
                ws.append(row)
        wb.save(f"{file_name}.xlsx")
        wb.close()
    except Exception as e:
        print(f"Encountered exception | Reason:{e}")


def file_handling(my_dict, file_name, select_val, new_choice):
    global f
    while True:
        try:
            if new_choice == "2":
                try:
                    f = open(f"{file_name}.txt", "w")
                    for key, val in my_dict.items():
                        f.write(tabulate(val, headers=list(get_config('top_headers', select_val).values()),
                                         tablefmt='pretty'))
                        f.write('\n\n')
                except Exception as e:
                    print(f"Encountered Exception | Reason: {e}")
                    return False
                finally:
                    f.close()
                    return True
            elif new_choice == "3":
                try:
                    f = open(f"{file_name}.csv", "w")
                    csv_writer = csv.writer(f, lineterminator="\n")
                    for key, val in my_dict.items():
                        csv_writer.writerows(val)
                        csv_writer.writerow([''])
                        csv_writer.writerow([''])
                except Exception as e:
                    print(f"Encountered Exception | Reason: {e}")
                    return False
                finally:
                    f.close()
                    return True
        except Exception as e:
            print(f'Not be able to write the data ,Reason:{e}')


def trim_lines(text, char):
    if text is not None:
        lines = ""
        for i in range(0, len(text), char):
            lines += text[i:i + char] + "\n"
        return lines


def q_validation(params_passing):
    while True:
        query = input("Enter your Query : ")
        if query not in [None, " ", '']:
            params_passing.update({'q': query})
            break
        else:
            print("Enter a valid query..!")


def category_calling(params_passing, select_val):
    while True:
        calling_choice = input("Do you want to  Enter category(y/n):")
        if calling_choice.lower() == "y":
            cat_dict = get_config('categories', select_val)
            print("Select Category:")
            table = []
            for key, val in cat_dict.items():
                table.append([key, val])
            print(tabulate(table, headers=list(get_config('headers', select_val).values()), tablefmt="pretty"))
            while True:
                choice = input("Enter Category : ")
                if select_val == "2":
                    try:
                        choice = int(choice)
                        if choice in cat_dict.keys():
                            params_passing['category'] = cat_dict.get(choice)
                            break
                        else:
                            print("Invalid input given,try again")
                    except ValueError:
                        print("Invalid selection try again")

                else:
                    if choice in cat_dict.keys():
                        params_passing['category'] = cat_dict.get(choice)
                        break
                    else:
                        print("Invalid input,try again")
            return params_passing
        elif calling_choice == "n":
            break
        else:
            print("You entered wrong input,Please try again")


def country_calling(query_params, select_val):
    while True:
        calling_choice = input("Do you want to  Enter country(y/n) : ")
        if calling_choice.lower() == "y":
            country_var = get_config("country_var", select_val)
            country_code = get_config("country_code", select_val)
            table = []
            for key, val in country_var.items():
                table.append([key, val])
            print(tabulate(table, headers=list(get_config('headers', select_val).values()), tablefmt="pretty"))
            while True:
                choice = input("Enter your country : ")
                if select_val == "2":
                    try:
                        choice = int(choice)
                        if choice in country_code.keys():
                            query_params["country"] = country_code[choice]
                            break
                        else:
                            print("Enter valid values.")
                    except ValueError:
                        print("You selected wrong input,Please try again.")
                else:
                    if choice in country_code.keys():
                        query_params["country"] = country_code[choice]
                        break
                    else:
                        print("Enter correct values.")
            return query_params
        elif calling_choice == "n":
            break
        else:
            print("You entered invalid input,try again.")


def articles_calling(params_passing):
    while True:
        articles_choice = input("Do you want to Enter no of articles(y/n): ")
        if articles_choice == "y":
            num_articles = articles_search()
            params_passing.update({"pageSize": num_articles})
            break
        elif articles_choice == "n":
            break
        else:
            print("Invalid selection,Please try again.")


def articles_search():
    while True:
        try:
            numb_articles = int(input("Enter no of articles: "))
            return numb_articles
        except ValueError:
            print("Only digits are allowed,try again.")


def query_validation(query_params):
    while True:
        query = input("Enter your Query : ")
        if query not in [None, " ", '']:
            query_params.update({'q': query})
            break
        else:
            print("Enter a valid Query..!")


def lang_val(query_params, select_val):
    while True:
        lang_choice = input("Do you want to  Enter languages(y/n): ")
        if lang_choice.lower() == "y":
            lang_var = get_config("language", select_val)
            language_codes = get_config("language_codes", select_val)
            table = []
            for key, val in lang_var.items():
                table.append([key, val])
            print(tabulate(table, headers=list(get_config('headers', select_val).values()), tablefmt="pretty"))
            while True:
                choice = input("Enter language : ")
                if select_val == "2":
                    try:
                        choice = int(choice)
                        if choice in language_codes.keys():
                            query_params["language"] = language_codes[choice]
                            break
                        else:
                            print("You entered wrong input,Please try again.")
                    except ValueError:
                        print("Invalid selection, Please try again.")
                else:

                    if choice in language_codes.keys():
                        query_params["language"] = language_codes[choice]
                        break
                    else:
                        print("You entered wrong input,try again.")

            return query_params
        elif lang_choice == "n":
            break
        else:
            print('You selected invalid option try again.')


def sort_validation(query_params, select_val):
    while True:
        sort_choice = input("Do you want to perform sort operations(y/n): ")
        if sort_choice.lower() == "y":
            sort_var = get_config('sort_val', select_val)
            table = []
            for key, val in sort_var.items():
                table.append([key, val])
            print(tabulate(table, headers=list(get_config('headers_val', select_val).values()), tablefmt="pretty"))
            while True:
                choice = input("select one sort operation: ")
                if select_val == "2":
                    try:
                        choice = int(choice)
                        if choice in sort_var.keys():
                            query_params["sortBy"] = sort_var.get(choice)
                            break
                        else:
                            print("You entered invalid option try again.")
                    except ValueError:
                        print("Invalid selection try again.")
                else:
                    if choice in sort_var.keys():
                        query_params["sortBy"] = sort_var.get(choice)
                        break
                    else:
                        print("You entered invalid option try again.")
            return query_params
        elif sort_choice == "n":
            break
        else:
            print('You selected invalid option try again.')


def get_config(section, select_val, key=None):
    if select_val == "1":
        config = ConfigParser()
        config.read('config.ini')
        if key is not None:
            return config.get(section, key)
        else:
            return dict(config.items(section))
    elif select_val == "2":
        file = open('config.yaml', 'r')
        data = yaml.safe_load(file)
        file.close()
        if key is not None:
            return data.get(section)[key]
        else:
            return data.get(section)
    elif select_val == "3":
        file = open('config.json', 'r')
        data = json.load(file)
        file.close()
        if key is not None:
            return data.get(section)[key]
        else:
            return data.get(section)


def articles_validation(query_params):
    while True:
        articles_choice = input("Do you want to Enter no of articles(y/n) : ")
        if articles_choice.lower() == "y":
            num_articles = calling_articles()
            query_params.update({"pageSize": num_articles})
            break
        elif articles_choice == "n":
            break
        else:
            print("Invalid selection,please try again.")


def dates_validation(select_val, date_type):
    while True:
        date = input(f"Enter the {date_type} date(YYYY-MM-DD): ")
        try:
            date_val_parsed = datetime.strptime(date, '%Y-%m-%d')

        except Exception as e:
            print(e)
            print("Invalid Date. Please provide the date.")
        else:
            res = get_config('days_limit', select_val, 'days')
            if (datetime.today() - date_val_parsed).days > int(res):
                print("Invalid date range. provide date range in less than 30 days")
            else:
                return date


def inp_dates(query_params, select_val):
    while True:
        dates_choice = input("Do you want to  Enter dates_choice(y/n) : ")
        if dates_choice.lower() == "y":
            start_date = dates_validation(select_val, date_type='from')
            end_date = dates_validation(select_val, date_type='to')
            query_params.update({'from': start_date, 'to': end_date})
            break
        elif dates_choice == "n":
            break
        else:
            print("You entered invalid selection try again.:")


def calling_articles():
    while True:
        try:
            numb_articles = int(input("Enter no.of articles : "))
            return numb_articles
        except ValueError:
            print("Only digits are allowed,try again.")


def api_call(url, request_method, params=None, data=None):
    if request_method == "POST":
        if data is None:
            print("In POST request must and should provide the payload/body")
            sys.exit(1)
    response = requests.request(method=request_method, url=url, params=params, data=data)
    if response.status_code in [200, 201, 204]:
        return response.json()
    else:
        print(
            f"Noticed Error while making an API Call | Status Code : {response.status_code}"
            f" | Reason : {response.reason}")


def main():
    count = 1
    my_dict = {}
    select_val = select_config()
    new_choice, file_name = output_format()

    while True:
        print("1. Search Everything \n2. Search Top-Headlines")
        try:
            while True:
                try:
                    choice = int(input("Enter your choice : "))
                    if choice in [1, 2]:
                        break
                    else:
                        print("Enter given numbers only,try again.")
                except ValueError:
                    print("Invalid selection, Please try again.")

            if choice == 1:
                print("You selected Everything api..!")
                try:
                    url = get_config('details', select_val, 'everything_api')
                except Exception as e:
                    print(f'Noticed Error | Reason: {e}')
                    sys.exit(1)
                query_params = {"apiKey": "4a7485605e3e460c8ba644568d0e4b4b"}
                query_validation(query_params)
                inp_dates(query_params, select_val)
                lang_val(query_params, select_val)
                sort_validation(query_params, select_val)
                articles_validation(query_params)
                output = api_call(url=url, request_method="GET", params=query_params)
                if output is not None:
                    table = []
                    temp = output.get("articles")
                    if len(temp) > 0:
                        for i in temp:
                            table.append([i.get("source").get("name"), i.get("author"),
                                          trim_lines(i.get("title"), 50),
                                          trim_lines(i.get("publishedAt"), 50),
                                          trim_lines(i.get("description"), 20)])
                        if new_choice == '1':
                            print(tabulate(table, headers=list(get_config('top_headers', select_val).values()),
                                           tablefmt='pretty'))
                        elif new_choice == '2':
                            my_dict[f'operation_{count}'] = table
                            count += 1
                        elif new_choice == "3":
                            table.insert(0, list(get_config('top_headers', select_val).values()))
                            my_dict[f'operation_{count}'] = table
                            count += 1
                        elif new_choice == "4":
                            table.insert(0, list(get_config('top_headers', select_val).values()))
                            for k, v in query_params.items():
                                if k == "q":
                                    my_dict[v] = table
                    else:
                        print("No records found..!")
            elif choice == 2:
                print("You selected top Headlines api")
                try:
                    url = get_config('details', select_val, 'thl_api')
                except Exception as e:
                    print(f'Noticed Error | Reason: {e}')
                    sys.exit(1)
                params_passing = {'apiKey': '4a7485605e3e460c8ba644568d0e4b4b'}
                q_validation(params_passing)
                category_calling(params_passing, select_val)
                country_calling(params_passing, select_val)
                articles_calling(params_passing)
                output = api_call(url=url, request_method="GET", params=params_passing)
                if output is not None:
                    table = []
                    temp = output.get("articles")
                    if len(temp) > 0:
                        for i in temp:
                            table.append([i.get("source").get("name"), i.get("author"),
                                          trim_lines(i.get("title"), 50),
                                          trim_lines(i.get("publishedAt"), 50),
                                          trim_lines(i.get("description"), 20)])
                        if new_choice == '1':
                            print(tabulate(table, headers=list(get_config('top_headers', select_val).values()),
                                           tablefmt='pretty'))
                        elif new_choice == '2':
                            my_dict[f'operation_{count}'] = table
                            count += 1
                        elif new_choice == "3":
                            table.insert(0, list(get_config('top_headers', select_val).values()))
                            my_dict[f'operation_{count}'] = table
                            count += 1
                        elif new_choice == "4":
                            table.insert(0, list(get_config('top_headers', select_val).values()))
                            for k, v in params_passing.items():
                                if k == "q":
                                    my_dict[v] = table

                    else:
                        print("No records found..!")
            else:
                print("You selected invalid option try again.")
        except ValueError:
            print("Only digits are allowed,Please try again.")

        while True:
            end = input("Do you want to continue(y/n):")
            if end.lower() == "y":
                status = True
                break
            elif end.lower() == "n" and new_choice == "2":
                file_handling(my_dict, file_name, select_val, new_choice)
                print("File created successfully")
                print(f'File data stored in,{file_name}.txt')
                status = False
                break
            elif end.lower() == "n" and new_choice == "3":
                file_handling(my_dict, file_name, select_val, new_choice)
                print("file created successfully")
                print(f'file data stored in,{file_name}.csv')
                status = False
                break
            elif end.lower() == "n" and new_choice == "4":
                creating_multiple_sheets(my_dict, file_name)
                print(f'file data stored in,{file_name}.xlsx')
                status = False
                break
            elif end.lower() == "n":
                status = False
                break
            else:
                print("You entered invalid input, Please try again.")
        if status:
            continue
        else:
            print("Thanks for using News Api..!")
            break


main()
