import math
import statistics
import json
import os
from datetime import datetime


def log_action(func):
    def wrapper(*args, **kwargs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {func.__name__} called")
        result = func(*args, **kwargs)
        return result
    return wrapper


patients = []
FILE_PATH = "patients.txt"


@log_action
def add_patient(**kwargs):
    patient = {
        "id":      len(patients) + 1,
        "name":    kwargs.get("name",    "Unknown"),
        "age":     kwargs.get("age",     0),
        "disease": kwargs.get("disease", "Not specified"),
        "doctor":  kwargs.get("doctor",  "Not assigned"),
        "ward":    kwargs.get("ward",    "General"),
    }
    patients.append(patient)
    print(f"Patient '{patient['name']}' added with ID {patient['id']}.")


@log_action
def view_patients():
    if not patients:
        print("No patients found.")
        return

    id_name_map = {p["id"]: p["name"] for p in patients}
    print(f"\nID to Name map: {id_name_map}\n")

    print(f"{'ID':<5} {'Name':<20} {'Age':<5} {'Disease':<20} {'Doctor':<15} {'Ward'}")
    for p in patients:
        print(f"{p['id']:<5} {p['name']:<20} {p['age']:<5} {p['disease']:<20} {p['doctor']:<15} {p['ward']}")


@log_action
def search_patient(name):
    name_lower = name.lower()
    results = list(filter(lambda p: name_lower in p["name"].lower(), patients))

    if results:
        print(f"\nFound {len(results)} patient(s) matching '{name}':")
        for p in results:
            print(f"  ID {p['id']} | {p['name']} | Age {p['age']} | {p['disease']}")
    else:
        print(f"No patients found matching '{name}'.")
    return results


@log_action
def filter_by_disease(disease):
    disease_lower = disease.lower()
    results = list(filter(lambda p: disease_lower in p["disease"].lower(), patients))

    print(f"\nPatients with disease matching '{disease}':")
    if results:
        for p in results:
            print(f"  {p['name']} (ID {p['id']}) - {p['disease']}")
    else:
        print("  None found.")
    return results


def patient_queue():
    for patient in patients:
        yield patient


@log_action
def show_queue():
    print("\nPatient Queue:")
    queue = patient_queue()
    for i, p in enumerate(queue, start=1):
        print(f"  {i}. {p['name']} - {p['disease']}")


@log_action
def show_stats():
    if len(patients) < 2:
        print("Need at least 2 patients for statistics.")
        return

    ages = [p["age"] for p in patients]

    avg      = statistics.mean(ages)
    median   = statistics.median(ages)
    stdev    = statistics.stdev(ages)
    oldest   = max(ages)
    youngest = min(ages)
    avg_ceil = math.ceil(avg)

    print(f"\nPatient Age Statistics")
    print(f"Total patients : {len(patients)}")
    print(f"Average age    : {avg:.1f}  (rounded up: {avg_ceil})")
    print(f"Median age     : {median}")
    print(f"Std deviation  : {stdev:.2f}")
    print(f"Oldest         : {oldest}")
    print(f"Youngest       : {youngest}")


@log_action
def save_to_file():
    with open(FILE_PATH, "w") as f:
        json.dump(patients, f, indent=4)
    print(f"{len(patients)} patient(s) saved to '{FILE_PATH}'.")


@log_action
def load_from_file():
    global patients
    if not os.path.exists(FILE_PATH):
        print("No saved file found. Starting fresh.")
        return
    with open(FILE_PATH, "r") as f:
        patients = json.load(f)
    print(f"{len(patients)} patient(s) loaded from '{FILE_PATH}'.")


def show_menu():
    print("""
Patient Management System
1. Add Patient
2. View All Patients
3. Search Patient by Name
4. Filter by Disease
5. Show Patient Queue
6. Show Age Statistics
7. Save to File
8. Load from File
0. Exit""")


def main():
    print("Welcome to the Patient Management System")
    load_from_file()

    while True:
        show_menu()
        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            print("\nAdd New Patient")
            name    = input("Name    : ").strip()
            age_str = input("Age     : ").strip()
            disease = input("Disease : ").strip()
            doctor  = input("Doctor  (press Enter to skip): ").strip()
            ward    = input("Ward    (press Enter to skip): ").strip()

            try:
                age = int(age_str)
            except ValueError:
                print("Invalid age. Please enter a number.")
                continue

            kwargs = {"name": name, "age": age, "disease": disease}
            if doctor:
                kwargs["doctor"] = doctor
            if ward:
                kwargs["ward"] = ward

            add_patient(**kwargs)

        elif choice == "2":
            view_patients()

        elif choice == "3":
            name = input("Enter name to search: ").strip()
            search_patient(name)

        elif choice == "4":
            disease = input("Enter disease to filter: ").strip()
            filter_by_disease(disease)

        elif choice == "5":
            show_queue()

        elif choice == "6":
            show_stats()

        elif choice == "7":
            save_to_file()

        elif choice == "8":
            load_from_file()

        elif choice == "0":
            save_to_file()
            print("\nGoodbye. Data saved.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()