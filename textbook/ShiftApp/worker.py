class Worker:
    def __init__(self, worker_id, name, role="Staff"):
        self.__worker_id = worker_id
        self.name = name
        self.role = role

    def get_id(self):
        return self.__worker_id

    def __str__(self):
        return f"[{self.__worker_id}] {self.name} ({self.role})"
