import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Initialize SQLite database
conn = sqlite3.connect('railway.db')
c = conn.cursor()

# Create bookings table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS bookings (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             passenger_name TEXT NOT NULL,
             email TEXT NOT NULL,
             train_number TEXT NOT NULL,
             seat_number TEXT NOT NULL
             )''')

# Function to send email
def send_email(to_email, subject, message):
    from_email = 'your_email@example.com'  # Update with your email address
    password = 'your_password'  # Update with your email password

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('smtp.example.com', 587)  # Update with your SMTP server and port
    server.starttls()
    server.login(from_email, password)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()

# Function to book a ticket
def book_ticket(passenger_name, email, train_number, seat_number):
    c.execute('INSERT INTO bookings (passenger_name, email, train_number, seat_number) VALUES (?, ?, ?, ?)',
              (passenger_name, email, train_number, seat_number))
    conn.commit()

    # Send confirmation email
    subject = 'Ticket Booking Confirmation'
    message = f'Dear {passenger_name},\n\nYour ticket has been successfully booked.\nTrain Number: {train_number}\nSeat Number: {seat_number}\n\nThank you for choosing our service.'
    send_email(email, subject, message)

# Main program loop
if __name__ == '__main__':
    while True:
        print("\nWelcome to Railway Ticket Booking System")
        print("1. Book Ticket")
        print("2. Exit")
        choice = input("Enter choice (1/2): ")

        if choice == '1':
            passenger_name = input("Enter passenger name: ")
            email = input("Enter email address: ")
            train_number = input("Enter train number: ")
            seat_number = input("Enter seat number: ")

            book_ticket(passenger_name, email, train_number, seat_number)
            print("Ticket booked successfully!")

        elif choice == '2':
            break

        else:
            print("Invalid choice. Please enter 1 or 2.")

    conn.close()  # Close database connection
