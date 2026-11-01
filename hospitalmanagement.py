"""
Smart Hospital Management System
"""

from abc import ABC, abstractmethod
from datetime import datetime


# ======================================================================
# STEP 1: Abstract class
# ======================================================================
class HospitalService(ABC):
    """Any class that inherits from this MUST implement process_payment.""" # This is a docstring
    # It 
    # is used to document a class, function, or method:

    @abstractmethod
    def process_payment(self, amount):
        pass # creating a function place holder without a code


# ======================================================================
# STEP 2: Patient class (inherits from HospitalService)
# ======================================================================
class Patient(HospitalService):
    def __init__(self, name, patient_id, phone, age, balance):
        self.name = name
        self.patient_id = patient_id
        self.phone = phone
        self.age = age
        self.__balance = balance  # private attribute (double underscore)

    @staticmethod
    def _is_valid_amount(amount):
        """An amount is valid if it is a number greater than zero."""
        return isinstance(amount, (int, float)) and not isinstance(amount, bool) and amount > 0

    @abstractmethod
    def patient_type(self):
        pass

    def display_details(self):
        print(f"  ID: {self.patient_id} | Name: {self.name} | Phone: {self.phone} | "
              f"Age: {self.age} | Type: {self.patient_type()} | "
              f"Balance: Ksh {self.__balance:,.2f}")

    def check_balance(self):
        return self.__balance

    def deposit(self, amount):
        if not self._is_valid_amount(amount):
            print("Deposit failed: amount must be greater than zero.")
            return False
        self.__balance += amount
        print(f"Deposit successful. New balance: Ksh {self.__balance:,.2f}")
        return True

    def withdraw(self, amount):
        if not self._is_valid_amount(amount):
            print("Withdrawal failed: amount must be greater than zero.")
            return False
        if amount > self.__balance:
            print(f"Withdrawal failed: insufficient funds (balance Ksh {self.__balance:,.2f}).")
            return False
        self.__balance -= amount
        print(f"Withdrawal successful. New balance: Ksh {self.__balance:,.2f}")
        return True


# ======================================================================
# STEP 3: Doctor class
# ======================================================================
class Doctor:
    def __init__(self, name, doctor_id, specialization, consultation_fee):
        self.name = name
        self.doctor_id = doctor_id
        self.specialization = specialization
        self.consultation_fee = consultation_fee

    def display_info(self):
        print(f"  ID: {self.doctor_id} | Dr. {self.name} | "
              f"Specialization: {self.specialization} | "
              f"Fee: Ksh {self.consultation_fee:,.2f}")


# ======================================================================
# STEP 4: Inheritance - Outpatient and Inpatient (different payments)
# ======================================================================
class Outpatient(Patient):
    SERVICE_FEE = 100

    def patient_type(self):
        return "Outpatient Patient"

    def process_payment(self, amount):
        if not self._is_valid_amount(amount):
            print("Payment failed: invalid amount.")
            return False
        total = amount + self.SERVICE_FEE
        if total > self.check_balance():
            print(f"Payment failed: total Ksh {total:,.2f} (includes Ksh {self.SERVICE_FEE} "
                  f"service fee) exceeds balance.")
            return False
        self.withdraw(total)  # reuse withdraw() instead of touching the private balance
        print(f"Outpatient payment of Ksh {total:,.2f} processed "
              f"(Ksh {amount:,.2f} + Ksh {self.SERVICE_FEE} service fee).")
        return True


class Inpatient(Patient):
    SERVICE_FEE = 200

    def patient_type(self):
        return "Inpatient Patient"

    def process_payment(self, amount):
        if not self._is_valid_amount(amount):
            print("Payment failed: invalid amount.")
            return False
        total = amount + self.SERVICE_FEE
        if total > self.check_balance():
            print(f"Payment failed: total Ksh {total:,.2f} (includes Ksh {self.SERVICE_FEE} "
                  f"service fee) exceeds balance.")
            return False
        self.withdraw(total)
        print(f"Inpatient payment of Ksh {total:,.2f} processed "
              f"(Ksh {amount:,.2f} + Ksh {self.SERVICE_FEE} service fee).")
        return True


# ======================================================================
# STEP 5: Appointment class
# ======================================================================
class Appointment:
    _next_id = 1  # class-level counter so every appointment gets a unique number

    def __init__(self, patient, doctor, date, time):
        self.appointment_id = Appointment._next_id
        Appointment._next_id += 1
        self.patient = patient
        self.doctor = doctor
        self.date = date
        self.time = time
        self.status = "Pending"

    def display_details(self):
        print(f"  Appointment #{self.appointment_id} | Patient: {self.patient.name} "
              f"({self.patient.patient_id}) | Doctor: Dr. {self.doctor.name} | "
              f"{self.date} at {self.time} | Status: {self.status}")

    def confirm(self):
        if self.status == "Cancelled":
            print("Cannot confirm a cancelled appointment.")
            return False
        self.status = "Confirmed"
        print(f"Appointment #{self.appointment_id} confirmed.")
        return True

    def cancel(self):
        if self.status == "Cancelled":
            print("This appointment is already cancelled.")
            return False
        self.status = "Cancelled"
        print(f"Appointment #{self.appointment_id} cancelled.")
        return True


# ======================================================================
# STEP 6: Lists to store records
# ======================================================================
patients = []
doctors = []
appointments = []


# ======================================================================
# Input helpers (try / except for invalid input)
# ======================================================================
def get_number(prompt):
    """Keep asking until the user types a valid number."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a whole number.")


def get_text(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty.")


# ======================================================================
# STEP 8: Reusable functions (with loops from STEP 7 inside them)
# ======================================================================
def find_patient(patient_id):
    """Loop through the patients list and return the match (or None)."""
    for p in patients:
        if p.patient_id == patient_id:
            return p
    return None


def find_doctor(doctor_id):
    for d in doctors:
        if d.doctor_id == doctor_id:
            return d
    return None


def find_appointment(appointment_id):
    for a in appointments:
        if a.appointment_id == appointment_id:
            return a
    return None


def register_patient():
    print("\n--- Register Patient ---")
    patient_id = get_text("Patient ID: ").upper()
    if find_patient(patient_id) is not None:  # prevent duplicate IDs
        print(f"Registration failed: patient ID '{patient_id}' already exists.")
        return

    name = get_text("Full name: ")
    phone = get_text("Phone number: ")

    age = get_int("Age: ")
    if age <= 0 or age > 120:
        print("Registration failed: age must be between 1 and 120.")
        return

    balance = get_number("Opening account balance (Ksh): ")
    if balance < 0:
        print("Registration failed: balance cannot be negative.")
        return

    print("Patient type:  1. Outpatient   2. Inpatient")
    choice = get_text("Choose 1 or 2: ")
    if choice == "1":
        patient = Outpatient(name, patient_id, phone, age, balance)
    elif choice == "2":
        patient = Inpatient(name, patient_id, phone, age, balance)
    else:
        print("Registration failed: invalid patient type.")
        return

    patients.append(patient)
    print(f"Success: {name} registered as {patient.patient_type()}.")


def register_doctor():
    print("\n--- Register Doctor ---")
    doctor_id = get_text("Doctor ID: ").upper()
    if find_doctor(doctor_id) is not None:
        print(f"Registration failed: doctor ID '{doctor_id}' already exists.")
        return

    name = get_text("Doctor's name: ")
    specialization = get_text("Specialization: ")
    fee = get_number("Consultation fee (Ksh): ")
    if fee <= 0:
        print("Registration failed: fee must be greater than zero.")
        return

    doctors.append(Doctor(name, doctor_id, specialization, fee))
    print(f"Success: Dr. {name} registered.")


def book_appointment():
    print("\n--- Book Appointment ---")
    patient = find_patient(get_text("Patient ID: ").upper())
    if patient is None:
        print("Booking failed: patient does not exist.")
        return

    doctor = find_doctor(get_text("Doctor ID: ").upper())
    if doctor is None:
        print("Booking failed: doctor does not exist.")
        return

    date = get_text("Date (YYYY-MM-DD): ")
    time = get_text("Time (HH:MM, 24-hour): ")
    try:
        datetime.strptime(date, "%Y-%m-%d")
        datetime.strptime(time, "%H:%M")
    except ValueError:
        print("Booking failed: use the formats YYYY-MM-DD and HH:MM.")
        return

    # Don't let a doctor be double-booked
    for a in appointments:
        if (a.doctor.doctor_id == doctor.doctor_id and a.date == date
                and a.time == time and a.status != "Cancelled"):
            print("Booking failed: that doctor already has an appointment at that time.")
            return

    appointment = Appointment(patient, doctor, date, time)
    appointments.append(appointment)
    appointment.confirm()
    print("Success: appointment booked.")


def display_patients():
    print("\n--- Registered Patients ---")
    if not patients:
        print("No patients registered yet.")
        return
    for p in patients:
        p.display_details()


def display_doctors():
    print("\n--- Registered Doctors ---")
    if not doctors:
        print("No doctors registered yet.")
        return
    for d in doctors:
        d.display_info()


def display_appointments():
    print("\n--- Appointments ---")
    if not appointments:
        print("No appointments booked yet.")
        return
    for a in appointments:
        a.display_details()


def search_patient():
    print("\n--- Search Patient ---")
    patient_id = get_text("Enter patient ID to search: ").upper()
    patient = find_patient(patient_id)
    if patient is None:
        print(f"No patient found with ID '{patient_id}'.")
    else:
        print("Patient found:")
        patient.display_details()


# ----- Functions backing the remaining menu options -----
def deposit_money():
    print("\n--- Deposit Money ---")
    patient = find_patient(get_text("Patient ID: ").upper())
    if patient is None:
        print("Deposit failed: patient not found.")
        return
    patient.deposit(get_number("Amount to deposit (Ksh): "))


def withdraw_money():
    print("\n--- Withdraw Money ---")
    patient = find_patient(get_text("Patient ID: ").upper())
    if patient is None:
        print("Withdrawal failed: patient not found.")
        return
    patient.withdraw(get_number("Amount to withdraw (Ksh): "))


def process_patient_payment():
    print("\n--- Process Patient Payment ---")
    patient = find_patient(get_text("Patient ID: ").upper())
    if patient is None:
        print("Payment failed: patient not found.")
        return
    amount = get_number("Consultation amount (Ksh): ")
    if amount <= 0:
        print("Payment failed: amount must be greater than zero.")
        return
    patient.process_payment(amount)  # Outpatient or Inpatient version runs automatically


def check_patient_balance():
    print("\n--- Check Balance ---")
    patient = find_patient(get_text("Patient ID: ").upper())
    if patient is None:
        print("Patient not found.")
        return
    print(f"{patient.name}'s balance: Ksh {patient.check_balance():,.2f}")


def cancel_appointment():
    print("\n--- Cancel Appointment ---")
    appointment = find_appointment(get_int("Appointment number: "))
    if appointment is None:
        print("Cancellation failed: appointment not found.")
        return
    appointment.cancel()


# ======================================================================
# STEP 9: Polymorphism demonstration
# ======================================================================
def demonstrate_polymorphism():
    print("\n" + "=" * 40)
    print("   POLYMORPHISM DEMO (temporary objects)")
    print("=" * 40)
    demo_patients = [
        Outpatient("Demo Outpatient", "DEMO1", "0700000000", 30, 1000),
        Inpatient("Demo Inpatient", "DEMO2", "0711111111", 45, 1000),
    ]
    # Same method names, different behaviour for each object type
    for p in demo_patients:
        print(f"\n{p.patient_type()}:")
        p.process_payment(500)  # outpatient pays 600, inpatient pays 700
    print("=" * 40 + "\n")


# ======================================================================
# STEP 10: Main menu (STEP 7: while loop + if/elif/else)
# ======================================================================
def show_menu():
    print("\n" + "=" * 40)
    print("       SMART HOSPITAL MANAGEMENT")
    print("=" * 40)
    print("1. Register Patient")
    print("2. Register Doctor")
    print("3. Display All Patients")
    print("4. Display All Doctors")
    print("5. Book Appointment")
    print("6. Display All Appointments")
    print("7. Search Patient")
    print("8. Deposit Money")
    print("9. Withdraw Money")
    print("10. Process Patient Payment")
    print("11. Check Patient Balance")
    print("12. Cancel Appointment")
    print("13. Exit")


def main():
    demonstrate_polymorphism()

    while True:  # keeps running until the user chooses Exit
        show_menu()
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number from 1 to 13.")
            continue

        if choice == 1:
            register_patient()
        elif choice == 2:
            register_doctor()
        elif choice == 3:
            display_patients()
        elif choice == 4:
            display_doctors()
        elif choice == 5:
            book_appointment()
        elif choice == 6:
            display_appointments()
        elif choice == 7:
            search_patient()
        elif choice == 8:
            deposit_money()
        elif choice == 9:
            withdraw_money()
        elif choice == 10:
            process_patient_payment()
        elif choice == 11:
            check_patient_balance()
        elif choice == 12:
            cancel_appointment()
        elif choice == 13:
            print("Thank you for using Smart Hospital Management. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a number from 1 to 13.")


if __name__ == "__main__":
    main()