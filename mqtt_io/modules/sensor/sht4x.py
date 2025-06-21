"""
SHT4x temperature and humidity sensor
"""

from typing import cast

from ...types import ConfigType, SensorValueType
from . import GenericSensor
from ...exceptions import RuntimeConfigError

REQUIREMENTS = ("adafruit-circuitpython-sht4x","adafruit-extended-bus")

CONFIG_SCHEMA = {
    "i2c_bus_num": {"type": "integer", "required": True, "empty": False},
}

class Sensor(GenericSensor):
    """
    Implementation of Sensor class for sht4x.
    """

    SENSOR_SCHEMA = {
        "type": {
            "type": 'string',
            "required": False,
            "empty": False,
            "default": 'temperature',
            "allowed": ['temperature', 'humidity'],
        }
    }

    def setup_module(self) -> None:
        # pylint: disable=import-outside-toplevel,import-error
        import adafruit_sht4x  # type: ignore
        from adafruit_extended_bus import ExtendedI2C as I2C

        self.bus_num: int = self.config["i2c_bus_num"]
        i2c = I2C(self.bus_num)
        
        self.sensor = adafruit_sht4x.SHT4x(i2c)

    @property
    def _temperature(self) -> SensorValueType:
        return cast(SensorValueType, self.sensor.temperature)

    @property
    def _humidity(self) -> SensorValueType:
        return cast(SensorValueType, self.sensor.relative_humidity)

    def get_value(self, sens_conf: ConfigType) -> SensorValueType:
        """
        Get the temperature value from the sensor
        """
        if sens_conf["type"] == "temperature":
            return self._temperature
        if sens_conf["type"] == "humidity":
            return self._humidity
        raise RuntimeConfigError(
            "sht4x sensor '%s' was not configured to return 'temperature' or 'humidity'"
            % sens_conf["name"]
        )
