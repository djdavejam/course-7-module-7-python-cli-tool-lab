class Task:
    """Represents a task with a title and completion status."""
    
    def __init__(self, title):
        self.title = title
        self.completed = False

    def complete(self):
        """Mark the task as completed and print confirmation."""
        self.completed = True
        print(f"✅ Task '{self.title}' completed.")

    def __str__(self):
        status = "✅" if self.completed else "⭕"
        return f"{status} {self.title}"


class User:
    """Represents a user with a name and a list of tasks."""
    
    def __init__(self, name):
        self.name = name
        self.tasks = []

    def add_task(self, task):
        """Add a task to the user's task list."""
        self.tasks.append(task)
        print(f"📌 Task '{task.title}' added to {self.name}.")

    def get_task_by_title(self, title):
        """Search for a task by its title in the user's task list."""
        for task in self.tasks:
            if task.title == title:
                return task
        return None

    def list_tasks(self):
        """Display all tasks for the user."""
        if not self.tasks:
            print(f"{self.name} has no tasks.")
        else:
            print(f"\n{self.name}'s tasks:")
            for i, task in enumerate(self.tasks, 1):
                print(f"  {i}. {task}")

    def __str__(self):
        return f"User: {self.name} ({len(self.tasks)} tasks)"