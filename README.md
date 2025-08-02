# Lists-functions-and-string-handling


## 📋 Task Management System

A comprehensive command-line task management application built with Python that demonstrates advanced programming concepts including list manipulation, function design, string handling, and file operations. This capstone project showcases professional-grade software development practices with user authentication, data persistence, and administrative reporting capabilities.

## 🎯 Project Overview

This enterprise-level task management system provides a complete solution for team task coordination and project tracking. The application features secure user authentication, comprehensive task management, and detailed analytics reporting - all implemented through a clean command-line interface.

## ✨ Key Features

### 🔐 User Management
- **Secure Authentication System** - Username/password login with validation
- **User Registration** - New user creation with duplicate prevention
- **Role-Based Access** - Administrative privileges for advanced features
- **Persistent User Storage** - File-based user data management

### 📝 Task Management
- **Task Creation** - Comprehensive task details with user assignment
- **Task Viewing** - Display all tasks or filter by current user
- **Task Editing** - Modify assignee and due dates for incomplete tasks
- **Task Completion** - Mark tasks as completed with status tracking
- **Due Date Management** - Date validation and overdue detection

### 📊 Analytics & Reporting
- **Task Overview Reports** - System-wide task statistics and completion rates
- **User Overview Reports** - Individual user performance metrics
- **Statistical Analysis** - Percentage calculations and trend analysis
- **File-Based Reports** - Exportable `.txt` report generation

### 💾 Data Management
- **File Persistence** - Automatic saving of tasks and users
- **Data Validation** - Input sanitization and error handling
- **Format Compatibility** - Support for multiple data formats
- **Backup Recovery** - Graceful handling of file corruption

## 🛠️ Technologies & Concepts Demonstrated

### Core Python Skills
- **Lists & Data Structures** - Complex list manipulation and filtering
- **Functions & Modularity** - Well-organized function design with clear separation of concerns
- **String Handling** - Advanced string parsing, formatting, and validation
- **File I/O Operations** - Reading, writing, and managing persistent data
- **Date/Time Management** - Date parsing, validation, and calculations

### Advanced Programming Concepts
- **Error Handling** - Comprehensive exception management
- **Data Validation** - Input sanitization and type checking
- **Algorithm Implementation** - Sorting, filtering, and statistical calculations
- **Code Organization** - PEP 8 compliant structure with clear documentation
- **User Interface Design** - Intuitive menu systems and user interaction

## 🚀 Installation & Setup

1. **Prerequisites**: Python 3.6 or higher
2. **Download**: Clone or download the `task_manager.py` file
3. **Initial Setup**: The program creates necessary files on first run
4. **Default Login**: 
   - Username: `admin`
   - Password: `password`

## 📖 Usage Guide

### Starting the Application
```bash
python task_manager.py
```

### Menu Options

| Option | Description | Access Level |
|--------|-------------|--------------|
| `r` | Register new user | All users |
| `a` | Add new task | All users |
| `va` | View all tasks | All users |
| `vm` | View my tasks | All users |
| `gr` | Generate reports | All users |
| `ds` | Display statistics | Admin only |
| `e` | Exit application | All users |

### Task Management Workflow

1. **Adding Tasks**:
   ```
   Select option: a
   Name of person assigned to task: john_doe
   Title of Task: Complete project documentation
   Description of Task: Create comprehensive user manual
   Due date of task (DD-MM-YYYY): 25-12-2024
   ```

2. **Viewing Personal Tasks**:
   ```
   Select option: vm
   Task Number: 1
   Enter task number to select: 1
   Enter 'c' to mark as complete or 'e' to edit task: c
   ```

3. **Editing Tasks**:
   ```
   Enter 'u' to change username or 'd' to change due date: d
   Enter new due date (DD-MM-YYYY): 30-12-2024
   ```

## 📊 Sample Output

### Task Display Format
```
________________________________________________________________________________
Task Number:         1
Task:               Complete project documentation
Date Assigned:      20-12-2024
Due Date:           25-12-2024
Completed:          No
Task Description:   
Create comprehensive user manual for the new system
________________________________________________________________________________
```

### Statistical Reports
```
________________________________________________________________________________
                                TASK OVERVIEW                                
________________________________________________________________________________
Total number of tasks:                  15
Total number of completed tasks:        8
Total number of uncompleted tasks:      7
Total number of tasks that are overdue: 3
Percentage of tasks that are incomplete: 46.67%
Percentage of tasks that are overdue:   20.00%
________________________________________________________________________________
```

## 🏗️ Code Architecture

### Function Organization
```python
# Data Management
load_tasks()           # Parse and load task data
load_users()           # Load user credentials
save_tasks()           # Persist task data
save_users()           # Save user information

# User Operations
reg_user()             # Register new users
login()                # Handle authentication

# Task Operations
add_task()             # Create new tasks
view_all()             # Display all tasks
view_mine()            # Show user-specific tasks
edit_task()            # Modify existing tasks

# Analytics
generate_reports()     # Create statistical reports
display_statistics()   # Show admin analytics
```

### Data Structures
- **Task Dictionary**: Contains username, title, description, due_date, assigned_date, completed
- **User Dictionary**: Maps usernames to passwords
- **File Formats**: Structured text files with consistent formatting

## 🎓 Programming Concepts Mastered

### List Manipulation
- **Filtering**: `[t for t in task_list if t['username'] == curr_user]`
- **Searching**: Finding tasks by criteria and user assignment
- **Sorting**: Organizing tasks by date and completion status
- **Indexing**: Safe list access with bounds checking

### Function Design
- **Single Responsibility**: Each function has a clear, specific purpose
- **Parameter Passing**: Efficient data sharing between functions
- **Return Values**: Consistent error handling and success indicators
- **Documentation**: Comprehensive docstrings for all functions

### String Handling
- **Parsing**: Complex text file interpretation
- **Formatting**: Professional output with aligned columns
- **Validation**: Input sanitization and format checking
- **Manipulation**: Date format conversion and text processing

### File Operations
- **Error Handling**: Graceful management of file system issues
- **Data Persistence**: Reliable saving and loading mechanisms
- **Format Management**: Support for multiple file structures
- **Backup Strategies**: Fallback options for data recovery

## 📈 Advanced Features

### Date Management
- **Format Standardization**: DD-MM-YYYY format throughout
- **Validation**: Comprehensive date input checking
- **Calculations**: Overdue detection and time-based analytics
- **Conversion**: Flexible date format handling

### Error Handling
- **File Operations**: Safe file reading/writing with fallbacks
- **User Input**: Validation and sanitization of all inputs
- **Data Integrity**: Checking for corrupted or incomplete data
- **Graceful Degradation**: Continuing operation despite errors

### Security Features
- **Authentication**: Secure login system
- **Authorization**: Role-based access control
- **Data Protection**: Input validation and sanitization
- **Session Management**: Proper user session handling

## 🔧 Technical Specifications

### File Structure
```
Lists-Functions-String-Handling-Capstone/
├── README.md
├── task_manager.py
├── tasks.txt                 # Generated on first run
├── user.txt                  # Generated on first run
├── task_overview.txt         # Generated by reports
└── user_overview.txt         # Generated by reports
```

### System Requirements
- **Python**: 3.6 or higher
- **Storage**: Minimal disk space for text files
- **Memory**: Low memory footprint
- **Platform**: Cross-platform compatibility

## 🎯 Learning Outcomes

This project demonstrates mastery of:

**Data Structures**: Complex list operations, dictionary management, and data relationships
**Algorithm Design**: Sorting, filtering, searching, and statistical calculations
**File Management**: Persistent data storage, format handling, and error recovery
**User Interface**: Menu-driven systems and interactive user experiences
**Software Architecture**: Modular design, function organization, and code maintainability
**Problem Solving**: Real-world application development and business logic implementation

## 🚀 Future Enhancements

Potential improvements and extensions:
- **Database Integration** - Migrate from file storage to SQLite/PostgreSQL
- **Web Interface** - Flask/Django web application
- **API Development** - RESTful API for external integrations
- **Advanced Reporting** - Charts, graphs, and data visualization
- **Email Notifications** - Automated task reminders and updates
- **Collaborative Features** - Team messaging and file sharing
- **Mobile Application** - Cross-platform mobile task management



## 📝 Code Quality

This project follows professional development standards:
- **PEP 8 Compliance** - Consistent Python style guidelines
- **Comprehensive Documentation** - Detailed function docstrings
- **Error Handling** - Robust exception management
- **Code Organization** - Logical structure and modularity
- **User Experience** - Intuitive interface and clear feedback

## 📄 License

This project is created for educational purposes demonstrating advanced Python programming concepts.

---

*Professional-grade task management system showcasing advanced Python programming, data structures, and software architecture principles.*
