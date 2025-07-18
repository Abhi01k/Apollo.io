from datetime import datetime
import os

ts_file = f"{datetime.now().strftime('%y%m%d-%H%M')}"
ts_db = f"{datetime.now().strftime('%Y-%m-%d %H:%M')}"
ts_time = f"{datetime.now().strftime('%H:%M:%S')}"
print(f"\n---------- {ts_time} starting {os.path.basename(__file__)}")
import time
start_time = time.time()

from dotenv import load_dotenv
load_dotenv()
PROJECTS_FOLDER = os.getenv("PROJECTS_FOLDER")
APOLLO_API_KEY = os.getenv("APOLLO_API_KEY")

import sys
sys.path.append(f"{PROJECTS_FOLDER}/indeXee")

import pprint
pp = pprint.PrettyPrinter(indent=4)

####################
# Apollo.io - Email enrichment

# IMPORTS (script-specific)

import requests
import sqlite3
from sqlite3 import Error
import my_utils

# GLOBALS

count_total = 0
count = 0
count_row = 0

test = True
v = False # verbose mode

# CLASSES

class PersonData:
    def __init__(self):
        self.first_name = None
        self.last_name = None
        self.domain = None
        self.email = None
        self.linkedin_url = None
        # Other attributes
        self.title = None
        self.headline = None
        self.country = None
        self.email_status = None
        self.company = None

    @property
    def name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        else:
            return None

    @property
    def email_prefix(self):
        if self.email is not None:
            return self.email.split('@')[0]

    def __str__(self):
        result = "\nPersonData("
        if self.email not in [None, '']:
            result += f"\nemail\t\t✅ {self.email}"
        if self.first_name is not None:
            result += f"\nfirst_name\t{self.first_name}"
        if self.last_name is not None:
            result += f"\nlast_name\t{self.last_name}"
        if self.domain is not None:
            result += f"\ndomain\t\t{self.domain}"
        if self.linkedin_url is not None:
            result += f"\nlinkedin_url\t{self.linkedin_url}"
        if self.title is not None:
            result += f"\ntitle\t\t{self.title}"
        if self.headline is not None:
            result += f"\nheadline\t{self.headline}"
        if self.country is not None:
            result += f"\ncountry\t\t{self.country}"
        if self.email_status is not None:
            result += f"\nemail_status\t{self.email_status}"
        if self.company is not None:
            result += f"\ncompany\t\t{self.company}"
        result += "\n)"
        return result

    def fetch_data(self, api_key, search_type, **kwargs):
        url = "https://api.apollo.io/v1/people/match"
        data = {
            "api_key": api_key,
            "search_type": search_type,
            **kwargs
        }
        headers = {
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/json'
        }

        response = requests.post(url, headers=headers, json=data)

        response_data = response.json().get('person', {})

        if v:
            for k,value in response_data.items():
                print(f"\n{k}: {value}")

        company = None
            company = "Apollo"  # default value

    for employment in response_data.get('employment_history', []):
        if employment.get('current'):
            company = employment.get('organization_name', 'Apollo')
            break

        self.linkedin_url = response_data.get('linkedin_url')
        self.first_name = response_data.get('first_name')
        self.last_name = response_data.get('last_name')
        self.title = response_data.get('title')
        self.headline = response_data.get('headline')
        country = response_data.get('country')
        if country != None:
            self.country = my_utils.country_code_from_location(response_data.get('country'))
        self.email = response_data.get('email')
        self.domain = my_utils.domain_from_email(response_data.get('email'))
        self.email_status = response_data.get('email_status')
        self.company = company





# FUNCTIONS

def add_person_to_db(person):
    conn = None
    try:
        conn = sqlite3.connect("/Users/nic/btob.db")
    except Error as e:
        print(e)

    if conn is None:
        print("Error! cannot create the database connection.")
        return

    with conn:
        # Check if the person already exists in the database based on the email
        cur = conn.cursor()

        if person.headline != None and 'is a role based email address' in person.headline:
            sql = '''INSERT INTO team_emails(email)
                        VALUES(?)'''
            email_prefix = person.email.split('@')[0]
            if len(email_prefix) > 2:
                add_to_db = (email_prefix,)
                cur.execute(sql, add_to_db)
                conn.commit()
                print(f"\n✅ 💿 Email prefix {email_prefix} added to team_emails in btob.db\n")

        else:

            cur.execute("SELECT * FROM contacts WHERE email = ?", (person.email,))
            existing_person = cur.fetchone()

            # If the person doesn't exist in the database, insert the new record
            if existing_person is None:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
                sql = '''INSERT INTO contacts(email, first, last, email_status, domain, country, title, linkedin, created, db, src)
                        VALUES(?,?,?,?,?,?,?,?,?,?,?)'''
                person_data = (person.email, person.first_name, person.last_name, person.email_status, person.domain, person.country, person.title, person.linkedin_url, current_time, 'DR', 'Apollo')
                cur.execute(sql, person_data)
                conn.commit()
                print("\n✅ 💿 Person added to btob.db\n")
            else:
                print("\n❌ Person already exists in btob.db\n")

def get_person_data_from_name_and_domain(first_name, last_name, domain):
    global APOLLO_API_KEY
    person = PersonData()
    person.fetch_data(APOLLO_API_KEY, 'name_and_domain', first_name=first_name, last_name=last_name, domain=domain)
    print(person)
    add_person_to_db(person)
    return person


def get_person_data_from_linkedin_url(linkedin_url):
    global APOLLO_API_KEY
    person = PersonData()
    person.fetch_data(APOLLO_API_KEY, 'linkedin_url', linkedin_url=linkedin_url)
    # print_attributes(person)
    print(person)
    add_person_to_db(person)
    return person


def get_person_data_from_email(email):
    global APOLLO_API_KEY
    person = PersonData()
    person.fetch_data(APOLLO_API_KEY, 'email', email=email)
    print(person)
    add_person_to_db(person)
    return person

# ########################################################################################################

if __name__ == '__main__':
    print('\n\n-------------------------------')

    # Change `run` between 'from_name', 'from_linkedin', and 'from_email' to run the script with different inputs
    run = 'from_email'

    if run == 'from_name':

        first = 'Paul'
        last = 'Atreides'
        domain = 'dune.org'

        person = get_person_data_from_name_and_domain(first, last, domain) # returns a PersonData object

    elif run == 'from_linkedin':

        linkedin_url = 'http://www.linkedin.com/in/paul-atreides-123456'

        person = get_person_data_from_linkedin_url(linkedin_url)

    elif run == 'from_email':

        email = 'paul.atreides@dune.org'

        person = get_person_data_from_email(email)

    run_time = round((time.time() - start_time), 1)
    if run_time > 60:
        print(f'\n{os.path.basename(__file__)} finished in {run_time/60} minutes.\n')
    else:
        print(f'\n{os.path.basename(__file__)} finished in {run_time}s.\n')