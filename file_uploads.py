import os

def clear_uploads():
    for file in os.listdir(".\\uploads\\"):
        os.remove(f".\\uploads\\{file}")


if __name__ == "__main__":
    clear_uploads()
