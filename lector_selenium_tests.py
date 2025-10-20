"""
Automated Black Box TestinBASE_URL = "http://localhost:5183"  
CREATE_URL = f"{BASE_URL}/Usuario/Create"
INDEX_URL = f"{BASE_URL}/Usuario/Index"
WAIT_TIMEOUT = 10

# Validation Rules (from Entity Model)
VALIDATIONS = {
    'primer_nombre': {
        'required': True,
        'min_length': 3,
        'max_length': 25,
        'error_messages': {
            'required': 'El primer nombre es obligatorio',
            'length': 'El primer nombre debe contener entre 3 a 25 caracteres'
        }
    },D - Create Operation
Using Selenium WebDriver with Python

Test Cases: 35 tests based on pairwise equivalence class partitioning
Date: October 20, 2025
"""

import csv
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('lector_tests.log'),
        logging.StreamHandler()
    ]
)

BASE_URL = "http://localhost:5183"  
CREATE_URL = f"{BASE_URL}/Usuario/Create"
INDEX_URL = f"{BASE_URL}/Usuario/Index"
WAIT_TIMEOUT = 10

# Validation Rules (from Entity Model)
VALIDATIONS = {
    'primer_nombre': {
        'required': True,
        'min_length': 1,
        'max_length': 25,
        'error_messages': {
            'required': 'El primer nombre es obligatorio',
            'length': 'El primer nombre debe contener entre 1 y 25 caracteres'
        }
    },
    'segundo_nombre': {
        'required': False,
        'min_length': 3,
        'max_length': 25,
        'error_messages': {
            'length': 'El segundo nombre debe contener entre 3 a 25 caracteres'
        }
    },
    'primer_apellido': {
        'required': True,
        'min_length': 3,
        'max_length': 25,
        'error_messages': {
            'required': 'El primer apellido es obligatorio',
            'length': 'El primer apellido debe contener entre 3 a 25 caracteres'
        }
    },
    'segundo_apellido': {
        'required': False,
        'min_length': 3,
        'max_length': 25,
        'error_messages': {
            'length': 'El segundo apellido debe contener entre 3 a 25 caracteres'
        }
    },
    'ci': {
        'required': True,
        'min_length': 6,
        'max_length': 10,
        'pattern': r'^\d+$',
        'error_messages': {
            'required': 'El número de cédula es obligatorio',
            'length': 'El número de cédula debe contener entre 6 a 10 dígitos',
            'pattern': 'El CI solo puede contener números',
            'duplicate': 'Ya existe un lector con este CI'
        }
    },
    'telefono': {
        'required': True,
        'min_length': 8,
        'max_length': 10,
        'pattern': r'^\d+$',
        'error_messages': {
            'required': 'El número de teléfono es obligatorio',
            'length': 'El teléfono debe contener entre 8 a 10 caracteres',
            'pattern': 'El teléfono solo puede contener números'
        }
    },
    'correo': {
        'required': True,
        'min_length': 5,
        'max_length': 45,
        'pattern': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        'error_messages': {
            'required': 'El correo electrónico es obligatorio',
            'length': 'El correo electrónico debe contener entre 5 a 45 caracteres',
            'pattern': 'El correo debe tener un formato válido'
        }
    }
}


class LectorTestRunner:
    """Test runner for Lector CRUD automated tests"""
    
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.driver = None
        self.wait = None
        self.test_results = []
        
    def setup(self):
        """Initialize WebDriver"""
        logging.info("Setting up WebDriver...")
        options = webdriver.FirefoxOptions()
        # Uncomment the line below to run headless
        # options.add_argument('--headless')
        options.add_argument('--width=1920')
        options.add_argument('--height=1080')
        
        # Use webdriver_manager to automatically download and manage geckodriver
        service = FirefoxService(GeckoDriverManager().install())
        self.driver = webdriver.Firefox(service=service, options=options)
        self.wait = WebDriverWait(self.driver, WAIT_TIMEOUT)
        logging.info("WebDriver initialized successfully")
        
    def teardown(self):
        """Close WebDriver"""
        if self.driver:
            logging.info("Closing WebDriver...")
            self.driver.quit()
            
    def parse_test_value(self, value):
        """
        Parse test values from CSV format
        Examples:
        - "A" x 25 -> "AAAA..." (25 times)
        - "Juan" -> "Juan"
        - "" -> ""
        """
        if not value or value.strip() == '""':
            return ""
            
        # Remove surrounding quotes
        value = value.strip().strip('"')
        
        # Check for repetition pattern: "X" x N
        if ' x ' in value:
            parts = value.split(' x ')
            if len(parts) == 2:
                char = parts[0].strip().strip('"')
                try:
                    count = int(parts[1].strip())
                    return char * count
                except ValueError:
                    pass
                    
        return value
    
    def navigate_to_create_page(self):
        """Navigate to the Create Lector page"""
        logging.info(f"Navigating to {CREATE_URL}")
        self.driver.get(CREATE_URL)
        time.sleep(1)  # Wait for page load
        
    def fill_form(self, test_data):
        """Fill the form with test data"""
        logging.info(f"Filling form with data: {test_data}")
        
        # Parse all values
        primer_nombre = self.parse_test_value(test_data.get('Primer Nombre', ''))
        segundo_nombre = self.parse_test_value(test_data.get('Segundo Nombre', ''))
        primer_apellido = self.parse_test_value(test_data.get('Primer Apellido', ''))
        segundo_apellido = self.parse_test_value(test_data.get('Segundo Apellido', ''))
        ci = self.parse_test_value(test_data.get('CI', ''))
        telefono = self.parse_test_value(test_data.get('Telefono', ''))
        correo = self.parse_test_value(test_data.get('Correo', ''))
        
        # Fill Primer Nombre
        if primer_nombre:
            field = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='primernombre']")
            field.clear()
            field.send_keys(primer_nombre)
            logging.debug(f"Primer Nombre: {primer_nombre}")
            
        # Fill Segundo Nombre
        if segundo_nombre:
            field = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='segundonombre']")
            field.clear()
            field.send_keys(segundo_nombre)
            logging.debug(f"Segundo Nombre: {segundo_nombre}")
            
        # Fill Primer Apellido
        if primer_apellido:
            field = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='primerapellido']")
            field.clear()
            field.send_keys(primer_apellido)
            logging.debug(f"Primer Apellido: {primer_apellido}")
            
        # Fill Segundo Apellido
        if segundo_apellido:
            field = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='segundoapellido']")
            field.clear()
            field.send_keys(segundo_apellido)
            logging.debug(f"Segundo Apellido: {segundo_apellido}")
            
        # Fill CI
        if ci:
            field = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='ci']")
            field.clear()
            field.send_keys(ci)
            logging.debug(f"CI: {ci}")
            
        # Fill Teléfono
        if telefono:
            field = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='telefono']")
            field.clear()
            field.send_keys(telefono)
            logging.debug(f"Teléfono: {telefono}")
            
        # Fill Correo
        if correo:
            field = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='correo']")
            field.clear()
            field.send_keys(correo)
            logging.debug(f"Correo: {correo}")
    
    def submit_form(self):
        """Submit the form"""
        logging.info("Submitting form...")
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='submit-button']")
        submit_button.click()
        time.sleep(2)  # Wait for submission and validation
        
    def check_validation_errors(self):
        """
        Check for validation error messages
        Returns: dict with field names as keys and error messages as values
        """
        errors = {}
        
        # Check all error spans
        error_fields = ['primernombre', 'segundonombre', 'primerapellido', 'segundoapellido', 
                       'ci', 'telefono', 'correo']
        
        for field in error_fields:
            try:
                error_element = self.driver.find_element(
                    By.CSS_SELECTOR, 
                    f"[data-testid='{field}-error']"
                )
                error_text = error_element.text.strip()
                if error_text:
                    errors[field] = error_text
                    logging.debug(f"Error found in {field}: {error_text}")
            except NoSuchElementException:
                continue
                
        return errors
    
    def is_on_index_page(self):
        """Check if redirected to Index page (success)"""
        try:
            current_url = self.driver.current_url
            is_index = '/Usuario/Index' in current_url or current_url.endswith('/Usuario')
            return is_index
        except:
            return False
    
    def determine_actual_result(self, has_errors, on_index):
        """Determine if test should pass or fail"""
        if on_index and not has_errors:
            return "Aceptado"
        else:
            return "Rechazado"
    
    def run_test_case(self, test_case):
        """
        Run a single test case
        Returns: dict with test results
        """
        caso = test_case.get('CASO', 'Unknown')
        expected = test_case.get('Resultado Esperado', '').strip()
        
        logging.info(f"\n{'='*60}")
        logging.info(f"Running Test Case: {caso}")
        logging.info(f"Expected Result: {expected}")
        logging.info(f"{'='*60}")
        
        result = {
            'caso': caso,
            'expected': expected,
            'actual': '',
            'passed': False,
            'errors': [],
            'notes': ''
        }
        
        try:
            # Navigate to create page
            self.navigate_to_create_page()
            
            # Fill form
            self.fill_form(test_case)
            
            # Submit form
            self.submit_form()
            
            # Check for errors
            errors = self.check_validation_errors()
            
            # Check if on index page
            on_index = self.is_on_index_page()
            
            # Determine actual result
            actual = self.determine_actual_result(len(errors) > 0, on_index)
            
            result['actual'] = actual
            result['errors'] = errors
            result['passed'] = (actual == expected)
            
            if on_index:
                result['notes'] = 'Redirected to Index page (creation successful)'
            elif errors:
                error_summary = ', '.join([f"{field}: {msg}" for field, msg in errors.items()])
                result['notes'] = f'Validation errors: {error_summary}'
            else:
                result['notes'] = 'Stayed on Create page, but no errors detected'
            
            # Log result
            status = "✓ PASSED" if result['passed'] else "✗ FAILED"
            logging.info(f"Result: {status}")
            logging.info(f"Expected: {expected}, Actual: {actual}")
            if errors:
                logging.info(f"Errors: {errors}")
            logging.info(f"Notes: {result['notes']}")
            
        except Exception as e:
            logging.error(f"Exception in test {caso}: {str(e)}")
            result['actual'] = 'Error'
            result['passed'] = False
            result['notes'] = f'Exception: {str(e)}'
            
        self.test_results.append(result)
        return result
    
    def run_all_tests(self, csv_file_path):
        """
        Run all test cases from CSV file
        """
        logging.info(f"Loading test cases from: {csv_file_path}")
        
        try:
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                test_cases = list(reader)
                
            logging.info(f"Loaded {len(test_cases)} test cases")
            
            # Setup WebDriver
            self.setup()
            
            # Run each test
            for i, test_case in enumerate(test_cases, 1):
                logging.info(f"\nTest {i}/{len(test_cases)}")
                self.run_test_case(test_case)
                time.sleep(1)  # Small delay between tests
                
        except FileNotFoundError:
            logging.error(f"CSV file not found: {csv_file_path}")
            raise
        except Exception as e:
            logging.error(f"Error running tests: {str(e)}")
            raise
        finally:
            # Teardown WebDriver
            self.teardown()
            
    def generate_report(self, output_file='lector_test_results.csv'):
        """Generate test results report"""
        logging.info(f"\nGenerating report: {output_file}")
        
        # Calculate statistics
        total = len(self.test_results)
        passed = sum(1 for r in self.test_results if r['passed'])
        failed = total - passed
        pass_rate = (passed / total * 100) if total > 0 else 0
        
        # Write results to CSV
        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['caso', 'expected', 'actual', 'passed', 'notes']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            writer.writeheader()
            for result in self.test_results:
                writer.writerow({
                    'caso': result['caso'],
                    'expected': result['expected'],
                    'actual': result['actual'],
                    'passed': 'PASS' if result['passed'] else 'FAIL',
                    'notes': result['notes']
                })
        
        # Print summary
        logging.info("\n" + "="*60)
        logging.info("TEST EXECUTION SUMMARY")
        logging.info("="*60)
        logging.info(f"Total Tests: {total}")
        logging.info(f"Passed: {passed} ({pass_rate:.1f}%)")
        logging.info(f"Failed: {failed} ({100-pass_rate:.1f}%)")
        logging.info("="*60)
        
        # Print failed tests
        if failed > 0:
            logging.info("\nFAILED TESTS:")
            for result in self.test_results:
                if not result['passed']:
                    logging.info(f"  - {result['caso']}: Expected '{result['expected']}', Got '{result['actual']}'")
                    logging.info(f"    Notes: {result['notes']}")
        
        logging.info(f"\nDetailed results saved to: {output_file}")
        
        return {
            'total': total,
            'passed': passed,
            'failed': failed,
            'pass_rate': pass_rate
        }


def main():
    """Main function to run the test suite"""
    print("="*60)
    print("LECTOR CRUD - AUTOMATED BLACK BOX TESTING")
    print("Selenium WebDriver + Python")
    print("="*60)
    print()
    
    # Configuration
    csv_file = 'BLACKBOX_BIBLIOTECA - LECTOR_TESTS.csv'
    
    # Ask user for CSV file path
    user_input = input(f"Enter CSV file path (default: {csv_file}): ").strip()
    if user_input:
        csv_file = user_input
    
    # Ask for base URL
    url_input = input(f"Enter application URL (default: {BASE_URL}): ").strip()
    base_url = url_input if url_input else BASE_URL
    
    print(f"\nTest Configuration:")
    print(f"  - CSV File: {csv_file}")
    print(f"  - Base URL: {base_url}")
    print(f"  - Create URL: {base_url}/Lector/Create")
    print()
    
    input("Press Enter to start testing...")
    
    # Create test runner
    runner = LectorTestRunner(base_url=base_url)
    
    try:
        # Run all tests
        runner.run_all_tests(csv_file)
        
        # Generate report
        stats = runner.generate_report('lector_test_results.csv')
        
        print("\n" + "="*60)
        print("TESTING COMPLETED!")
        print("="*60)
        print(f"Results saved to: lector_test_results.csv")
        print(f"Logs saved to: lector_tests.log")
        print()
        
        return stats['passed'] == stats['total']  # Return success if all passed
        
    except Exception as e:
        logging.error(f"Test execution failed: {str(e)}")
        return False


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)