import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

class RailwaySystem:
    def __init__(self, root):
        self.root = root
        self.ticket_price = 50  # $25 for up and $25 for down
        self.setup_data()
        self.setup_ui()

    def setup_data(self):
        self.train_schedule = {
            '09:00-up': {'available': 480, 'earned': 0, 'passengers': 0},
            '11:00-up': {'available': 480, 'earned': 0, 'passengers': 0},
            '13:00-up': {'available': 480, 'earned': 0, 'passengers': 0},
            '15:00-up': {'available': 480, 'earned': 0, 'passengers': 0},
            '10:00-down': {'available': 480, 'earned': 0, 'passengers': 0},
            '12:00-down': {'available': 480, 'earned': 0, 'passengers': 0},
            '14:00-down': {'available': 480, 'earned': 0, 'passengers': 0},
            '16:00-down': {'available': 560, 'earned': 0, 'passengers': 0},
        }

    def setup_ui(self):
        self.root.title("Electric Mountain Railway Booking System")
        ttk.Style().theme_use('clam')

        self.labels = {}
        row = 0
        for time, info in self.train_schedule.items():
            ttk.Label(self.root, text=f"Train at {time}", font=('Helvetica', 10)).grid(row=row, column=0, padx=10, pady=10)
            availability_label = ttk.Label(self.root, text=f"Available Seats: {info['available']}", font=('Helvetica', 10))
            availability_label.grid(row=row, column=1, padx=10, pady=10)
            self.labels[time] = availability_label
            ttk.Button(self.root, text="Book Ticket", command=lambda t=time: self.book_ticket(t)).grid(row=row, column=2, padx=10, pady=10)
            row += 1

        ttk.Label(self.root, text=f"Ticket Price: ${self.ticket_price} (Return Journey)", font=('Helvetica', 10)).grid(row=row, column=0, columnspan=3, pady=10)

    def book_ticket(self, time):
        num_passengers = simpledialog.askinteger("Number of Passengers", "Enter number of passengers:", minvalue=1, maxvalue=80)
        if num_passengers is None:
            return

        return_time = self.get_return_time(time)
        if not return_time:
            messagebox.showerror("Error", "Return journey not found.")
            return

        if not self.check_availability(time, return_time, num_passengers):
            return

        total_cost, discount_percentage = self.calculate_cost(num_passengers)

        confirmation = messagebox.askyesno("Confirm Booking", f"Total cost: ${total_cost}\nDiscount: {discount_percentage:.2f}%\nProceed with booking?")
        if not confirmation:
            return

        self.update_journey(time, num_passengers, total_cost)
        self.update_journey(return_time, num_passengers, total_cost)
        self.update_display(time)
        self.update_display(return_time)

    def get_return_time(self, time):
        hour, direction = time.split('-')
        hour = int(hour.split(':')[0])
        return_time_hour = hour + 1 if direction == 'up' else hour - 1
        return f"{return_time_hour:02d}:00-down" if direction == 'up' else f"{return_time_hour:02d}:00-up"

    def check_availability(self, time, return_time, num_passengers):
        if self.train_schedule[time]['available'] < num_passengers or self.train_schedule[return_time]['available'] < num_passengers:
            messagebox.showerror("Error", "Not enough seats available for both journeys.")
            return False
        return True

    def calculate_cost(self, num_passengers):
        discount = num_passengers // 10
        total_cost = (num_passengers - discount) * self.ticket_price
        discount_percentage = (discount / num_passengers) * 100 if num_passengers else 0
        return total_cost, discount_percentage

    def update_journey(self, time, num_passengers, total_cost):
        self.train_schedule[time]['available'] -= num_passengers
        self.train_schedule[time]['earned'] += total_cost
        self.train_schedule[time]['passengers'] += num_passengers

    def update_display(self, time):
        availability = self.train_schedule[time]['available']
        text = 'Closed' if availability == 0 else f"Available Seats: {availability}"
        self.labels[time].config(text=text)

    def show_totals(self):
        total_passengers = 0
        total_earnings = 0
        most_passengers = 0
        busiest_journey = None

        print("\nJourney Report for the Day:")
        for time, info in self.train_schedule.items():
            print(f"Train {time}: Total Passengers: {info['passengers']}, Total Earnings: ${info['earned']}")
            total_passengers += info['passengers']
            total_earnings += info['earned']
            if info['passengers'] > most_passengers:
                most_passengers = info['passengers']
                busiest_journey = time

        print(f"\nTotal Passengers for the Day: {total_passengers}")
        print(f"Total Earnings for the Day: ${total_earnings}")

        if busiest_journey:
            print(f"Busiest Journey: {busiest_journey} with {most_passengers} passengers")
        else:
            print("No journeys were made today.")

def main():
    root = tk.Tk()
    app = RailwaySystem(root)
    root.protocol("WM_DELETE_WINDOW", lambda: [app.show_totals(), root.destroy()])
    root.mainloop()

if __name__ == "__main__":
    main()
