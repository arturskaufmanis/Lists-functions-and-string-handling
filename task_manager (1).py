# task_manager.py - A task management system with user authentication
# This program allows users to register, add tasks, view all tasks, view their own tasks,
# generate reports and display statistics (admin only).
# It uses a file-based approach to store tasks and user information.
# PEP 8 Compliant Version with DD-MM-YYYY date format

import os
from datetime import datetime, date

# Constants
DATETIME_STRING_FORMAT = "%d-%m-%Y"  # Changed from YYYY-MM-DD to DD-MM-YYYY
SEPARATOR_LINE = "_" * 80


def load_tasks():
    """
    Load and parse tasks from tasks.txt file.
    
    Returns:
        list: List of task dictionaries
    """
    task_list = []
    
    try:
        # Return empty list if file doesn't exist or is empty
        if not os.path.exists("tasks.txt") or os.path.getsize("tasks.txt") == 0:
            return []
            
        with open("tasks.txt", 'r') as task_file:
            content = task_file.read()
            
        # Split content by task separator (indicated by multiple underscores)
        task_blocks = content.split("\n" + SEPARATOR_LINE + "\n")
        
        for block in task_blocks:
            if not block.strip():
                continue
                
            # Parse the block into task components
            task = {}
            lines = block.strip().split("\n")
            
            for i, line in enumerate(lines):
                if not line.strip() or line.startswith("_"):
                    continue
                    
                if ": " in line:
                    key, value = line.split(": ", 1)
                    key = key.strip()
                    value = value.strip()
                    
                    if key == "Task":
                        task['title'] = value
                    elif key == "Assigned to":
                        task['username'] = value
                    elif key == "Date Assigned":
                        task['assigned_date'] = datetime.strptime(value, DATETIME_STRING_FORMAT)
                    elif key == "Due Date":
                        task['due_date'] = datetime.strptime(value, DATETIME_STRING_FORMAT)
                    elif key == "Completed":
                        task['completed'] = (value == "Yes")
                    elif key == "Task Description":
                        # The description is on the next line
                        if i + 1 < len(lines):
                            task['description'] = lines[i + 1].strip()
                        else:
                            task['description'] = ""
            
            # Only add if we have all required fields
            if all(key in task for key in ['username', 'title', 'description', 'due_date', 
                                          'assigned_date', 'completed']):
                task_list.append(task)
                
    except Exception as e:
        print(f"Error loading tasks: {e}")
        # If there's an error with the new format, try the old format as fallback
        try:
            with open("tasks.txt", 'r') as task_file:
                task_data = task_file.read().split("\n")
                
            task_list = []
            for t_str in task_data:
                if not t_str.strip():
                    continue
                    
                # Parse task components
                task_components = t_str.split(";")
                if len(task_components) != 6:  # Basic validation
                    continue
                    
                # Create task dictionary in one step
                # Note: This handles the old format which might still be YYYY-MM-DD
                # We'll try both formats to be safe
                task = {
                    'username': task_components[0],
                    'title': task_components[1],
                    'description': task_components[2],
                    'completed': True if task_components[5] == "Yes" else False
                }
                
                # Try the new date format first, fall back to old format if needed
                try:
                    task['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
                except ValueError:
                    task['due_date'] = datetime.strptime(task_components[3], "%Y-%m-%d")
                    
                try:
                    task['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
                except ValueError:
                    task['assigned_date'] = datetime.strptime(task_components[4], "%Y-%m-%d")
                
                task_list.append(task)
        except Exception as e2:
            print(f"Error loading tasks with fallback method: {e2}")
        
    return task_list


def load_users():
    """
    Load users from user.txt file.
    
    Returns:
        dict: Dictionary mapping usernames to passwords
    """
    username_password = {}
    
    try:
        # Create file with default admin account if it doesn't exist
        if not os.path.exists("user.txt"):
            with open("user.txt", "w") as default_file:
                default_file.write("Username: admin\nPassword: password")
        
        with open("user.txt", 'r') as user_file:
            content = user_file.read()
            
        # Try new format first
        user_blocks = content.split("\n\n")
        
        for block in user_blocks:
            if not block.strip():
                continue
                
            lines = block.strip().split("\n")
            username = None
            password = None
            
            for line in lines:
                if line.startswith("Username: "):
                    username = line.replace("Username: ", "", 1).strip()
                elif line.startswith("Password: "):
                    password = line.replace("Password: ", "", 1).strip()
            
            if username and password:
                username_password[username] = password
                
        # If no users found, try old format
        if not username_password:
            with open("user.txt", 'r') as user_file:
                user_data = user_file.read().split("\n")
            
            for user in user_data:
                if not user.strip():
                    continue
                    
                if ";" in user:
                    username, password = user.split(';')
                    username_password[username] = password
                    
    except Exception as e:
        print(f"Error loading users: {e}")
        
    return username_password


def save_tasks(task_list):
    """
    Save tasks to tasks.txt file with perfectly aligned two-column format.
    Uses DD-MM-YYYY date format.
    
    Args:
        task_list (list): List of task dictionaries
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open("tasks.txt", "w") as task_file:
            for i, t in enumerate(task_list):
                if i > 0:
                    task_file.write("\n")
                
                task_file.write(f"{SEPARATOR_LINE}\n")
                # Create consistent column widths with left-aligned labels and left-aligned values
                task_file.write(f"{'Task:':<20}{t['title']}\n")
                task_file.write(f"{'Assigned to:':<20}{t['username']}\n")
                task_file.write(f"{'Date Assigned:':<20}{t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n")
                task_file.write(f"{'Due Date:':<20}{t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n")
                task_file.write(f"{'Completed:':<20}{'Yes' if t['completed'] else 'No'}\n")
                task_file.write(f"{'Task Description:':<20}\n{t['description']}\n")
                task_file.write(f"{SEPARATOR_LINE}")
                
        return True
    except Exception as e:
        print(f"Error saving tasks: {e}")
        return False


def save_users(username_password):
    """
    Save users to user.txt file in a user-friendly format.
    
    Args:
        username_password (dict): Dictionary mapping usernames to passwords
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open("user.txt", "w") as user_file:
            for i, (username, password) in enumerate(username_password.items()):
                if i > 0:
                    user_file.write("\n\n")
                user_file.write(f"Username: {username}\n")
                user_file.write(f"Password: {password}")
        return True
    except Exception as e:
        print(f"Error saving users: {e}")
        return False


def reg_user(username_password):
    """
    Register a new user if username doesn't already exist.
    
    Args:
        username_password (dict): Dictionary mapping usernames to passwords
    """
    new_username = input("New Username: ")
    
    # Check if username already exists
    if new_username in username_password:
        print("Error: Username already exists. Please choose a different username.")
        return
        
    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")

    if new_password != confirm_password:
        print("Passwords do not match")
        return
        
    # Add new user and save
    username_password[new_username] = new_password
    if save_users(username_password):
        print("New user added successfully")


def add_task(username_password, task_list):
    """
    Add a new task assigned to a valid user.
    Uses DD-MM-YYYY date format for input.
    
    Args:
        username_password (dict): Dictionary mapping usernames to passwords
        task_list (list): List of task dictionaries
    """
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password:
        print("User does not exist. Please enter a valid username")
        return
        
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    
    # Get and validate due date
    due_date_time = None
    while not due_date_time:
        try:
            task_due_date = input("Due date of task (DD-MM-YYYY): ")  # Changed format in prompt
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
        except ValueError:
            print("Invalid datetime format. Please use the format DD-MM-YYYY")  # Changed format in error message
    
    # Create new task
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": datetime.now(),  # Changed to include time for consistency
        "completed": False
    }

    task_list.append(new_task)
    if save_tasks(task_list):
        print("Task successfully added.")


def view_all(task_list):
    """
    Display all tasks in a readable format with perfectly aligned columns.
    Uses DD-MM-YYYY date format for display.
    
    Args:
        task_list (list): List of task dictionaries
    """
    if not task_list:
        print("No tasks found.")
        return
        
    print("\n--- All Tasks ---")
    for t in task_list:
        print(f"\n{SEPARATOR_LINE}")
        print(f"{'Task:':<20}{t['title']}")
        print(f"{'Assigned to:':<20}{t['username']}")
        print(f"{'Date Assigned:':<20}{t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}")
        print(f"{'Due Date:':<20}{t['due_date'].strftime(DATETIME_STRING_FORMAT)}")
        print(f"{'Completed:':<20}{'Yes' if t['completed'] else 'No'}")
        print(f"{'Task Description:':<20}\n{t['description']}")
        print(f"{SEPARATOR_LINE}")


def edit_task(task_list, task_index, username_password):
    """
    Edit username or due date for an incomplete task.
    Uses DD-MM-YYYY date format for input.
    
    Args:
        task_list (list): List of task dictionaries
        task_index (int): Index of task to edit
        username_password (dict): Dictionary mapping usernames to passwords
    """
    if task_list[task_index]['completed']:
        print("Cannot edit a completed task.")
        return
    
    edit_option = input("Enter 'u' to change username or 'd' to change due date: ").lower()
    
    if edit_option == 'u':
        new_username = input("Enter new username: ")
        if new_username in username_password:
            task_list[task_index]['username'] = new_username
            save_tasks(task_list)
            print("Task reassigned successfully!")
        else:
            print("User does not exist. Task not updated.")
            
    elif edit_option == 'd':
        try:
            new_due_date = input("Enter new due date (DD-MM-YYYY): ")  # Changed format in prompt
            new_date_time = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
            task_list[task_index]['due_date'] = new_date_time
            save_tasks(task_list)
            print("Due date updated successfully!")
        except ValueError:
            print("Invalid datetime format. Task not updated.")  # Changed format in error message
    else:
        print("Invalid choice.")


def view_mine(curr_user, task_list, username_password):
    """
    View and manage tasks assigned to current user with perfectly aligned columns.
    Uses DD-MM-YYYY date format for display.
    
    Args:
        curr_user (str): Current username
        task_list (list): List of task dictionaries
        username_password (dict): Dictionary mapping usernames to passwords
    """
    # Filter user tasks
    user_tasks = [t for t in task_list if t['username'] == curr_user]
    
    if not user_tasks:
        print("You have no tasks assigned to you.")
        return
    
    # Display user tasks with perfect alignment
    print(f"\n--- Tasks assigned to {curr_user} ---")
    for i, t in enumerate(user_tasks, 1):
        print(f"\n{SEPARATOR_LINE}")
        print(f"{'Task Number:':<20}{i}")
        print(f"{'Task:':<20}{t['title']}")
        print(f"{'Date Assigned:':<20}{t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}")
        print(f"{'Due Date:':<20}{t['due_date'].strftime(DATETIME_STRING_FORMAT)}")
        print(f"{'Completed:':<20}{'Yes' if t['completed'] else 'No'}")
        print(f"{'Task Description:':<20}\n{t['description']}")
        print(f"{SEPARATOR_LINE}")
    
    # Task selection logic for editing or marking complete
    while True:
        try:
            task_choice = int(input("\nEnter task number to select a task or -1 to return to main menu: "))
            
            if task_choice == -1:
                return
                
            if not (1 <= task_choice <= len(user_tasks)):
                print("Invalid task number.")
                continue
                
            # Get selected task and its index in global task_list
            selected_task = user_tasks[task_choice - 1]
            global_task_index = task_list.index(selected_task)
            
            # Task action
            action = input("Enter 'c' to mark as complete or 'e' to edit task: ").lower()
            
            if action == 'c':
                task_list[global_task_index]['completed'] = True
                save_tasks(task_list)
                print("Task marked as complete!")
                return
                
            elif action == 'e':
                edit_task(task_list, global_task_index, username_password)
                return
                
            else:
                print("Invalid choice.")
                
        except ValueError:
            print("Invalid input. Please enter a number.")


def generate_reports(task_list, username_password):
    """
    Generate task and user overview reports with perfectly aligned columns.
    Uses DD-MM-YYYY date format in calculations.
    
    Args:
        task_list (list): List of task dictionaries
        username_password (dict): Dictionary mapping usernames to passwords
    """
    # Task overview calculations
    total_tasks = len(task_list)
    completed_tasks = sum(1 for t in task_list if t['completed'])
    uncompleted_tasks = total_tasks - completed_tasks
    
    # Get overdue tasks (current date comparison)
    current_date = datetime.now().date()
    overdue_tasks = sum(1 for t in task_list if not t['completed'] and t['due_date'].date() < current_date)
    
    # Calculate percentages (avoid division by zero)
    incomplete_percentage = (uncompleted_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    overdue_percentage = (overdue_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    
    # Write task overview report with perfect column alignment
    with open("task_overview.txt", "w") as report_file:
        report_file.write(f"{SEPARATOR_LINE}\n")
        report_file.write(f"{'TASK OVERVIEW':^80}\n")  # Center the title
        report_file.write(f"{SEPARATOR_LINE}\n")
        report_file.write(f"{'Total number of tasks:':<40}{total_tasks}\n")
        report_file.write(f"{'Total number of completed tasks:':<40}{completed_tasks}\n")
        report_file.write(f"{'Total number of uncompleted tasks:':<40}{uncompleted_tasks}\n")
        report_file.write(f"{'Total number of tasks that are overdue:':<40}{overdue_tasks}\n")
        report_file.write(f"{'Percentage of tasks that are incomplete:':<40}{incomplete_percentage:.2f}%\n")
        report_file.write(f"{'Percentage of tasks that are overdue:':<40}{overdue_percentage:.2f}%\n")
        report_file.write(f"{SEPARATOR_LINE}\n")
    
    # User overview report with perfect column alignment
    with open("user_overview.txt", "w") as report_file:
        report_file.write(f"{SEPARATOR_LINE}\n")
        report_file.write(f"{'USER OVERVIEW':^80}\n")  # Center the title
        report_file.write(f"{SEPARATOR_LINE}\n")
        report_file.write(f"{'Total number of registered users:':<40}{len(username_password)}\n")
        report_file.write(f"{'Total number of tasks:':<40}{total_tasks}\n")
        report_file.write(f"{SEPARATOR_LINE}\n")
        
        # Calculate statistics for each user
        for username in username_password:
            user_tasks = [t for t in task_list if t['username'] == username]
            user_task_count = len(user_tasks)
            
            report_file.write("\n")
            report_file.write(f"{SEPARATOR_LINE}\n")
            report_file.write(f"{'User:':<20}{username}\n")
            report_file.write(f"{SEPARATOR_LINE}\n")
            
            # Skip detailed stats if user has no tasks
            if user_task_count == 0:
                report_file.write("No tasks assigned to this user.\n")
                continue
            
            # Calculate user statistics
            task_percentage = (user_task_count / total_tasks) * 100 if total_tasks > 0 else 0
            completed_user_tasks = sum(1 for t in user_tasks if t['completed'])
            completed_percentage = (completed_user_tasks / user_task_count) * 100 if user_task_count > 0 else 0
            uncompleted_percentage = 100 - completed_percentage
            
            # Overdue tasks for user
            overdue_user_tasks = sum(1 for t in user_tasks 
                                    if not t['completed'] and t['due_date'].date() < current_date)
            overdue_percentage = (overdue_user_tasks / user_task_count) * 100 if user_task_count > 0 else 0
            
            # Write user statistics with perfect column alignment
            report_file.write(f"{'Total tasks assigned:':<40}{user_task_count}\n")
            report_file.write(f"{'Percentage of total tasks:':<40}{task_percentage:.2f}%\n")
            report_file.write(f"{'Percentage of tasks completed:':<40}{completed_percentage:.2f}%\n")
            report_file.write(f"{'Percentage of tasks to be completed:':<40}{uncompleted_percentage:.2f}%\n")
            report_file.write(f"{'Percentage of tasks overdue:':<40}{overdue_percentage:.2f}%\n")
            report_file.write(f"{SEPARATOR_LINE}\n")
    
    print("Reports generated successfully.")


def display_statistics(task_list, username_password):
    """
    Display statistics from generated reports.
    
    Args:
        task_list (list): List of task dictionaries
        username_password (dict): Dictionary mapping usernames to passwords
    """
    # Generate reports if they don't exist
    if not os.path.exists("task_overview.txt") or not os.path.exists("user_overview.txt"):
        generate_reports(task_list, username_password)
    
    # Display task overview
    print("\n===== TASK STATISTICS =====")
    with open("task_overview.txt", "r") as report_file:
        print(report_file.read())
    
    # Display user overview
    print("\n===== USER STATISTICS =====")
    with open("user_overview.txt", "r") as report_file:
        print(report_file.read())


def login():
    """
    Handle user login process.
    
    Returns:
        tuple: (username, username_password dictionary)
    """
    username_password = load_users()
    
    while True:
        print("LOGIN")
        curr_user = input("Username: ")
        curr_pass = input("Password: ")
        
        if curr_user not in username_password:
            print("User does not exist")
            continue
            
        if username_password[curr_user] != curr_pass:
            print("Wrong password")
            continue
            
        print("Login Successful!")
        return curr_user, username_password


def main():
    """
    Main program function. Controls program flow and menu options.
    """
    # Initialize tasks.txt if it doesn't exist
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w") as default_file:
            pass
            
    # Handle login
    curr_user, username_password = login()
    task_list = load_tasks()
    
    # Dictionary of menu options mapped to functions
    menu_options = {
        'r': lambda: reg_user(username_password),
        'a': lambda: add_task(username_password, task_list),
        'va': lambda: view_all(task_list),
        'vm': lambda: view_mine(curr_user, task_list, username_password),
        'gr': lambda: generate_reports(task_list, username_password),
        'ds': lambda: display_statistics(task_list, username_password) 
              if curr_user == 'admin' else print("Only admin users can display statistics."),
        'e': lambda: exit('Goodbye!!!')
    }
    
    # Main program loop
    while True:
        print()
        menu = input('''Select one of the following Options:
r - register user
a - add task
va - view all tasks
vm - view my tasks
gr - generate reports
ds - display statistics
e - Exit
: ''').lower()
        
        # Execute the selected menu option if it exists
        if menu in menu_options:
            menu_options[menu]()
        else:
            print("You have made a wrong choice, Please Try again")


if __name__ == "__main__":
    main()
