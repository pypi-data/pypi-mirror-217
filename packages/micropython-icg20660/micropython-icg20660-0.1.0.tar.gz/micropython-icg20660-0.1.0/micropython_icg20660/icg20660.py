# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT
"""
`icg20660`
================================================================================

MicroPython Driver for the TDK ICG20660 Accelerometer/Gyro sensor


* Author(s): Jose D. Montoya


"""

import time
from micropython import const
from micropython_icg20660.i2c_helpers import CBits, RegisterStruct

try:
    from typing import Tuple
except ImportError:
    pass


__version__ = "0.1.0"
__repo__ = "https://github.com/jposada202020/MicroPython_ICG20660.git"

_DEVICE_ID = const(0x75)
_GYRO_CONFIG = const(0x1B)
_CONFIG = const(0x1A)
_SMPLRT_DIV = const(0x19)
_ACCEL_CONFIG = const(0x1C)
_ACCEL_XOUT_H = const(0x3B)  # first byte of accel data
_GYRO_XOUT_H = const(0x43)  # first byte of accel data
_PWR_MGMT_1 = const(0x6B)

GYRO_DLPF_DISABLED = const(0b10)
GYRO_DLPF_ENABLED = const(0b00)
gyro_dlpf_mode_values = (GYRO_DLPF_DISABLED, GYRO_DLPF_ENABLED)

DLPF_CFG_0 = const(0b000)
DLPF_CFG_1 = const(0b001)
DLPF_CFG_2 = const(0b010)
DLPF_CFG_7 = const(0b111)
gyro_dlpf_configuration_values = (DLPF_CFG_0, DLPF_CFG_1, DLPF_CFG_2, DLPF_CFG_7)

FS_125_DPS = const(0b00)
FS_250_DPS = const(0b01)
FS_500_DPS = const(0b10)
gyro_full_scale_values = (FS_125_DPS, FS_250_DPS, FS_500_DPS)
gyro_full_scale_sensitivity = (262, 131, 65.5)

rate_values = {
    500.0: 1,
    250.0: 3,
    200.0: 4,
    125.0: 7,
    100.0: 9,
    62.5: 15,
    50.0: 19,
    31.3: 31,
    15.6: 63,
    10.0: 99,
    7.8: 127,
    3.9: 255,
}
data_rate_values = (
    500.0,
    250.0,
    200.0,
    125.0,
    100.0,
    62.5,
    50.0,
    31.3,
    15.6,
    10.0,
    7.8,
    3.9,
)
rate_divisor_values = (1, 3, 4, 7, 9, 15, 19, 31, 63, 99, 127, 255)

RANGE_2G = const(0b00)
RANGE_4G = const(0b01)
RANGE_8G = const(0b10)
RANGE_16G = const(0b11)
acceleration_range_values = (RANGE_2G, RANGE_4G, RANGE_8G, RANGE_16G)
acc_range_sensitivity = (16384, 8192, 4096, 2048)


class ICG20660:
    """Driver for the ICG20660 Sensor connected over I2C.

    :param ~machine.I2C i2c: The I2C bus the ICG20660 is connected to.
    :param int address: The I2C device address. Defaults to :const:`0x69`

    :raises RuntimeError: if the sensor is not found

    **Quickstart: Importing and using the device**

    Here is an example of using the :class:`ICG20660` class.
    First you will need to import the libraries to use the sensor

    .. code-block:: python

        from machine import Pin, I2C
        from micropython_icg20660 import icg20660

    Once this is done you can define your `machine.I2C` object and define your sensor object

    .. code-block:: python

        i2c = I2C(1, sda=Pin(2), scl=Pin(3))
        icg20660 = icg20660.ICG20660(i2c)

    Now you have access to the attributes

    .. code-block:: python

    """

    _device_id = RegisterStruct(_DEVICE_ID, "B")
    _rate_divisor = RegisterStruct(_SMPLRT_DIV, "B")

    _sleep = CBits(1, _PWR_MGMT_1, 6)

    _gyro_full_scale = CBits(2, _CONFIG, 3)
    _gyro_dlpf_configuration = CBits(3, _CONFIG, 0)
    _gyro_dlpf_mode = CBits(2, _GYRO_CONFIG, 0)
    _acceleration_range = CBits(2, _ACCEL_CONFIG, 3)

    _raw_accel_data = RegisterStruct(_ACCEL_XOUT_H, ">hhh")
    _raw_gyro_data = RegisterStruct(_GYRO_XOUT_H, ">hhh")

    def __init__(self, i2c, address: int = 0x69) -> None:
        self._i2c = i2c
        self._address = address

        if self._device_id != 0x91:
            raise RuntimeError("Failed to find ICG20660")

        self._sleep = 0
        self.gyro_full_scale = FS_125_DPS
        self.acceleration_range = RANGE_2G

    @property
    def gyro_dlpf_mode(self) -> str:
        """
        Sensor gyro_dlpf_mode. Enables gyro DLPF

        +-----------------------------------------+------------------+
        | Mode                                    | Value            |
        +=========================================+==================+
        | :py:const:`icg20660.GYRO_DLPF_DISABLED` | :py:const:`0b10` |
        +-----------------------------------------+------------------+
        | :py:const:`icg20660.GYRO_DLPF_ENABLED`  | :py:const:`0b00` |
        +-----------------------------------------+------------------+
        """
        values = ("GYRO_DLPF_DISABLED", "N/A", "GYRO_DLPF_ENABLED")
        return values[self._gyro_dlpf_mode]

    @gyro_dlpf_mode.setter
    def gyro_dlpf_mode(self, value: int) -> None:
        if value not in gyro_dlpf_mode_values:
            raise ValueError("Value must be a valid gyro_dlpf_mode setting")
        self._gyro_dlpf_mode = value

    @property
    def gyro_dlpf_configuration(self) -> str:
        """
        Sensor gyro_dlpf_configuration. For this to have an effect,
        :attr:`gyro_dlpf_mode` must be enabled. The gyroscope and
        temperature sensor will be filtered. For more details please
        refer to the datasheet.

        +---------------------------------+-------------------+
        | Mode                            | Value             |
        +=================================+===================+
        | :py:const:`icg20660.DLPF_CFG_0` | :py:const:`0b000` |
        +---------------------------------+-------------------+
        | :py:const:`icg20660.DLPF_CFG_1` | :py:const:`0b001` |
        +---------------------------------+-------------------+
        | :py:const:`icg20660.DLPF_CFG_2` | :py:const:`0b010` |
        +---------------------------------+-------------------+
        | :py:const:`icg20660.DLPF_CFG_7` | :py:const:`0b111` |
        +---------------------------------+-------------------+
        """
        values = ("DLPF_CFG_0", "DLPF_CFG_1", "DLPF_CFG_2", "DLPF_CFG_7")
        return values[self._gyro_dlpf_configuration]

    @gyro_dlpf_configuration.setter
    def gyro_dlpf_configuration(self, value: int) -> None:
        if value not in gyro_dlpf_configuration_values:
            raise ValueError("Value must be a valid dlpf_configuration setting")
        self._gyro_dlpf_configuration = value

    @property
    def gyro_full_scale(self) -> str:
        """
        Sensor gyro_full_scale

        +---------------------------------+------------------+
        | Mode                            | Value            |
        +=================================+==================+
        | :py:const:`icg20660.FS_125_DPS` | :py:const:`0b00` |
        +---------------------------------+------------------+
        | :py:const:`icg20660.FS_250_DPS` | :py:const:`0b01` |
        +---------------------------------+------------------+
        | :py:const:`icg20660.FS_500_DPS` | :py:const:`0b10` |
        +---------------------------------+------------------+
        """
        values = ("FS_125_DPS", "FS_250_DPS", "FS_500_DPS")
        return values[self._gyro_full_scale]

    @gyro_full_scale.setter
    def gyro_full_scale(self, value: int) -> None:
        if value not in gyro_full_scale_values:
            raise ValueError("Value must be a valid gyro_full_scale setting")
        self._gyro_full_scale = value
        self._memory_gyro_fs = value

    @property
    def data_rate(self):
        """The rate at which sensor measurements are taken in Hz"""
        return list(rate_values.keys())[
            list(rate_values.values()).index(self.data_rate_divisor)
        ]

    @data_rate.setter
    def data_rate(self, value):
        """
        .. note::

            The data rates are set indirectly by setting a rate divisor according to the
            following formula:

            .. math::

                \\text{data_rate } = \\frac{1000}{1 + divisor}

                Accepted values are:

        | * 500.0
        | * 250.0
        | * 200.0
        | * 125.0
        | * 100.0
        | * 62.5
        | * 50.0
        | * 31.3
        | * 15.6
        | * 10.0
        | * 7.8
        | * 3.9

        """
        if value not in data_rate_values:
            raise ValueError("Data rate must be a valid setting")

        self.data_rate_divisor = rate_values[value]

    @property
    def data_rate_divisor(self):
        """
        Accepted values are:

        | * 1
        | * 3
        | * 4
        | * 7
        | * 9
        | * 15
        | * 19
        | * 31
        | * 63
        | * 99
        | * 127
        | * 255

        """

        raw_rate_divisor = self._rate_divisor

        return raw_rate_divisor

    @data_rate_divisor.setter
    def data_rate_divisor(self, value):
        if value not in rate_divisor_values:
            raise ValueError("Value must be a valid data rate divisor setting")

        self._rate_divisor = value

    @property
    def acceleration_range(self) -> str:
        """
        Sensor acceleration_range

        +--------------------------------+------------------+
        | Mode                           | Value            |
        +================================+==================+
        | :py:const:`icg20660.RANGE_2G`  | :py:const:`0b00` |
        +--------------------------------+------------------+
        | :py:const:`icg20660.RANGE_4G`  | :py:const:`0b01` |
        +--------------------------------+------------------+
        | :py:const:`icg20660.RANGE_8G`  | :py:const:`0b10` |
        +--------------------------------+------------------+
        | :py:const:`icg20660.RANGE_16G` | :py:const:`0b11` |
        +--------------------------------+------------------+
        """
        values = ("RANGE_2G", "RANGE_4G", "RANGE_8G", "RANGE_16G")
        return values[self._acceleration_range]

    @acceleration_range.setter
    def acceleration_range(self, value: int) -> None:
        if value not in acceleration_range_values:
            raise ValueError("Value must be a valid acceleration_range setting")
        self._acceleration_range = value
        self._memory_accel_range = value

    @property
    def acceleration(self) -> Tuple[float, float, float]:
        """
        Acceleration Property. The x, y, z acceleration values returned in a 3-tuple
        and are in :math:`m / s ^ 2.`
        :return: Acceleration Values
        """
        raw_measurement = self._raw_accel_data
        time.sleep(0.005)
        x = (
            raw_measurement[0]
            / acc_range_sensitivity[self._memory_accel_range]
            * 9.80665
        )
        y = (
            raw_measurement[1]
            / acc_range_sensitivity[self._memory_accel_range]
            * 9.80665
        )
        z = (
            raw_measurement[2]
            / acc_range_sensitivity[self._memory_accel_range]
            * 9.80665
        )

        return x, y, z

    @property
    def gyro(self):
        """
        Gyro Property. The x, y, z angular velocity values returned in a 3-tuple and
        are in :math:`degrees / second`
        :return: Angular velocity Values
        """
        raw_measurement = self._raw_gyro_data
        time.sleep(0.005)
        x = (
            raw_measurement[0]
            / gyro_full_scale_sensitivity[self._memory_gyro_fs]
            * 0.017453293
        )
        y = (
            raw_measurement[1]
            / gyro_full_scale_sensitivity[self._memory_gyro_fs]
            * 0.017453293
        )
        z = (
            raw_measurement[2]
            / gyro_full_scale_sensitivity[self._memory_gyro_fs]
            * 0.017453293
        )

        return x, y, z
