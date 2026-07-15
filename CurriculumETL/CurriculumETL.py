import json
from pathlib import Path
from services.etl_service import ETLService

DATA_DIR: str = "data" # Directory where JSON files are stored.

def main():
    print("Starting Lesson ETL validation...")

    etl = ETLService()
    directory = Path(DATA_DIR)

    if not directory.exists():
        print(f"Error: JSON data directory doesn't exist.")
        return
    
    for file_path in directory.glob("*.json"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                json_data = json.load(f)

                if not json_data or "data" not in json_data or not json_data["data"]:
                    continue

                etl.process_file(json_data)
        except (json.JSONDecodeError, PermissionError) as e:
            print(f"Error loading {file_path.name}: {e}")

if __name__ == "__main__":
    main()
