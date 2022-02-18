import matplotlib.pyplot as plt
import csv
from dateutil.parser import parse
from datetime import datetime 
from datetime import timedelta
import requests
import configparser

config = configparser.RawConfigParser()
config.read('config.properties')
token = config.get('DEFAULT', 'CONNECT_API_TOKEN')
base_url = config.get('DEFAULT', 'CONNECT_API_ENDPOINT')

def get_users(group):
    url = base_url + "/v1alpha1/groups/" + group + "/members?token=" + token
    users = requests.get(url).json()
    return users

def get_user_profile(username):
    url = base_url + "/v1alpha1/users/" + username + "?token=" + token
    user_profile = requests.get(url).json()
    return user_profile

def get_user_report(group):
    user_list = []
    users = get_users(group)

    for member in users['memberships']:
        username = member['user_name']
        user_profile = get_user_profile(username)
        username = user_profile['metadata']['unix_name'] 
        join_date = parse(user_profile['metadata']['join_date']).strftime('%Y/%m/%d')
        jd = datetime.strptime(join_date, '%Y/%m/%d')
        email = user_profile['metadata']['email']
        institution = user_profile['metadata']['institution']
        name = user_profile['metadata']['name']
        phone = user_profile['metadata']['phone']
        user_entry = {
            'username': username, 
            'email': email, 
            'institution': institution,
            'join_date': join_date,
            'jd': jd,
            'group': group
        }
        user_list.append(user_entry)

    return user_list

def write_user_report(filename, user_report):
    sorted_user_report = sorted(user_report, key=lambda user : user['jd'], reverse=True)
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(['Username', 'Email', 'Join date', 'Group', 'Institution'])
        for user in sorted_user_report:
            csvwriter.writerow([user['username'], user['email'], user['join_date'], user['group'], user['institution']])

def plot_user_report(filename, user_report):
    xvalues_format = "%m-%Y" 
    xvalues_set = set()
    for user in user_report:
        join_date = user['jd']
        xvalue = datetime(join_date.year, join_date.month, 1).strftime(xvalues_format)
        xvalues_set.add(xvalue)
    xvalues = list(xvalues_set)
    xvalues.sort(key=lambda x:datetime.strptime(x, xvalues_format))
    yvalues = [0] * len(xvalues)
    for i in range(len(xvalues)):
        xvalue = datetime.strptime(xvalues[i], xvalues_format)
        L = list(filter(lambda u : ((xvalue.year - u['jd'].year) * 12) + (xvalue.month - u['jd'].month) >= 0, user_report))
        yvalues[i] = len(L)
    plt.bar(xvalues, yvalues, color = 'g', width = 0.72, label = "Number of users by month")
    plt.xlabel('Month')
    plt.ylabel('Number of users')
    plt.title('Number of users by month')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    group = 'root.atlas-af'
    user_report = get_user_report(group)
    write_user_report('user_report.csv', user_report)
    print("Created user report for group %s and wrote to user_report.csv" %group)
    plot_user_report('user_report.png', user_report)
    print("Plotted user report for group %s and saved image to user_report.png" %group)