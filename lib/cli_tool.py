"""
Task Manager CLI Tool

A command-line interface for managing tasks using object-oriented programming.
Supports adding tasks to users and marking tasks as complete.
"""

import argparse
import sys
import os

# Add the lib directory to the Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from lib.models import Task, User

# Global dictionary to store users and their tasks
users = {}


def add_task(args):
    """Add a new task for a user."""
    # Get existing user or create new one
    user = users.get(args.user)
    if not user:
        user = User(args.user)
        users[args.user] = user
    
    # Create and add the task
    task = Task(args.title)
    user.add_task(task)


def complete_task(args):
    """Mark a task as complete for a user."""
    user = users.get(args.user)
    if not user:
        print(f"❌ User '{args.user}' not found.")
        return
    
    task = user.get_task_by_title(args.title)
    if not task:
        print(f"❌ Task '{args.title}' not found for {args.user}.")
        return
    
    if task.completed:
        print(f"ℹ️  Task '{args.title}' is already completed.")
    else:
        task.complete()


def list_tasks(args):
    """List all tasks for a user."""
    user = users.get(args.user)
    if not user:
        print(f"❌ User '{args.user}' not found.")
        return
    
    user.list_tasks()


def list_users(args):
    """List all users in the system."""
    if not users:
        print("No users found.")
        return
    
    print("\nAll users:")
    for username, user in users.items():
        print(f"  • {user}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Task Manager CLI - Manage tasks for users",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s add-task Alice "Write unit tests"
  %(prog)s complete-task Alice "Write unit tests"
  %(prog)s list-tasks Alice
  %(prog)s list-users
        """
    )
    
    subparsers = parser.add_subparsers(
        dest='command',
        help='Available commands'
    )

    # Subparser for adding tasks
    add_parser = subparsers.add_parser(
        "add-task", 
        help="Add a new task for a user"
    )
    add_parser.add_argument("user", help="Username")
    add_parser.add_argument("title", help="Task title")
    add_parser.set_defaults(func=add_task)

    # Subparser for completing tasks
    complete_parser = subparsers.add_parser(
        "complete-task", 
        help="Mark a task as complete"
    )
    complete_parser.add_argument("user", help="Username")
    complete_parser.add_argument("title", help="Task title")
    complete_parser.set_defaults(func=complete_task)

    # Subparser for listing tasks
    list_parser = subparsers.add_parser(
        "list-tasks", 
        help="List all tasks for a user"
    )
    list_parser.add_argument("user", help="Username")
    list_parser.set_defaults(func=list_tasks)

    # Subparser for listing users
    users_parser = subparsers.add_parser(
        "list-users", 
        help="List all users"
    )
    users_parser.set_defaults(func=list_users)

    # Parse arguments and execute appropriate function
    args = parser.parse_args()
    
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
