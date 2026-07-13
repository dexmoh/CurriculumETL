
# from database.db import get_connection


# def test_db():
#     try:
#         conn = get_connection()
#         cursor = conn.cursor()

#         cursor.execute(
#             "INSERT INTO test_connection (message) VALUES (?)",
#             "Hello from Milica"
#         )

#         conn.commit()

#         cursor.close()
#         conn.close()

#         print("Insert successful!")

#     except Exception as e:
#         print("Error:", e)


# if __name__ == "__main__":
#     test_db()

# from drive.drive_client import get_drive_service, list_files_recursive

# SERVICE_ACCOUNT_JSON = r"C:\Users\Sladjana\Documents\curriculum-etl-key\curriculumetl-9019948c547c.json"
# FOLDER_ID = "1bSOM6vmbmylWbWCqgAnXPiBLRCF7xs4b"


# def main():
#     print("Starting Drive test...")

#     service = get_drive_service(SERVICE_ACCOUNT_JSON)
#     print("Connected to Drive")

#     all_files = list_files_recursive(service, FOLDER_ID)

#     print("Found files:")
#     for f in all_files:
#         print(f["name"], f["id"])


# if __name__ == "__main__":
#     main()

# from drive.drive_client import (
#     get_drive_service,
#     list_files_recursive,
#     download_file_content
# )

# SERVICE_ACCOUNT_JSON = r"C:\Users\Sladjana\Documents\curriculum-etl-key\curriculumetl-9019948c547c.json"
# FOLDER_ID = "1bSOM6vmbmylWbWCqgAnXPiBLRCF7xs4b"


# def main():
#     print("Starting Drive test...")

#     service = get_drive_service(SERVICE_ACCOUNT_JSON)
#     all_files = list_files_recursive(service, FOLDER_ID)

#     # Find first JSON file only
#     for f in all_files:
#         if f["name"].endswith(".json"):
#             print("Found JSON:", f["name"])

#             # content = download_file_content(service, f["id"])
#             json_data = download_file_content(service, f["id"])

#             # print("\n--- FILE CONTENT START ---")
#             # print(content[:1000])  # print only first 1000 characters
#             # print("\n--- FILE CONTENT END ---")
#             # print("Type of object:", type(json_data))
#             # print("Top-level keys:", json_data.keys())

#             print("Top-level keys:", json_data.keys())

#             if "data" not in json_data:
#                 print("No lesson data found")
#                 break

#             lessons = json_data["data"]

#             print("Type of data:", type(lessons))
#             print("Number of items in data:", len(lessons))

#             if len(lessons) > 0:
#                 first = lessons[0]
#                 print("\nFirst lesson keys:")
#                 print(first.keys())

#             break  # stop after first file


# if __name__ == "__main__":
#     main()

from drive.drive_client import (
    get_drive_service,
    list_files_recursive,
    download_file_content
)
from services.etl_service import ETLService

SERVICE_ACCOUNT_JSON = r"C:\Users\Sladjana\Documents\curriculum-etl-key\curriculumetl-9019948c547c.json"
FOLDER_ID = "1bSOM6vmbmylWbWCqgAnXPiBLRCF7xs4b"


def main():
    print("Starting Lesson ETL validation...\n")

    service = get_drive_service(SERVICE_ACCOUNT_JSON)
    all_files = list_files_recursive(service, FOLDER_ID)
    
    etl = ETLService()

    for f in files:
        if f["name"].endswith(".json"):
            json_data = download_file_content(service, f["id"])
            etl.process_file(f, json_data)


    # for f in all_files:
    #     if not f["name"].endswith(".json"):
    #         continue

    #     print("--------------------------------------------------")
    #     print("Processing file:", f["name"])

    #     try:
    #         json_data = download_file_content(service, f["id"])
    #     except Exception as e:
    #         print("Download failed:", e)
    #         continue

    #     # 1️ Must contain "data"
    #     if "data" not in json_data:
    #         print("Skipping: no 'data' key")
    #         continue

    #     data_list = json_data["data"]

    #     # 2️ Must be non-empty list
    #     if not isinstance(data_list, list) or len(data_list) == 0:
    #         print("Skipping: empty or invalid data list")
    #         continue

    #     first = data_list[0]

    #     # 3️ Skip error JSON
    #     if "error" in first:
    #         print("Skipping: error JSON detected")
    #         continue

    #     # 4️ Accept only valid lesson structure
    #     if "LearningObject" not in first:
    #         print("Skipping: unknown JSON structure")
    #         continue

    #     #  VALID LESSON JSON (Type 1 or Type 2)
    #     print("VALID LESSON DETECTED")
    #     print("CourseCode:", first.get("CourseCode"))
    #     print("Lesson:", first.get("Lesson"))
    #     print("Title:", first.get("Title"))
    #     print("Year:", first.get("Year"))
    #     print("Author:", first.get("Author"))

    #     # learning_objects = first.get("LearningObject", [])
    #     # print("Number of LearningObjects:", len(learning_objects))

    #     learning_objects = first.get("LearningObject", [])

    #     print("Number of LearningObjects:", len(learning_objects))

    #     if len(learning_objects) > 0:
    #         lo = learning_objects[0]
    #         print("\n--- FIRST LEARNING OBJECT STRUCTURE ---")
    #         print("Keys:", lo.keys())

    #         for key, value in lo.items():
    #             print(f"\nField: {key}")
    #             print("Type:", type(value))

    #     break  # stop after first file

    # print("\nValidation phase complete.")


if __name__ == "__main__":
    main()