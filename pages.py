import time
import data
import helpers
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

class UrbanRoutesPage:
    # Setup básico
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    flash_field = (By.XPATH, "//button[text()='Pedir un taxi']")
    pick_comfort = (By.XPATH, "//div[contains(@class, 'tcard')][.//div[text()='Comfort']]")
    phone_field = (By.CLASS_NAME, 'np-button' )
    phone_number_field = (By.ID, "phone")
    phone_next_button = (By.XPATH, "//button[text()='Siguiente']")
    phone_code_field = (By.ID, "code")
    phone_confirmation_button = (By.XPATH, "/html/body/div/div/div[1]/div[2]/div[2]/form/div[2]/button[1]")
    # Interacciones para el método de pago
    payment_method = (By.CLASS_NAME, 'pp-text')
    add_payment_method = (By.XPATH, "//div[contains(@class,'pp-row')][.//div[text()='Agregar tarjeta']]")
    payment_method_number = (By.XPATH, "//div[contains(@class,'card-number-input')]//input[@id='number']")
    payment_method_code = (By.XPATH, "//div[contains(@class,'card-code-input')]//input[@id='code']")
    payment_method_confirm = (By.XPATH, "//div[contains(@class,'pp-buttons')]//button[normalize-space()='Agregar']")
    payment_method_close = (By.XPATH, "//div[contains(@class,'section')][.//div[normalize-space()='Método de pago']]//button[contains(@class,'close-button')]")
    # Interacciones para el mensaje al conductor
    driver_message_field = (By.XPATH, "//div[contains(@class,'input-container')][.//label[normalize-space()='Mensaje para el conductor...']]//input")
    # Interacciones para pedir la manta y los pañuelos
    blanket_button = (By.XPATH,"//div[contains(@class,'r-sw-container')][.//div[normalize-space()='Manta y pañuelos']]//span[contains(@class,'slider')]")
    # Interacciones para agregar helado
    add_ice_cream = (By.CLASS_NAME, "counter-plus")
    # Interacciones para reservar
    reserve_button = (By.XPATH,"//button[.//span[normalize-space()='Pedir un taxi']]")


    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_comfort(self):
        address_from = data.address_from
        address_to = data.address_to
        self.set_from(address_from)
        self.set_to(address_to)
        WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(self.flash_field))
        self.driver.find_element(*self.flash_field).click()
        self.driver.find_element(*self.pick_comfort).click()

    def get_comfort(self):
        return self.driver.find_element(*self.pick_comfort).get_attribute('class')

    def set_phone_number(self, phone_number):
        self.set_comfort()
        self.driver.find_element(*self.phone_field).click()
        self.driver.find_element(*self.phone_number_field).send_keys(phone_number)
        self.driver.find_element(*self.phone_next_button).click()
        WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(self.phone_code_field))
        self.driver.find_element(*self.phone_code_field).send_keys(helpers.retrieve_phone_code(self.driver))
        self.driver.find_element(*self.phone_confirmation_button).click()

    def get_phone_number(self):
        return self.driver.find_element(*self.phone_number_field).get_property('value')

    def set_credit_card(self):
        self.set_phone_number(data.phone_number)
        self.driver.find_element(*self.payment_method).click()
        self.driver.find_element(*self.add_payment_method).click()
        self.driver.find_element(*self.payment_method_number).send_keys(data.card_number)
        self.driver.find_element(*self.payment_method_code).send_keys(data.card_code)
        self.driver.find_element(*self.payment_method_code).send_keys(Keys.TAB)
        self.driver.find_element(*self.payment_method_confirm).click()
        self.driver.find_element(*self.payment_method_close).click()

    def set_driver_message(self):
        self.set_credit_card()
        self.driver.find_element(*self.driver_message_field).send_keys(data.message_for_driver)

    def set_blankets_scarves(self):
        self.set_driver_message()
        self.driver.find_element(*self.blanket_button).click()

    def set_ice_cream(self):
        self.set_blankets_scarves()
        self.driver.find_element(*self.add_ice_cream).click()
        self.driver.find_element(*self.add_ice_cream).click()


    def set_reserve_vehicle(self):
        self.set_ice_cream()
        self.driver.find_element(*self.reserve_button).click()

    def driver_assigned(self):
        self.set_reserve_vehicle()
        def is_driver_assigned(driver):
            return driver.find_element(By.CLASS_NAME,"order-header-title").text != "Buscar automóvil"
        WebDriverWait(self.driver, 60).until(is_driver_assigned)
        time.sleep(5)