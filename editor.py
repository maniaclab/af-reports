from tksheet import Sheet
import tkinter as tk
import user_report

class Editor(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Editor')
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
        self.sheet = Sheet(self.frame, headers = ['Username', 'Email', 'Join date', 'Institution'])
        self.sheet.readonly_columns(columns=[0,1,2], readonly=True, redraw=True)
        self.sheet.enable_bindings()
        self.frame.grid(row = 0, column = 0, sticky = "nswe")
        self.sheet.grid(row = 0, column = 0, sticky = "nswe")
        self.load_report()

    def load_report(self):
        print("Downloading report...")
        report = user_report.get_user_report('root.atlas-af')
        print("Finished downloading report")
        self.sheet.set_sheet_data(data=[[user['username'], user['email'], user['join_date'], user['institution']] for user in report])

    def save(self):
        print("Saving")

if __name__ == "__main__":
    app = Editor()
    app.mainloop()