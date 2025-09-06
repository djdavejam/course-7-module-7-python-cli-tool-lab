"""
Test suite for the Task Manager CLI Tool

Tests both the CLI functionality and the underlying object models.
"""

import subprocess
import tempfile
import os
import sys
import unittest
from io import StringIO
from contextlib import redirect_stdout

# Add the lib directory to the Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from lib.models import Task, User


def run_cli_command(command_args):
    """Helper function to run CLI command and capture output."""
    # Get the path to cli_tool.py
    cli_path = os.path.join(os.path.dirname(__file__), '..', 'lib', 'cli_tool.py')
    
    # Run the command
    result = subprocess.run(
        ["python", cli_path] + command_args, 
        capture_output=True, 
        text=True
    )
    
    return result


class TestTaskModel(unittest.TestCase):
    """Test the Task class functionality."""
    
    def test_task_creation(self):
        """Test creating a new task."""
        task = Task("Write unit tests")
        self.assertEqual(task.title, "Write unit tests")
        self.assertFalse(task.completed)
    
    def test_task_completion(self):
        """Test marking a task as complete."""
        task = Task("Test task")
        
        # Capture the print output
        output = StringIO()
        with redirect_stdout(output):
            task.complete()
        
        self.assertTrue(task.completed)
        self.assertIn("Task 'Test task' completed", output.getvalue())
    
    def test_task_string_representation(self):
        """Test task string representation."""
        incomplete_task = Task("Incomplete task")
        complete_task = Task("Complete task")
        
        # Redirect stdout to avoid seeing the completion message
        with redirect_stdout(StringIO()):
            complete_task.complete()
        
        self.assertIn("⭕", str(incomplete_task))
        self.assertIn("✅", str(complete_task))


class TestUserModel(unittest.TestCase):
    """Test the User class functionality."""
    
    def test_user_creation(self):
        """Test creating a new user."""
        user = User("Alice")
        self.assertEqual(user.name, "Alice")
        self.assertEqual(len(user.tasks), 0)
    
    def test_add_task_to_user(self):
        """Test adding a task to a user."""
        user = User("Bob")
        task = Task("Complete project")
        
        # Capture the print output
        output = StringIO()
        with redirect_stdout(output):
            user.add_task(task)
        
        self.assertEqual(len(user.tasks), 1)
        self.assertEqual(user.tasks[0], task)
        self.assertIn("Task 'Complete project' added to Bob", output.getvalue())
    
    def test_get_task_by_title_found(self):
        """Test finding a task by title."""
        user = User("Charlie")
        task1 = Task("Task 1")
        task2 = Task("Task 2")
        
        with redirect_stdout(StringIO()):
            user.add_task(task1)
            user.add_task(task2)
        
        found_task = user.get_task_by_title("Task 2")
        self.assertEqual(found_task, task2)
    
    def test_get_task_by_title_not_found(self):
        """Test searching for a non-existent task."""
        user = User("David")
        task = Task("Existing task")
        
        with redirect_stdout(StringIO()):
            user.add_task(task)
        
        found_task = user.get_task_by_title("Non-existent task")
        self.assertIsNone(found_task)
    
    def test_list_tasks_empty(self):
        """Test listing tasks when user has no tasks."""
        user = User("Emma")
        
        output = StringIO()
        with redirect_stdout(output):
            user.list_tasks()
        
        self.assertIn("Emma has no tasks", output.getvalue())
    
    def test_list_tasks_with_tasks(self):
        """Test listing tasks when user has tasks."""
        user = User("Frank")
        task1 = Task("Task 1")
        task2 = Task("Task 2")
        
        with redirect_stdout(StringIO()):
            user.add_task(task1)
            user.add_task(task2)
        
        output = StringIO()
        with redirect_stdout(output):
            user.list_tasks()
        
        output_text = output.getvalue()
        self.assertIn("Frank's tasks:", output_text)
        self.assertIn("1. ⭕ Task 1", output_text)
        self.assertIn("2. ⭕ Task 2", output_text)


class TestCLITool(unittest.TestCase):
    """Test the CLI tool functionality."""
    
    def test_add_task_command(self):
        """Test the add-task command."""
        result = run_cli_command(["add-task", "Alice", "Submit report"])
        
        self.assertEqual(result.returncode, 0)
        self.assertIn("Task 'Submit report' added to Alice", result.stdout)
    
    def test_complete_task_command(self):
        """Test the complete-task command in isolation."""
        # Create a simpler test that doesn't rely on subprocess
        # Import the modules directly and test the functionality
        from lib.models import Task, User
        from lib.cli_tool import complete_task
        import lib.cli_tool
        
        # Set up test data
        users = {}
        user = User("Bob")
        users["Bob"] = user
        
        # Capture output for add_task
        output = StringIO()
        with redirect_stdout(output):
            task = Task("Finish lab")
            user.add_task(task)
        
        # Create args object to simulate CLI arguments
        class Args:
            def __init__(self, user, title):
                self.user = user
                self.title = title
        
        # Patch the users dictionary in the cli_tool module
        original_users = lib.cli_tool.users
        lib.cli_tool.users = users
        
        try:
            # Test completing the task
            args = Args("Bob", "Finish lab")
            
            # Capture the output
            output = StringIO()
            with redirect_stdout(output):
                complete_task(args)
            
            # Check the output
            output_text = output.getvalue()
            self.assertIn("Task 'Finish lab' completed", output_text)
            
            # Verify the task is actually completed
            self.assertTrue(user.tasks[0].completed)
            
        finally:
            # Restore original users dictionary
            lib.cli_tool.users = original_users
    
    def test_help_command(self):
        """Test the help functionality."""
        result = run_cli_command(["--help"])
        
        self.assertEqual(result.returncode, 0)
        self.assertIn("Task Manager CLI", result.stdout)
        self.assertIn("add-task", result.stdout)
        self.assertIn("complete-task", result.stdout)
    
    def test_no_command_shows_help(self):
        """Test that running without arguments shows help."""
        result = run_cli_command([])
        
        self.assertEqual(result.returncode, 0)
        self.assertIn("usage:", result.stdout)


def run_integration_test():
    """Run a complete integration test demonstrating the workflow."""
    print("=" * 50)
    print("INTEGRATION TEST: Task Manager CLI Workflow")
    print("=" * 50)
    
    # Test adding tasks using the CLI
    print("\n1. Adding tasks...")
    result1 = run_cli_command(["add-task", "Alice", "Write unit tests"])
    print("Command:", "add-task Alice 'Write unit tests'")
    print("Output:", result1.stdout.strip())
    
    result2 = run_cli_command(["add-task", "Alice", "Review code"])
    print("Command:", "add-task Alice 'Review code'")
    print("Output:", result2.stdout.strip())
    
    result3 = run_cli_command(["add-task", "Bob", "Deploy application"])
    print("Command:", "add-task Bob 'Deploy application'")
    print("Output:", result3.stdout.strip())
    
    # Test direct model functionality for task completion workflow
    print("\n2. Testing task completion workflow...")
    print("Setting up test environment...")
    
    # Import and set up the models directly
    from lib.models import Task, User
    from lib.cli_tool import complete_task, list_tasks, list_users
    import lib.cli_tool
    
    # Create users and tasks to simulate the CLI state
    users = {}
    
    # Add Alice with tasks
    alice = User("Alice")
    users["Alice"] = alice
    print("Creating Alice with tasks...")
    with StringIO() as output:
        with redirect_stdout(output):
            alice.add_task(Task("Write unit tests"))
            alice.add_task(Task("Review code"))
    
    # Add Bob with tasks  
    bob = User("Bob")
    users["Bob"] = bob
    print("Creating Bob with tasks...")
    with StringIO() as output:
        with redirect_stdout(output):
            bob.add_task(Task("Deploy application"))
    
    # Simulate CLI arguments
    class Args:
        def __init__(self, user=None, title=None):
            self.user = user
            self.title = title
    
    # Temporarily patch the users dictionary
    original_users = lib.cli_tool.users
    lib.cli_tool.users = users
    
    try:
        # Test completing a task
        print("\nCompleting Alice's 'Write unit tests' task:")
        complete_task(Args("Alice", "Write unit tests"))
        
        print("\nListing Alice's tasks:")
        list_tasks(Args("Alice"))
        
        print("\nListing all users:")
        list_users(Args())
        
    finally:
        # Restore original users dictionary
        lib.cli_tool.users = original_users
    
    print("\n" + "=" * 50)
    print("INTEGRATION TEST COMPLETE")
    print("=" * 50)


if __name__ == "__main__":
    # Run the unit tests
    print("Running unit tests...")
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # Run the integration test
    print("\n" + "=" * 50)
    run_integration_test()