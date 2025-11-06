import os
import sys
import shutil
from datetime import datetime

def log_activity(message):
    """Append a timestamped message to StudentFiles/activity_log.txt."""
    try:
        current_dir = os.getcwd()
        student_files_path = os.path.join(current_dir, "StudentFiles")
        os.makedirs(student_files_path, exist_ok=True)
        log_file = os.path.join(student_files_path, "activity_log.txt")
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"{timestamp} {message}\n")
    except Exception:
        # If logging fails, print to stderr but do not raise further
        print("Failed to write to activity log.", file=sys.stderr)

def initialize_project():
    """Initialize the project by creating StudentFiles directory."""
    try:
        # Get the current directory
        current_dir = os.getcwd()
        student_files_path = os.path.join(current_dir, "StudentFiles")
        
        # Check if StudentFiles folder exists
        if not os.path.exists(student_files_path):
            os.makedirs(student_files_path)
            print(f"Created StudentFiles directory at: {os.path.abspath(student_files_path)}")
        else:
            print(f"StudentFiles directory already exists at: {os.path.abspath(student_files_path)}")
            
        return student_files_path
        
    except PermissionError as e:
        log_activity(f"ERROR: Permission denied. Unable to create directory: {e}")
        print("Error: Permission denied. Unable to create directory.")
        sys.exit(1)
    except Exception as e:
        log_activity(f"ERROR: Unexpected error during initialization: {e}")
        print(f"Error: An unexpected error occurred: {str(e)}")
        sys.exit(1)

def create_student_records():
    """Create a new file with student records."""
    try:
        # Generate filename with current date
        current_date = datetime.now().strftime("%Y-%m-%d")
        filename = f"records_{current_date}.txt"
        
        # Get the full path
        student_files_path = initialize_project()
        file_path = os.path.join(student_files_path, filename)
        
        # Get student names
        student_names = []
        print("Please enter 5 student names:")
        for i in range(5):
            name = input(f"Enter student {i+1} name: ")
            student_names.append(name)
        
        # Write to file
        with open(file_path, 'w', encoding="utf-8") as file:
            for name in student_names:
                file.write(f"{name}\n")
        
        # Display success message
        creation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\nSuccess! File '{filename}' created at {creation_time}")
        return file_path
        
    except Exception as e:
        log_activity(f"ERROR: Unable to create or write to file: {e}")
        print(f"Error: Unable to create or write to file: {str(e)}")
        sys.exit(1)

def display_file_info(file_path=None):
    """Read and display file contents and information."""
    try:
        # If no file_path provided, get the most recent file
        if file_path is None:
            student_files_path = initialize_project()
            files = [f for f in os.listdir(student_files_path) if f.startswith('records_')]
            if not files:
                print("No record files found!")
                return
            latest_file = max(files)
            file_path = os.path.join(student_files_path, latest_file)

        # Display file contents
        print("\nFile Contents:")
        print("-" * 20)
        with open(file_path, 'r', encoding="utf-8") as file:
            print(file.read())
        print("-" * 20)

        # Display file size
        size_bytes = os.path.getsize(file_path)
        print(f"File size: {size_bytes} bytes")

        # Display last modified date
        mod_time = os.path.getmtime(file_path)
        mod_date = datetime.fromtimestamp(mod_time)
        print(f"Last modified: {mod_date}")

    except Exception as e:
        log_activity(f"ERROR: Unable to read file information: {e}")
        print(f"Error: Unable to read file information: {str(e)}")
        sys.exit(1)

def backup_and_archive(file_path=None):
    """Create a backup copy, move it into Archive, and list Archive contents."""
    try:
        student_files_path = initialize_project()

        # Determine source file
        if file_path is None:
            files = [f for f in os.listdir(student_files_path) if f.startswith('records_')]
            if not files:
                print("No record files to backup!")
                return None
            latest_file = max(files)
            file_path = os.path.join(student_files_path, latest_file)

        # Create backup filename and copy
        backup_filename = f"backup_{os.path.basename(file_path)}"
        backup_path = os.path.join(student_files_path, backup_filename)
        shutil.copy(file_path, backup_path)

        # Ensure Archive folder exists
        archive_dir = os.path.join(student_files_path, "Archive")
        os.makedirs(archive_dir, exist_ok=True)

        # Move backup into Archive
        dest_path = shutil.move(backup_path, os.path.join(archive_dir, backup_filename))
        print(f"Backup created and moved to Archive: {os.path.basename(dest_path)}")

        # List files in Archive
        archive_files = os.listdir(archive_dir)
        print("Files in Archive:")
        for f in archive_files:
            print(f" - {f}")

        return dest_path

    except Exception as e:
        log_activity(f"ERROR: Backup/archive failed: {e}")
        print(f"Error during backup/archive: {str(e)}")
        sys.exit(1)

def delete_file_prompt():
    """Prompt user to delete a file from StudentFiles, perform deletion, log and list remaining files."""
    try:
        student_files_path = initialize_project()
        answer = input("Would you like to delete a file from the StudentFiles folder? (Yes/No): ").strip().lower()
        if answer != "yes":
            return

        filename = input("Enter the exact filename to delete (e.g., records_2025-10-31.txt): ").strip()
        target_path = os.path.join(student_files_path, filename)

        # Security check: ensure target_path is inside StudentFiles
        abs_student_dir = os.path.abspath(student_files_path)
        abs_target = os.path.abspath(target_path)
        if not abs_target.startswith(abs_student_dir + os.sep) and abs_target != abs_student_dir:
            print("Invalid filename or path. Deletion aborted.")
            log_activity(f"ERROR: Attempted deletion outside StudentFiles: {filename}")
            return

        if not os.path.exists(target_path):
            print(f"File '{filename}' does not exist in StudentFiles.")
            log_activity(f"ERROR: Deletion failed; file not found: {filename}")
            return

        os.remove(target_path)
        print(f"File '{filename}' deleted successfully.")
        log_activity(f"{filename} deleted successfully.")

        # Display remaining files in StudentFiles
        remaining = os.listdir(student_files_path)
        print("Remaining files in StudentFiles:")
        for f in remaining:
            print(f" - {f}")

    except Exception as e:
        log_activity(f"ERROR: Deletion failed: {e}")
        print(f"Error during deletion: {e}")

if __name__ == "__main__":
    file_path = create_student_records()
    display_file_info(file_path)
    dest = backup_and_archive(file_path)
    if dest:
        log_activity(f"{os.path.basename(file_path)} created and archived successfully.")
    delete_file_prompt()
