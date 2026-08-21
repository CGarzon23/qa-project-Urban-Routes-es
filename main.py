from time import sleep

import data
import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


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
        self.driver.find_element(*self.phone_code_field).send_keys(retrieve_phone_code(self.driver))
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


class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        options = webdriver.ChromeOptions()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.get(data.urban_routes_url)
        time.sleep(2)
        cls.home_page = UrbanRoutesPage(cls.driver)


    def test_set_route(self):
        address_from = data.address_from
        address_to = data.address_to
        self.home_page.set_from(address_from)
        self.home_page.set_to(address_to)
        assert self.home_page.get_from() == address_from
        assert self.home_page.get_to() == address_to

    def test_set_comfort(self):
        self.home_page.set_comfort()
        assert "active" in self.home_page.get_comfort()

    def test_set_phone_number(self):
        self.home_page.set_phone_number(data.phone_number)
        assert self.home_page.get_phone_number() == data.phone_number

    def test_add_credit_card(self):
        self.home_page.set_credit_card()

    def test_add_driver_message(self):
        self.home_page.set_driver_message()

    def test_add_blankets_scarves(self):
        self.home_page.set_blankets_scarves()

    def test_add_ice_cream(self):
        self.home_page.set_ice_cream()

    def test_reserve_vehicle(self):
        self.home_page.set_reserve_vehicle()

    def test_driver_accept(self):
        self.home_page.driver_assigned()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

