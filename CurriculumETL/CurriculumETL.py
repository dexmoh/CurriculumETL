import json
from pathlib import Path
from gui_app import GuiApp
from services.etl_service import etl_process_json
from services.drive_downloader_service import download_drive_data

# Directory where JSON files are stored.
JSON_DATA_DIR: str = "data"

# Set this to True if you don't already have all JSON files downloaded inside JSON_DATA_DIR.
DOWNLOAD_DATA_BEFORE_PROCESSING: bool = True

# Whether the GUI app should autorun when processing finishes.
RUN_GUI_AFTER_PROCESSING: bool = True

def main():
    print("Starting Lesson ETL validation...")

    if DOWNLOAD_DATA_BEFORE_PROCESSING:
        download_drive_data(JSON_DATA_DIR)

    directory = Path(JSON_DATA_DIR)

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
                print(f"Processed file: {json_data.get("driveFileName", "N/A")} (#{counter})")
        except (json.JSONDecodeError, PermissionError) as e:
            print(f"Error loading {file_path.name}: {e}")
        except Exception as e:
            print(f"ERROR: {e}")
            break

    print(f"Done! Processed {counter} JSON files.")

    if RUN_GUI_AFTER_PROCESSING:
        GuiApp().run()

if __name__ == "__main__":
    main()
