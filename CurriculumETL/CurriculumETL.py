import json
from pathlib import Path
from services.etl_service import etl_process_json

DATA_DIR: str = "data" # Directory where JSON files are stored.

def main():
    print("Starting Lesson ETL validation...")

    directory = Path(DATA_DIR)

    if not directory.exists():
        print(f"Error: JSON data directory doesn't exist.")
        return
    
    counter: int = 0
    for file_path in directory.glob("*.json"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                json_data: dict = json.load(f)

                if not json_data or "data" not in json_data or not json_data["data"]:
                    continue

                etl_process_json(json_data)
                counter += 1
        except (json.JSONDecodeError, PermissionError) as e:
            print(f"Error loading {file_path.name}: {e}")
    print(f"Done! Processed {counter} JSON files.")

if __name__ == "__main__":
    main()
