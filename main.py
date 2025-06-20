import logging
import sys
from dotenv import load_dotenv

from logging_conf import configure_logging
from src.upload_s3_file import upload_s3_file

load_dotenv()

configure_logging()
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting S3 file upload script")
    if len(sys.argv) < 2:
        logger.error("File path argument is required")
        sys.exit(1)
    file_path = sys.argv[1]
    upload_s3_file(file_path)
    logger.info("S3 file upload script completed successfully")

if __name__ == "__main__":
    main()