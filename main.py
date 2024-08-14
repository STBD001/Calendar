import tkinter as tk
from tkinter import simpledialog, messagebox
import calendar
from datetime import datetime

class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personalizowany Kalendarz Zadań")
        self.current_year = datetime.now().year
        self.current_month = datetime.now().month
        self.events = {}

        self.create_calendar()

    def create_calendar(self):
        self.cal_frame = tk.Frame(self.root)
        self.cal_frame.pack()
        self.nav_frame = tk.Frame(self.root)
        self.nav_frame.pack()

        self.prev_button = tk.Button(self.nav_frame, text="<", command=self.prev_month)
        self.prev_button.grid(row=0, column=0)

        self.next_button = tk.Button(self.nav_frame, text=">", command=self.next_month)
        self.next_button.grid(row=0, column=2)

        self.month_label = tk.Label(self.nav_frame, text=f"{calendar.month_name[self.current_month]} {self.current_year}")
        self.month_label.grid(row=0, column=1)

        self.draw_calendar()

    def draw_calendar(self):
        for widget in self.cal_frame.winfo_children():
            widget.destroy()

        self.month_label.config(text=f"{calendar.month_name[self.current_month]} {self.current_year}")

        cal = calendar.monthcalendar(self.current_year, self.current_month)
        for week in cal:
            week_frame = tk.Frame(self.cal_frame)
            week_frame.pack()
            for day in week:
                if day != 0:
                    day_str = f"{self.current_year}-{self.current_month:02d}-{day:02d}"
                    if day_str in self.events:
                        day_button = tk.Button(week_frame, text=day, bg='red', command=lambda d=day: self.view_day(d))
                    else:
                        day_button = tk.Button(week_frame, text=day, command=lambda d=day: self.view_day(d))
                    day_button.pack(side=tk.LEFT, padx=5, pady=5)
                else:
                    tk.Label(week_frame, text="").pack(side=tk.LEFT, padx=5, pady=5)

    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.draw_calendar()

    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.draw_calendar()

    def view_day(self, day):
        day_str = f"{self.current_year}-{self.current_month:02d}-{day:02d}"
        events = self.events.get(day_str, [])
        event_list = "\n".join(events) if events else "Brak wydarzeń"
        top = tk.Toplevel(self.root)
        top.title(f"Wydarzenia z dnia {day_str}")

        event_label = tk.Label(top, text=event_list)
        event_label.pack()

        add_event_button = tk.Button(top, text="Dodaj wydarzenie", command=lambda: self.add_event(day_str, top))
        add_event_button.pack()

    def add_event(self, day_str, top):
        event = simpledialog.askstring("Dodaj wydarzenie", "Wprowadź nazwę wydarzenia:", parent=top)
        if event:
            if day_str in self.events:
                self.events[day_str].append(event)
            else:
                self.events[day_str] = [event]
            top.destroy()
            self.draw_calendar()

if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()
