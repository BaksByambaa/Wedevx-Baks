from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import logging
import time
import os

# Configure logging (should match job_application_bot.py setup)
logger = logging.getLogger(__name__)

def wait_for_element(driver, by, value, timeout=10):
    """Wait for an element to be present and visible."""
    try:
        # First wait for presence
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        # Then wait for visibility
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((by, value))
        )
        return element
    except TimeoutException:
        logger.error(f"Timeout waiting for element: {value}")
        raise
    except Exception as e:
        logger.error(f"Error waiting for element {value}: {e}")
        raise

def fill_job_application(driver, resume_path=None):
    """
    Fill out the specified required fields in the job application form with dummy data.
    Includes logic to upload a resume if resume_path is provided.
    Does not click submit button.
    Accepts driver instance already on the application page.
    """
    try:
        logger.info("Starting to fill application form...")
        
        # Wait for the application form container to be present
        logger.info("Waiting for application form container...")
        form_container_selector = 'div._jobPostingForm_14ib5_407.ashby-application-form-container'
        try:
            form = wait_for_element(driver, By.CSS_SELECTOR, form_container_selector, timeout=10)
            logger.info("Application form container found.")
        except TimeoutException:
            logger.error(f"Timeout waiting for application form container: {form_container_selector}")
            return False # Indicate failure
        except Exception as e:
            logger.error(f"Error finding application form container: {e}")
            return False # Indicate failure
        
        # Dummy data for the specific required fields
        dummy_data = {
            '_systemfield_name': 'Baks Tech',
            '_systemfield_email': 'baks.tech@gmail.com',
            '2dad4788-1915-4348-8891-7fd4756fe97c': 'Yes',  # Timezone question
            'dacaf08c-8fa5-41ce-ab88-ad54a5e0d5ec': 'Yes',  # 5+ years frontend
            '7e0074c4-e91f-4416-9cdd-178953fb90d4': 'Yes'   # Design system contributions
        }

        logger.info("Attempting to fill specific required fields...")

        # --- Fill Name field ---
        field_id = '_systemfield_name'
        logger.info(f"Attempting to fill field: {field_id}")
        try:
            # Find the input element within the form container by its ID
            name_input = WebDriverWait(form, 5).until(
                EC.presence_of_element_located((By.ID, field_id))
            )
            name_input.clear()
            name_input.send_keys(dummy_data[field_id])
            logger.info(f"Successfully filled field: {field_id}")
        except Exception as e:
            logger.warning(f"Error filling field {field_id}: {e}")

        # --- Fill Email field ---
        field_id = '_systemfield_email'
        logger.info(f"Attempting to fill field: {field_id}")
        try:
            # Find the input element within the form container by its ID
            email_input = WebDriverWait(form, 5).until(
                EC.presence_of_element_located((By.ID, field_id))
            )
            email_input.clear()
            email_input.send_keys(dummy_data[field_id])
            logger.info(f"Successfully filled field: {field_id}")
        except Exception as e:
            logger.warning(f"Error filling field {field_id}: {e}")

        # --- Handle Yes/No questions ---
        yes_no_fields = [
            '2dad4788-1915-4348-8891-7fd4756fe97c',  # Timezone
            'dacaf08c-8fa5-41ce-ab88-ad54a5e0d5ec',  # 5+ years frontend
            '7e0074c4-e91f-4416-9cdd-178953fb90d4'   # Design system contributions
        ]

        for field_id in yes_no_fields:
            logger.info(f"Attempting to fill field: {field_id}")
            try:
                # Find the parent container div for this question
                question_container_div = WebDriverWait(form, 5).until(
                    EC.presence_of_element_located((By.XPATH, f'.//label[@for="{field_id}"]/ancestor::div[@class="_fieldEntry_hkyf8_29 ashby-application-form-field-entry"]'))
                )

                # Find and click the 'Yes' button within this specific question's container
                yes_button = WebDriverWait(question_container_div, 5).until(
                    EC.element_to_be_clickable((By.XPATH, './/button[contains(text(), "Yes")]'))
                )
                yes_button.click()
                logger.info(f"Successfully clicked 'Yes' for field: {field_id}")
            except Exception as e:
                logger.warning(f"Error clicking 'Yes' for field {field_id}: {e}")

        # --- Handle Resume Upload ---
        resume_field_id = '_systemfield_resume'
        logger.info(f"Attempting to upload resume for field: {resume_field_id}")
        
        if not resume_path:
            logger.warning(f"Skipping resume upload for {resume_field_id}: No resume path provided.")
        elif not os.path.exists(resume_path):
             logger.warning(f"Skipping resume upload for {resume_field_id}: File not found at {resume_path}.")
        else:
            try:
                # Find the file input element by its ID
                # Note: file inputs can sometimes be invisible or replaced by custom buttons.
                # Sending keys to the input element is the standard way to upload.
                logger.info(f"Finding resume file input with ID: {resume_field_id}")
                resume_input = WebDriverWait(form, 10).until(
                    EC.presence_of_element_located((By.ID, resume_field_id))
                )
                
                # Send the file path to the input element
                logger.info(f"Sending file path {resume_path} to input element.")
                resume_input.send_keys(resume_path)
                logger.info(f"Successfully sent file path for resume upload: {resume_path}")
                # Note: Visual confirmation of upload might require checking for specific elements or text on the page.
                
            except Exception as e:
                logger.warning(f"Error uploading resume file for field {resume_field_id} at path {resume_path}: {e}")

        logger.info("Finished filling application form")
        
        # Add 5 second sleep after filling all fields
        logger.info("Waiting 7 seconds after filling fields...")
        time.sleep(7)
        
        return True # Indicate success

    except Exception as e:
        logger.error(f"Error during form filling: {e}")
        # Do not raise here, let the main script handle driver quit
        return False # Indicate failure 