# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
from machine import Pin, I2C
from micropython_icg20660 import icg20660

i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
icg = icg20660.ICG20660(i2c)

icg.gyro_dlpf_mode = icg20660.GYRO_DLPF_ENABLED

while True:
    for gyro_dlpf_mode in icg20660.gyro_dlpf_mode_values:
        print("Current Gyro dlpf mode setting: ", icg.gyro_dlpf_mode)
        for _ in range(10):
            gyrox, gyroy, gyroz = icg.gyro
            print("x:{:.2f}°/s, y:{:.2f}°/s, z{:.2f}°/s".format(gyrox, gyroy, gyroz))
            print()
            time.sleep(0.5)
        icg.gyro_dlpf_mode = gyro_dlpf_mode
