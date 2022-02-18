import user_report

def get_email_list():
    email_list = []
    report = user_report.get_user_report('root.atlas-af')
    for user in report:
        email_list.append(user['email'])
    return email_list

if __name__ == "__main__":
    email_list = get_email_list()
    filecontents = ','.join(email_list)
    print("Email list: " + filecontents)
    with open('email_list.txt', 'w') as file:
        file.write(filecontents)