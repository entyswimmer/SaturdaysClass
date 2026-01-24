class Shift:
    def __init__(self, date):
        self.date = date
        self.assigned_workers = []

    def add_worker(self, worker):
        if worker not in self.assigned_workers:
            self.assigned_workers.append(worker)
            print(f"{worker.name} を {self.date} のシフトに入れました。")
        else:
            print(f"{worker.name} は既にシフトに入っています。")

    def remove_worker(self, worker_id):
        initial_count = len(self.assigned_workers)
        self.assigned_workers = [w for w in self.assigned_workers if w.get_id() != worker_id]
        
        if len(self.assigned_workers) < initial_count:
            print(f"{worker_id} を {self.date} から消去しました。")
        else:
            print(f" {worker_id} はシフトに見つかりませんでした。")

    def show_shift_info(self):
        print(f"\n--- 日付: {self.date} ---")
        if not self.assigned_workers:
            print("シフトに誰も割り当てられていません")
        for worker in self.assigned_workers:
            print(worker)
