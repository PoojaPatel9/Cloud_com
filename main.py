import sys
import qrcode
import logging
import os
import argparse
from pathlib import Path

# Environment Variables for Configuration
QR_DIRECTORY = os.getenv('QR_CODE_DIR', 'qr_codes')  # Directory for saving QR code
QR_FILENAME = os.getenv('QR_CODE_FILENAME', 'github_qr.png')  # Filename from env
FILL_COLOR = os.getenv('FILL_COLOR', 'red')  # Fill color for the QR code
BACK_COLOR = os.getenv('BACK_COLOR', 'white')  # Background color for the QR code
DEFAULT_URL = os.getenv('QR_DATA_URL', 'https://github.com/PoojaPatel9')  # Default GitHub profile

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

def create_directory(directory_path):
    """Ensure the QR code directory exists."""
    try:
        os.makedirs(directory_path, exist_ok=True)
    except Exception as e:
        logging.error(f"Failed to create directory {directory_path}: {e}")
        sys.exit(1)

def is_valid_url(url):
    """Validate the provided URL."""
    if validators.url(url):
        return True
    else:
        logging.error(f"Invalid URL provided: {url}")
        return False

def generate_qr_code(data, output_path, fill_color='red', back_color='white'):
    """Generate and save a QR code."""
    if not is_valid_url(data):
        return  # Exit the function if the URL is not valid

    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color=fill_color, back_color=back_color)

        img.save(output_path)
        logging.info(f"QR code successfully saved to {output_path}")

    except Exception as e:
        logging.error(f"An error occurred while generating or saving the QR code: {e}")

def main():
    """Main function to handle QR code generation."""
    parser = argparse.ArgumentParser(description="Generate a QR code.")
    parser.add_argument('--url', help="The URL to encode in the QR code", default=DEFAULT_URL)
    args = parser.parse_args()

    # Ensure QR code directory exists
    create_directory(QR_DIRECTORY)

    # Generate and save the QR code to the specified path
    qr_code_full_path = os.path.join(QR_DIRECTORY, QR_FILENAME)
    generate_qr_code(args.url, qr_code_full_path, FILL_COLOR, BACK_COLOR)

if __name__ == "__main__":
    main()
