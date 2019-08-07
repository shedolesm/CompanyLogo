from flask import Flask, jsonify
import json
from collections import Counter
import operator
import re


app = Flask(__name__)
app.config["DEBUG"] = True


def get_me_logo(fcompanyName):
    upper_company_name = re.sub(r"[^A-Za-z]", "", fcompanyName.upper())
    char_counts = dict(Counter(upper_company_name))
    sorted_char_counts_alphabetically = dict(sorted(char_counts.items(), key=operator.itemgetter(0)))
    most_frequent_sorted_alphabetically = sorted(sorted_char_counts_alphabetically.items(), key=operator.itemgetter(1), reverse=True)
    if len(most_frequent_sorted_alphabetically) >= 3:
        logo = most_frequent_sorted_alphabetically[0][0] + "," + most_frequent_sorted_alphabetically[1][0] + "," + most_frequent_sorted_alphabetically[2][0]
    elif len(most_frequent_sorted_alphabetically) == 2:
        logo = most_frequent_sorted_alphabetically[0][0] + "," + most_frequent_sorted_alphabetically[1][0]
    else:
        logo = most_frequent_sorted_alphabetically[0][0]
    return logo.rstrip(" ")


try:
    with open("CompaniesList.json", "r", encoding="utf8") as write_file:
        data = json.load(write_file)
except FileNotFoundError:
    print("No Data File Found!")


@app.route('/api/v1.0/resources/companies/all', methods=['GET'])
def get_all_companies():
    return jsonify(data)


@app.route('/api/v1.0/resources/companies/<string:company_id>', methods=['GET'])
def get_task(company_id):
    company = [company for company in data if company['CompanyId'] == company_id]
    if len(company) == 0 or company is None:
        return jsonify({"status": "404", "data": "Please specify Valid Company ID!"})
    company[0]["logoCharacters"] = get_me_logo(company[0]['Company Name'])

    return jsonify(company[0])


if __name__ == '__main__':
    app.run()

