import sys
from dotenv import load_dotenv

from src.upload_s3_file import upload_s3_file

load_dotenv()

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <file_path>")
        sys.exit(1)
    file_path = sys.argv[1]
    upload_s3_file(file_path)

if __name__ == "__main__":
    main()