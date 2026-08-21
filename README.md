# Urban Routes - QA Automation

## Descripción del proyecto

Proyecto de automatización de pruebas para **Urban Routes**, una aplicación web de planificación y solicitud de viajes.

Las pruebas automatizan un flujo de reserva utilizando Selenium y verifican distintas funcionalidades de la interfaz, entre ellas:

- Configuración de las direcciones de origen y destino.
- Selección de la tarifa **Comfort**.
- Registro y confirmación del número de teléfono.
- Configuración del método de pago mediante tarjeta.
- Introducción de un mensaje para el conductor.
- Activación de requisitos del viaje, como **Manta y pañuelos**.
- Selección de dos unidades de helado mediante un contador.
- Solicitud del taxi.
- Espera hasta que el estado del modal cambie de búsqueda de automóvil a información del viaje.

## Tecnologías y técnicas utilizadas

### Python

Lenguaje utilizado para desarrollar las pruebas automatizadas y la estructura del Page Object Model.

### Selenium WebDriver

Se utiliza para controlar Chrome y automatizar las interacciones con Urban Routes, incluyendo:

- Localización de elementos.
- Escritura en campos de entrada.
- Clics sobre botones y controles.
- Lectura de valores de los elementos.
- Comprobación de estados de la interfaz.

### Pytest

Framework utilizado para ejecutar y organizar las pruebas mediante clases y métodos con nombres `test_*`.

### Page Object Model (POM)

La clase `UrbanRoutesPage` representa la página y centraliza los localizadores y las acciones realizadas sobre sus elementos.

Los elementos de la página se almacenan como atributos de clase, por ejemplo:

```python
from_field = (By.ID, 'from')
pick_comfort = (By.XPATH, "//div[contains(@class, 'tcard')][.//div[text()='Comfort']]")
```

Las acciones se encapsulan en métodos como:

```python
set_from()
set_to()
set_comfort()
set_credit_card()
set_driver_message()
set_blankets_scarves()
set_ice_cream()
set_reserve_vehicle()
```

### XPath y localizadores Selenium

Se utilizan distintos tipos de localizadores, principalmente:

- `By.ID`
- `By.CLASS_NAME`
- `By.XPATH`

Para algunos elementos se utilizan XPath basados en el elemento padre y el texto de un elemento hijo, con `contains()` y `normalize-space()` para hacer los localizadores más resistentes a cambios menores del HTML.

### Esperas explícitas

Se utiliza `WebDriverWait` junto con `expected_conditions` para esperar a que determinados elementos estén presentes antes de interactuar con ellos.

También se implementa una espera personalizada para comprobar que el encabezado del modal deje de mostrar **"Buscar automóvil"**, indicando que el estado del viaje ha cambiado.

 y Chrome DevTools Protocol para obtener el código de confirmación telefónica generado por la aplicación.

## Estructura general

El archivo principal contiene:

- `retrieve_phone_code()` — obtiene el código de confirmación telefónica.
- `UrbanRoutesPage` — Page Object con localizadores y métodos de interacción.
- `TestUrbanRoutes` — conjunto de pruebas ejecutadas con pytest.

Los datos utilizados por las pruebas se importan desde el módulo `data`.

## Requisitos previos

Antes de ejecutar las pruebas, se necesita:

1. Python instalado.
2. Google Chrome instalado.
3. Un entorno virtual con las dependencias del proyecto.
4. Selenium instalado.
5. Pytest instalado.
6. El archivo `data.py` con los datos requeridos por las pruebas, incluida `urban_routes_url`, las direcciones y los datos utilizados durante el flujo.

## Instalación

Desde la carpeta del proyecto, crear y activar un entorno virtual si todavía no existe:

```bash
python -m venv .venv
```

En Git Bash para Windows:

```bash
source .venv/Scripts/activate
```

Instalar las dependencias principales:

```bash
python -m pip install selenium pytest
```

## Ejecución de las pruebas

Desde la carpeta raíz del proyecto, con el entorno virtual activado:

```bash
pytest
```

También se puede ejecutar pytest mediante Python:

```bash
python -m pytest
```

Para ejecutar específicamente `main.py`:

```bash
pytest main.py
```

Para ejecutar una prueba concreta:

```bash
pytest main.py::TestUrbanRoutes::test_set_route
```

Ejemplo para la prueba de aceptación del conductor:

```bash
pytest main.py::TestUrbanRoutes::test_driver_accept
```

## Notas

La configuración de Chrome utilizada en `setup_class()` habilita los logs de rendimiento porque son necesarios para recuperar el código de confirmación mediante `retrieve_phone_code()`.

La prueba `test_driver_accept` realiza el flujo de reserva y después espera hasta 60 segundos a que el texto del encabezado del modal deje de ser **"Buscar automóvil"**. Esto permite comprobar el cambio de estado del modal cuando se asigna el viaje.
