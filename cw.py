import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import logging
import random
import string

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()

retryable_exceptions = (TimeoutException, NoSuchElementException)

def chrome_driver():
    """
    Configure and initialize a Chrome WebDriver instance with optimized settings.
    
    Returns:
        webdriver.Chrome: Configured Chrome WebDriver instance with custom options for:
            - Stability (no-sandbox, disable-dev-shm-usage)
            - WebGL compatibility
            - Performance optimization
            - Reduced logging
    """
    chrome_options = Options()
    # Stability options
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    # WebGL fixes
    chrome_options.add_argument("--enable-unsafe-webgl")
    chrome_options.add_argument("--enable-unsafe-swiftshader")
    # Performance options
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-logging")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--silent")
    chrome_options.page_load_strategy = "normal"

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

def form(driver, email, max_retries=3):
    """
    Fill out the Cloudworkers application form using provided email.
    
    Args:
        driver (webdriver.Chrome): Initialized Chrome WebDriver instance
        email (str): Email address to use in the application
        max_retries (int, optional): Maximum number of retry attempts. Defaults to 3.
    
    Returns:
        bool: True if application submitted successfully, False otherwise
    
    The function:
        1. Validates email format (@gmail.com)
        2. Fills personal information (name, contact details, etc.)
        3. Selects dropdown values for birthday, country, etc.
        4. Handles reCAPTCHA verification
        5. Submits the form
        6. Implements retry logic for failures
    """
    if not email.endswith("@gmail.com"):
        logger.warning("Skipping invalid email: %s", email)
        return False

    for attempt in range(max_retries):
        try:
            # Clear browser state on retry attempts
            if attempt > 0:
                logger.info(f"Retry attempt {attempt + 1}/{max_retries}")
                driver.execute_script("window.localStorage.clear();")
                driver.execute_script("window.sessionStorage.clear();")
                driver.delete_all_cookies()
                driver.refresh()
                time.sleep(2)

            driver.get("https://www.cloudworkers.company/en")
            time.sleep(2)

            first_name = "John" # Add your first name
            last_name = "Doe" # Add your last name
            phone = "0700000000" # Add your phone number
            skype_name = "John Doe" # Add your Skype name
            times_available = "Anytime of the day" # Add your preferred time
            about_you = "Having had 2 years of experience as a customer service representative and 4 years of experience as a chat moderator. My objective role was to help entertain the user with stimulating conversation and encourage a long-lasting relationship engagement. And the ability to create and develop an imaginative and engaging experience for the user, build rapport, and ensure the customer has a positive experience." # Add a brief description about yourself

            # Wait up to 10 seconds for elements
            wait = WebDriverWait(driver, 10)

            
            try:

                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="text"].form-control.form-control-lg.required.form-custom[name="first_name"][id="first_name"]'))).send_keys(first_name)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="text"].form-control.form-control-lg.required.form-custom[name="last_name"][id="last_name"]'))).send_keys(last_name)
                email_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="email"].form-control.form-control-lg.required.form-custom[name="email"][id="email"]')))
                email_field.send_keys(email)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="text"].form-control.form-control-lg[name="phone_number"][id="phone_number"]'))).send_keys(phone)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="text"].form-control.form-control-lg[name="skype_name"][id="skype_name"]'))).send_keys(skype_name)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="text"].form-control.form-control-lg[name="reach_by_phone"][id="reach_by_phone"]'))).send_keys(times_available)
                
                about_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'textarea.form-control.form-control-lg.required[name="description"][id="description"]')))
                about_field.send_keys(about_you)

                # Dropdown selections with waits
                Select(wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'select.form-control.form-control-lg[name="day"][id="day"][required]')))).select_by_visible_text("01") # Add day in number format e.g. 19
                Select(wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'select.form-control.form-control-lg[name="month"][id="month"][required]')))).select_by_value("01") # Add month in number format e.g. 09
                Select(wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'select.form-control.form-control-lg[name="year"][id="year"][required]')))).select_by_visible_text("1900") # Add year in number format e.g. 1998
                Select(wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'select.form-control.form-control-lg[name="promotion"][id="promotion"]')))).select_by_value("Google")
                Select(wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'select.form-control.form-control-lg[name="application_country"][id="application_country"][required]')))).select_by_value("9")
                Select(wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'select.form-control.form-control-lg[name="experience"][id="experience"]')))).select_by_value("Yes")

                # Ensure the element is in view
                terms_checkbox = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="checkbox"].form-check-input.required[id="terms-of-use"][required]')))
                driver.execute_script("arguments[0].scrollIntoView(true);", terms_checkbox)
                time.sleep(1)  # Allow time for scrolling
                driver.execute_script("arguments[0].click();", terms_checkbox)

                print("Solve the reCAPTCHA manually. Waiting up to 60 seconds.")
                extended_wait = WebDriverWait(driver, 60)

                try:
                    # Wait for reCAPTCHA frame and switch to it
                    extended_wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, 'iframe[title="reCAPTCHA"]')))

                    # Click the reCAPTCHA checkbox
                    recaptcha_checkbox = extended_wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.recaptcha-checkbox-border'))
                    )
                    recaptcha_checkbox.click()
                    driver.switch_to.default_content()

                    # Wait for the `g-recaptcha-response` to be populated
                    print("Waiting for reCAPTCHA to be solved...")
                    extended_wait.until(
                        lambda d: d.find_element(By.ID, "g-recaptcha-response").get_attribute("value").strip() != ""
                    )
                    print("reCAPTCHA solved.")

                   # Proceed to locate and click the submit button
                    submit_button = extended_wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"].btn.btn-primary.btn-lg#btn-send-application'))
                    )
                    driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
                    submit_button.click()

                    # Wait for success confirmation
                    extended_wait.until(lambda d: d.current_url == "https://www.cloudworkers.company/en#applicationSuccessCard")
                    logger.info(f"Successfully submitted application for email: {email}")
                    return True

                except NoSuchElementException as e:
                    logger.error(f"Element not found for email {email}: {e}")
                    return False
                except TimeoutException as e:
                    logger.error(f"Operation timed out for email {email}: {e}")
                    return False


            except retryable_exceptions as e:
                if attempt < max_retries - 1:
                    logger.warning(
                        f"Attempt {attempt + 1} failed for email {email} with {e.__class__.__name__}: {str(e)}"
                    )
                    logger.info("Retrying with clean browser state...")
                else:
                    logger.error(
                        f"Max retries ({max_retries}) reached for email {email}. Last error: {str(e)}"
                    )
                    return False
            
            
        except Exception as e:
            logger.error(f"Unexpected error for email {email}: {str(e)}")
            return False

    return False

def generate_email_aliases(base_email, num_aliases):
    """
    Generate a list of email aliases based on the provided base email.
    
    Args:
        base_email (str): The base email address (e.g., "example@gmail.com")
        num_aliases (int): Number of aliases to generate
    
    Returns:
        list: List of generated email aliases
    """
    aliases = []
    for _ in range(num_aliases):
        alias = base_email.replace("@", f"+{random_string(5)}@")
        aliases.append(alias)
    return aliases

def random_string(length):
    """
    Generate a random string of the specified length.
    
    Args:
        length (int): Length of the random string
    
    Returns:
        str: Randomly generated string
    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def main():
    """
    Main execution function that orchestrates the application submission process.
    
    Workflow:
        1. Reads email addresses from 'aliases2.txt'
        2. Filters for valid Gmail addresses
        3. Processes up to 20 valid emails
        4. Reinitializes the WebDriver every 5 submissions
        5. Handles errors and provides logging
    
    Note: The function limits processing to 20 emails and restarts the browser 
    every 5 submissions to maintain stability.
    """
    try:
        # Generate email aliases
        base_email = "email@gmail.com" # Add your base email
        num_aliases = 20
        email_aliases = generate_email_aliases(base_email, num_aliases)

        # Use generated email aliases instead of reading from file
        valid_emails = email_aliases

        logger.info(f"Processing {len(valid_emails)} valid emails")

        driver = chrome_driver()
        successful_submissions = 0
        unsuccessful_submissions = 0
        try:
            for index, email in enumerate(valid_emails[:20], start=1):
                if index % 5 == 0:
                    driver.quit()
                    driver = chrome_driver()
                success = form(driver, email)
                if success:
                    successful_submissions += 1
                else:
                    unsuccessful_submissions += 1
                    logger.error(f"Failed to submit application for email: {email}")
        finally:
            if driver:
                driver.quit()
        logger.info(f"Total successful submissions: {successful_submissions}")
        logger.info(f"Total unsuccessful submissions: {unsuccessful_submissions}")
    except Exception as e:
        logger.critical("Critical error: %s", str(e))

if __name__ == "__main__":
    main()
