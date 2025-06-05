from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import json
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_driver():
    """Set up and return a configured Chrome WebDriver."""
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Uncomment for headless mode
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_experimental_options = {"excludeSwitches": ["enable-automation"], "useAutomationExtension": False}
    chrome_options.add_experimental_option("prefs", {"credentials_enable_service": False, "profile.password_manager_enabled": False})
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

def wait_for_element(driver, by, value, timeout=20):
    """Wait for an element to be present and visible."""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        # Also wait for visibility
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((by, value))
        )
        return element
    except TimeoutException:
        logger.error(f"Timeout waiting for element: {value}")
        raise

def extract_job_fields(url):
    """
    Navigate to the Ashby careers page, filter for Americas Engineering,
    select the first job, extract description and required fields from the application form.
    Returns the driver instance along with the extracted data.
    """
    driver = setup_driver()
    job_description = ""
    extracted_fields = []
    try:
        logger.info("Navigating to careers page...")
        driver.get(url)
        time.sleep(5)  # Give the page time to fully load
        
        # Try to find and switch to the iframe
        logger.info("Looking for job board iframe...")
        try:
            iframe = wait_for_element(driver, By.ID, "ashby_embed_iframe")
            logger.info("Found iframe, switching to it...")
            driver.switch_to.frame(iframe)
            logger.info("Switched to iframe")
        except TimeoutException:
            logger.info("No iframe found or timeout, continuing with main page...")
            try:
                driver.switch_to.default_content()
                logger.info("Switched back to default content.")
            except Exception as e:
                logger.warning(f"Could not switch back to default content: {e}")

        # Try to find the department select element
        logger.info("Looking for department select element...")
        selectors = [
            (By.CSS_SELECTOR, 'select[name="departmentId"]'),
            (By.CSS_SELECTOR, 'select.ashby-job-board-filter[name="departmentId"]'),
            (By.XPATH, "//select[@name='departmentId']"),
            (By.XPATH, "//select[contains(@class, 'ashby-job-board-filter')]")
        ]
        
        department_select = None
        for by, selector in selectors:
            try:
                logger.info(f"Trying selector: {selector}")
                department_select = wait_for_element(driver, by, selector, timeout=30)
                if department_select and department_select.is_displayed() and department_select.is_enabled():
                    logger.info(f"Found and element is interactable using: {selector}")
                    break
            except TimeoutException:
                continue
            except Exception as e:
                logger.warning(f"Error finding/waiting for element with {selector}: {e}")
                continue
        
        if not department_select:
            raise NoSuchElementException("Could not find department select element after trying all selectors.")
        
        # Select Americas Engineering
        logger.info("Selecting Americas Engineering department...")
        select = Select(department_select)
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'option'))
            )
            select.select_by_value("d22def71-84b4-4837-b73f-854a46fdb3fc")
            logger.info("Successfully selected Americas Engineering by value")
        except NoSuchElementException:
            logger.warning("Could not select Americas Engineering by value, trying by visible text")
            try:
                select.select_by_visible_text("Americas Engineering")
                logger.info("Successfully selected Americas Engineering by visible text")
            except NoSuchElementException:
                logger.error("Could not select Americas Engineering by visible text.")
                raise
        
        time.sleep(2)  # Wait for the job listings to update after selection
        
        # Wait for job listings and click the first one
        logger.info("Finding and clicking first job listing...")
        job_selectors = [
            (By.CSS_SELECTOR, 'div._jobPosting_12ylk_379'),
            (By.CSS_SELECTOR, 'div.ashby-job-posting-brief')
        ]
        
        job_link = None
        for by, selector in job_selectors:
            try:
                logger.info(f"Trying job selector: {selector}")
                job_link = wait_for_element(driver, by, selector, timeout=5)
                if job_link:
                    logger.info(f"Found job link using: {selector}")
                    parent_anchor = job_link.find_element(By.XPATH, "./ancestor::a")
                    parent_anchor.click()
                    logger.info("Clicked first job listing")
                    break
            except TimeoutException:
                continue
            except Exception as e:
                logger.warning(f"Error finding/waiting for job link with {selector}: {e}")
                continue
        
        if not job_link:
            raise NoSuchElementException("Could not find job listing link after trying all selectors.")
        
        time.sleep(2)  # Wait for job details to load

        # Extract job description
        logger.info("Extracting job description...")
        description_selectors = [
            (By.XPATH, "//div[contains(@class, '_description_')]"),
            (By.XPATH, "//div[contains(@class, 'job-posting-page-description')]"),
            (By.CSS_SELECTOR, 'div.job-posting-page-description'),
            (By.CSS_SELECTOR, 'div[data-ph="description"]'),
            (By.CSS_SELECTOR, 'div._description_1aam4_1'),
            (By.XPATH, "//div[@data-ph='description']"),
        ]

        description_element = None
        for by, selector in description_selectors:
            try:
                logger.info(f"Trying description selector: {selector}")
                description_element = wait_for_element(driver, by, selector, timeout=5)
                if description_element:
                    logger.info(f"Found description element using: {selector}")
                    job_description = description_element.text
                    logger.info("Successfully extracted job description")
                    break
            except TimeoutException:
                continue

        # Return the driver and job description here
        return driver, job_description

    except Exception as e:
        logger.error(f"Error during extraction: {e}")
        if driver:
            driver.quit()
        raise

def click_apply_button(driver):
    logger.info("Clicking Apply button...")
    apply_button_selectors = [
        (By.XPATH, "//button[contains(text(), 'Apply')]"),
        (By.CSS_SELECTOR, 'button._primary_8wvgw_96'),
        (By.CSS_SELECTOR, 'button[data-qa*="apply-button"]')
    ]

    apply_button = None
    for by, selector in apply_button_selectors:
        try:
            logger.info(f"Trying Apply button selector: {selector}")
            apply_button = WebDriverWait(driver, 15).until(
                 EC.element_to_be_clickable((by, selector))
             )
            if apply_button:
                logger.info(f"Found Apply button using: {selector}")
                break
        except TimeoutException:
            continue
        except Exception as e:
            logger.warning(f"Error finding/waiting for Apply button with {selector}: {e}")
            continue

    if not apply_button:
        raise NoSuchElementException("Could not find Apply button after trying all selectors.")

    try:
        apply_button.click()
        logger.info("Clicked Apply button using standard click.")
    except StaleElementReferenceException:
         logger.warning("StaleElementReferenceException during standard click, trying again...")
         # Re-find the element and click again
         # Use the first selector that worked in the loop above
         try:
             apply_button = WebDriverWait(driver, 10).until(
                  EC.element_to_be_clickable((apply_button_selectors[0][0], apply_button_selectors[0][1]))
             )
             apply_button.click()
             logger.info("Clicked Apply button using standard click (after re-finding).")
         except Exception as re_e:
              logger.warning(f"Re-finding and clicking failed: {re_e}. Trying JavaScript click...")
              driver.execute_script("arguments[0].click();", apply_button)
              logger.info("Clicked Apply button using JavaScript (after re-finding failure).")
    except Exception as e:
        logger.warning(f"Standard click failed: {e}. Trying JavaScript click...")
        driver.execute_script("arguments[0].click();", apply_button)
        logger.info("Clicked Apply button using JavaScript.")

    # Give time for the form to load after clicking Apply
    time.sleep(5)

if __name__ == "__main__":
    # Test the extraction with the Ashby careers page
    url = "https://www.ashbyhq.com/careers"
    try:
        driver, description = extract_job_fields(url)
        print("\nExtracted Job Description:")
        print(description)
    except Exception as e:
        print(f"\nError: {str(e)}") 