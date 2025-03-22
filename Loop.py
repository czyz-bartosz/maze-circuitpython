class _Loop:
    tasks = []
    def add(self, task):
        self.tasks.append(task)
    def remove(self, task):
        self.tasks.remove(task)
    def run(self):
        for task in self.tasks:
            task()

loop = _Loop()
