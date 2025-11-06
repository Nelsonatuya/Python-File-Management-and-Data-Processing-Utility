import os
import sys
import json
import csv
from datetime import datetime

def prompt_create_students(json_path):
    """Prompt user to create students.json with 5 students and save it."""
    try:
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        students = []
        print("students.json not found.Create one with 5 students.")
        print("For scores enter comma-separated numbers, e.g. 80,90,70")
        for i in range(5):
            while True:
                sid = input(f"Student {i+1} id (e.g., S001): ").strip()
                name = input(f"Student {i+1} name (e.g., Alice): ").strip()
                scores_raw = input(f"Student {i+1} scores (comma-separated): ").strip()
                # parse scores
                try:
                    if scores_raw == "":
                        scores = []
                    else:
                        scores = [int(s.strip()) for s in scores_raw.split(',') if s.strip() != ""]
                except ValueError:
                    print("Invalid scores. Please enter integers separated by commas.")
                    continue
                if not sid or not name:
                    print("ID and name cannot be empty. Please re-enter.")
                    continue
                students.append({"id": sid, "name": name, "scores": scores})
                break
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(students, f, indent=2)
        print(f"Created students.json at: {json_path}")
        return students
    except Exception as e:
        print(f"Failed to create students.json: {e}")
        return None

def load_students(json_path):
    """Load students list from JSON file."""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"students.json not found at: {json_path}")
        ans = input("Would you like to create students.json now with 5 students? (Yes/No): ").strip().lower()
        if ans == "yes":
            created = prompt_create_students(json_path)
            if created is None:
                return None
            return created
        else:
            return None
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON file: {e}")
        return None

def compute_averages(students):
    """Compute average score for each student, rounded to 2 decimals."""
    results = []
    for s in students:
        scores = s.get('scores', []) or []
        avg = round(sum(scores) / len(scores), 2) if scores else 0.00
        results.append({
            'id': s.get('id', ''),
            'name': s.get('name', ''),
            'average': avg
        })
    return results

def write_csv(report_path, rows):
    """Write rows to CSV with headers id,name,average."""
    try:
        with open(report_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['id', 'name', 'average'])
            writer.writeheader()
            for r in rows:
                # Format average with two decimals
                r_out = {'id': r['id'], 'name': r['name'], 'average': f"{r['average']:.2f}"}
                writer.writerow(r_out)
        return True
    except Exception as e:
        print(f"Failed to write CSV: {e}")
        return False

def main():
    base_dir = os.path.join(os.getcwd(), "StudentFiles")
    json_path = os.path.join(base_dir, "students.json")
    report_path = os.path.join(base_dir, "report.csv")

    students = load_students(json_path)
    if students is None:
        # Informative message already printed by load_students
        return

    try:
        results = compute_averages(students)
        # Sort by average descending
        results.sort(key=lambda x: x['average'], reverse=True)

        success = write_csv(report_path, results)
        if success:
            print(f"Report written to: {report_path}")
        else:
            sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
