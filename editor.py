from tksheet import Sheet
import tkinter as tk
import user_report
import requests
import json
import configparser

config = configparser.RawConfigParser()
config.read('config.properties')
token = config.get('DEFAULT', 'CONNECT_API_TOKEN')
base_url = config.get('DEFAULT', 'CONNECT_API_ENDPOINT')

class Editor(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Editor')
        self.geometry("%dx%d+0+0" % (self.winfo_screenwidth(), self.winfo_screenheight()))
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        file_menu = tk.Menu(menubar)
        file_menu.add_command(label='Save', command=self.save)
        file_menu.add_command(label='Reset', command=self.load_report)
        file_menu.add_command(label='Exit', command=self.destroy)
        menubar.add_cascade(label="File", menu=file_menu)
        save_menu = tk.Menu(menubar)
        save_menu.add_command(label='Save', command=self.save)
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 1)
        self.frame = tk.Frame(self)
        self.frame.grid_columnconfigure(0, weight = 1)
        self.frame.grid_rowconfigure(0, weight = 1)
        self.sheet = Sheet(
            self.frame, 
            headers = ['Username', 'Email', 'Join date', 'Institution']
        )
        self.sheet.readonly_columns(columns=[0,1,2], readonly=True)
        self.sheet.enable_bindings(bindings = "all")
        self.frame.grid(row = 0, column = 0, sticky = "nswe")
        self.sheet.grid(row = 0, column = 0, sticky = "nswe")
        self.load_report()

    def load_report(self):
        print("Downloading report...")
        report = user_report.get_user_report('root.atlas-af')
        print("Finished downloading report")
        self.sheet.set_sheet_data(data=[[user['username'], user['email'], user['join_date'], user['institution']] for user in report])
        self.sheet.set_all_column_widths(width = int(self.winfo_screenwidth()/4))
        # self.sheet.set_all_cell_sizes_to_text()

    def save(self):
        print("Updating database...")
        sheet_data = self.sheet.get_sheet_data()
        for user in sheet_data:
            username = user[0]
            institution = user[3]
            profile = user_report.get_user_profile(username)
            if profile['metadata']['unix_name'] == username and profile['metadata']['institution'] != institution:
                # print("Updating user %s" %user[0])
                self.update_user(username, institution)            
        print("Finished updating database")

    def update_user(self, username, institution):
        query = {"token": token}
        json_data = {'apiVersion': 'v1alpha1', 'kind': 'User', 'metadata': {'institution': institution}}
        url = base_url + "/v1alpha1/users/" + username
        try:
            resp = requests.put(url, params=query, json=json_data)
            print("Response status: " + str(resp.status_code))
            # print("Response content: " + str(resp.content))
            # print("Response text: " + str(resp.text))
            print("Updated user %s. Set institution to %s" %(username, institution))
        except Exception as err:
            print("Error updating user %s: %s" %(username, str(err)))

if __name__ == "__main__":
    app = Editor()
    app.mainloop()