import pages
import data
import time
from selenium import webdriver

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
        cls.home_page = pages.UrbanRoutesPage(cls.driver)


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