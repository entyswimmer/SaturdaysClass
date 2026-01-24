from worker import Worker
from shift import Shift

def main():
    # 1. Create worker instances
    worker1 = Worker(101, "Tanaka", "Manager")
    worker2 = Worker(102, "Sato", "Staff")
    worker3 = Worker(103, "Suzuki", "Staff")

    # 2. Create shift instances
    monday_shift = Shift("2024-05-20")
    tuesday_shift = Shift("2024-05-21")

    # 3. Assign workers to shifts
    print("--- Assigning Workers ---")
    monday_shift.add_worker(worker1)
    monday_shift.add_worker(worker2)
    
    tuesday_shift.add_worker(worker1)
    tuesday_shift.add_worker(worker3)

    # 4. Display shift information
    monday_shift.show_shift_info()
    tuesday_shift.show_shift_info()

    # 5. Remove a worker and show updated info
    print("\n--- Updating Monday Shift ---")
    monday_shift.remove_worker(102)
    monday_shift.show_shift_info()

if __name__ == "__main__":
    main()
