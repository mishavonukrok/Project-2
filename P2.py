import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
import datetime
import csv

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Event Manager")
        self.geometry("500x450")

        self.events = []

        self.load_events_from_csv()

        self.create_widgets()

    def create_widgets(self):
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.new_event_btn = tk.Button(self.main_frame, text="New event", command=self.new_event)
        self.new_event_btn.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        self.change_event_btn = tk.Button(self.main_frame, text="Change event", command=self.change_event)
        self.change_event_btn.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        
        self.delete_event_btn = tk.Button(self.main_frame, text="Delete event", command=self.delete_event)
        self.delete_event_btn.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

    def new_event(self):
        self.event_form(None)

    def change_event(self):
        event_selection = tk.Toplevel(self)
        event_selection.title("Select an event")

        event_list = tk.Listbox(event_selection)
        event_list.pack(fill=tk.BOTH, expand=True)

        for index, event in enumerate(self.events):
            event_list.insert(tk.END, f"{index + 1}. {event['name']}")

        event_list.bind("<Double-1>", lambda e: self.event_form(index=event_list.curselection()[0], event_selection=event_selection))
        
    def delete_event(self):
        event_selection = tk.Toplevel(self)
        event_selection.title("Select an event to delete")

        event_list = tk.Listbox(event_selection)
        event_list.pack(fill=tk.BOTH, expand=True)

        for index, event in enumerate(self.events):
            event_list.insert(tk.END, f"{index + 1}. {event['name']}")

        event_list.bind("<Double-1>", lambda e: self.confirm_delete(index=event_list.curselection()[0], event_selection=event_selection))
        
    def confirm_delete(self, index, event_selection):
        def delete():
            del self.events[index]
            self.save_events_to_csv()
            messagebox.showinfo("Success", "Event deleted successfully.")
            event_info_window.destroy()
            event_selection.destroy()

        event = self.events[index]
        event_info_window = tk.Toplevel(self)
        event_info_window.title("Event Information")

        event_info_label = tk.Label(event_info_window, text=f"Name: {event['name']}\nTime: {event['time']}\nDate: {event['date']}\nAddress: {event['address']}\nComment: {event['comment']}")
        event_info_label.pack(pady=10)

        delete_button = tk.Button(event_info_window, text="Delete", command=delete)
        delete_button.pack(pady=5)


    def event_form(self, index, event_selection=None):
        event_window = tk.Toplevel(self)
        event_window.title("Event Form")
        self.geometry("500x400")

        form_frame = tk.Frame(event_window)
        form_frame.pack(pady=10)

        # Name
        name_label = tk.Label(form_frame, text="Name:")
        name_label.grid(row=0, column=0, sticky="w")
        self.name_entry = tk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, sticky="w")

        # Time
        time_label = tk.Label(form_frame, text="Time:")
        time_label.grid(row=1, column=0, sticky="w")

        hours = [str(i) for i in range(1, 13)]
        minutes = [f"{i:02}" for i in range(60)]
        ampm = ['AM', 'PM']

        self.hour_combobox = ttk.Combobox(form_frame, values=hours, state="readonly", width=3)
        self.hour_combobox.grid(row=1, column=1, sticky="w")

        self.minute_combobox = ttk.Combobox(form_frame, values=minutes, state="readonly", width=3)
        self.minute_combobox.grid(row=1, column=2, sticky="w")

        self.ampm_combobox = ttk.Combobox(form_frame, values=ampm, state="readonly", width=3)
        self.ampm_combobox.grid(row=1, column=3, sticky="w")

        # Date
        date_label = tk.Label(form_frame, text="Date:")
        date_label.grid(row=2, column=0, sticky="w")
        self.date_btn = tk.Button(form_frame, text="Select Date", command=self.select_date)
        self.date_btn.grid(row=2, column=1, sticky="w")
        
        # Address
        address_label = tk.Label(form_frame, text="Address:")
        address_label.grid(row=3, column=0, sticky="w")
        self.address_entry = tk.Entry(form_frame)
        self.address_entry.grid(row=3, column=1, sticky="w")

        # Comment
        comment_label = tk.Label(form_frame, text="Comment:")
        comment_label.grid(row=4, column=0, sticky="w")
        self.comment_text = tk.Text(form_frame, width=25, height=5, wrap=tk.WORD)
        self.comment_text.grid(row=4, column=1, sticky="w")

        if index is not None:
            event = self.events[index]
            self.name_entry.insert(0, event["name"])
            hour, minute, am_pm = event["time"].split(":")[0], event["time"].split(":")[1][:2], event["time"].split()[1]
            self.hour_combobox.set(hour)
            self.minute_combobox.set(minute)
            self.ampm_combobox.set(am_pm)
            self.date_btn.config(text=event["date"])
            self.address_entry.insert(0, event["address"])
            self.comment_text.insert(tk.END, event["comment"])

        button_frame = tk.Frame(event_window)
        button_frame.pack(pady=10)

        save_btn = tk.Button(button_frame, text="Save", command=lambda: self.save_event(index, event_window, event_selection))
        save_btn.grid(row=0, column=0, padx=5)

        clear_btn = tk.Button(button_frame, text="Clear", command=self.clear_form)
        clear_btn.grid(row=0, column=1, padx=5)

    def select_date(self):
        def on_date_select():
            date = cal.selection_get()
            if date:
                self.date_btn.config(text=date.strftime("%Y-%m-%d"))
            date_window.destroy()

        date_window = tk.Toplevel(self)
        cal = Calendar(date_window, selectmode="day", date_pattern="y-mm-dd")
        cal.pack(fill=tk.BOTH, expand=True)
        ok_btn = tk.Button(date_window, text="OK", command=on_date_select)
        ok_btn.pack(pady=5)

    def save_event(self, selected_event, event_window, event_selection=None):
        name = self.name_entry.get()
        time = f"{self.hour_combobox.get()}:{self.minute_combobox.get()} {self.ampm_combobox.get()}"
        date = self.date_btn["text"]
        address = self.address_entry.get()
        comment = self.comment_text.get(1.0, tk.END).strip()

        if not name or not time or not date or not address:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        event_info = {
            "name": name,
            "time": time,
            "date": date,
            "address": address,
            "comment": comment
        }

        if selected_event is not None:
            self.events[selected_event] = event_info
        else:
            self.events.append(event_info)

        self.save_events_to_csv()
        messagebox.showinfo("Success", "Event saved successfully.")
        self.clear_form()
        event_window.destroy()
        if event_selection:
            event_selection.destroy()

    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.hour_combobox.set('')
        self.minute_combobox.set('')
        self.ampm_combobox.set('')
        self.date_btn.config(text="Select Date")
        self.address_entry.delete(0, tk.END)
        self.comment_text.delete(1.0, tk.END)

    def load_events_from_csv(self):
        try:
            with open("events.csv", "r") as csvfile:
                reader = csv.DictReader(csvfile)
                self.events = [row for row in reader]
        except FileNotFoundError:
            pass
    
    def save_events_to_csv(self):
        with open("events.csv", "w", newline='') as csvfile:
            fieldnames = ["name", "time", "date", "address", "comment"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.events)

if __name__ == "__main__":
    app = Application()
    app.mainloop()