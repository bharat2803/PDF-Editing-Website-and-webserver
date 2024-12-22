import os

def clear_uploads():
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    for file in os.listdir("uploads"):
        file_path = os.path.join("uploads", file)
    
        # Check if it is a file before trying to remove
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Removed: {file_path}")
        else:
            print(f"Skipped (not a file): {file_path}")


if __name__ == "__main__":
    clear_uploads()
