# A file transfer app that moves only files
# that have been updated in the past 24 hours,
# Moves files between user-selected folders
# Also includes function that retrieves the last
# time that the file transfer widget was used

# Author: James Merrill
# Python version 3.5

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import shutil
import os
import os.path
import datetime
import time
import sqlite3

class Window:

    def create_database():
        conn = sqlite3.connect('transfer_history.db')
        with conn:
            c = conn.cursor()
            c.execute("CREATE TABLE if not exists tbl_history( \
                ID INTEGER PRIMARY KEY, unix REAL, datestamp TEXT);")
            conn.commit()
        conn.close()
    create_database()

    def __init__(self,master):
        
        master.title('24 hour file transfer app')
        master.resizable(False, False)
        self.header_frame = ttk.Frame(master)
        self.header_frame.pack()
        
        ttk.Label(self.header_frame, text = "Move today's files...").grid(row=1, column=2, columnspan=2, padx=10, pady=10,)
        ttk.Label(self.header_frame, text = "Select file origin:").grid(row=2, column=1, columnspan=1, padx=5, pady=10, sticky = 'e')
        ttk.Label(self.header_frame, text = "Select file destination:").grid(row=3, column=1, columnspan=1, padx=5, pady=10, sticky = 'e')
        ttk.Label(self.header_frame, text = "Time of last transfer:").grid(row=4, column=2, columnspan=1, padx=5, pady=10, sticky = 'e')

        self.origin_name = StringVar()
        self.dest_name = StringVar()
        self.last_transfer = StringVar()

        ttk.Label(self.header_frame, textvariable = self.origin_name, width = 50, relief = SUNKEN).grid(row=2, column=2, columnspan=2, padx=10, pady=10)
        ttk.Label(self.header_frame, textvariable = self.dest_name, width = 50, relief = SUNKEN).grid(row=3, column=2, columnspan=2, padx=10, pady=10)
        ttk.Label(self.header_frame, textvariable = self.last_transfer, width = 30, relief = SUNKEN).grid(row=4, column=3, columnspan=1, padx=10, pady=10)

        ttk.Button(self.header_frame, text = 'Browse...',command = self.origin).grid(row=2, column=4, columnspan=1, padx=10)
        ttk.Button(self.header_frame, text = 'Browse...',command = self.destination).grid(row=3, column=4, columnspan=1, padx=10, pady=10)             
        ttk.Button(self.header_frame, text = 'Transfer Files!',command = self.move_files).grid(row=5, column=2, columnspan=2, padx=10, pady=10)
        
        def show_last_transfer(self):
            conn = sqlite3.connect('transfer_history.db')
            with conn:
                c = conn.cursor()
                c.execute("SELECT * FROM tbl_history WHERE unix = (SELECT MAX(unix) FROM tbl_history)")
                for row in c.fetchall():
                    print(row[2])
                    self.last_transfer.set(row[2])
        show_last_transfer(self)
    
    def origin(self):
        self.origin = filedialog.askdirectory(title='Choose a file')
        if self.origin:
            self.origin_name.set(self.origin)       
            print(self.origin)
        
    def destination(self):
        self.destination = filedialog.askdirectory(title='Choose a file')
        if self.destination:
            self.dest_name.set(self.destination)
            print(self.destination)
          
    def move_files(self):
        for file in os.listdir(self.origin):
            from datetime import date, datetime, time, timedelta
            file = os.path.join(self.origin, file)
            now = datetime.now()
            before = now - timedelta(hours=24)
            last_modified_date = datetime.fromtimestamp(os.path.getmtime(file))
            if  last_modified_date > before:
                shutil.move(file, self.destination)
                print (file)
            conn = sqlite3.connect('transfer_history.db')
            import time
            import datetime
            with conn:
                c = conn.cursor()
                if file:
                    unix = time.time()
                    date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
                    c.execute("INSERT INTO tbl_history (unix, datestamp) VALUES (?, ?)", (unix, date))
                    conn.commit()

def main():
    root = Tk()
    window = Window(root)
    root.mainloop()

if __name__ == "__main__": main()
