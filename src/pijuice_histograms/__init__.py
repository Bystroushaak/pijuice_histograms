import time
from enum import Enum
from typing import Optional

from pijuice import PiJuice


class PowerTypeEnum(Enum):
    NOT_PRESENT = 0
    BAD = 1
    WEAK = 2
    PRESENT = 3


class BatteryInfo:
    def __init__(self, voltage, current, temperature):
        self.voltage = voltage
        self.current = current
        self.temperature = temperature


class Datapoint:
    timestamp: float
    power_type: Optional[PowerTypeEnum]
    battery: Optional[BatteryInfo]

    def __init__(self):
        self.timestamp = time.time()
        self.power_type = None
        self.battery = None

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"""Datapoint(
    timestamp={self.timestamp},
    power_type={self.power_type},
    battery=BatteryInfo(
        voltage={self.battery.voltage},
        current={self.battery.current},
        temperature={self.battery.temperature},
    ),
)"""


class Storage:
    def __init__(self, path: str):
        self.path = path

    def add_datapoint(self, datapoint: Datapoint):
        print(datapoint)

    def save(self):
        pass

    def create_storage(self):
        pass


class DatapointCollector:
    SAVE_EVERY = 10 * 60 / 5  # 10 minutes

    def __init__(self, db_path):
        self.db_path = db_path
        self.storage = Storage(self.db_path)

        self.pijuice = PiJuice(1, 0x14)

    def run(self):
        cnt = self.SAVE_EVERY
        while True:
            datapoint = self._get_datapoint()
            self.storage.add_datapoint(datapoint)

            cnt -= 1
            if cnt <= 0:
                cnt = self.SAVE_EVERY
                self.save()

            time.sleep(5)

    def _get_datapoint(self) -> Datapoint:
        datapoint = Datapoint()

        status = self.pijuice.status
        datapoint.power_type = getattr(
            PowerTypeEnum,
            status.GetStatus()["data"]["powerInput"],
        )

        datapoint.battery = BatteryInfo(
            voltage=status.GetBatteryVoltage()["data"] / 1000,
            current=status.GetBatteryCurrent()["data"] / 1000,
            temperature=status.GetBatteryTemperature()["data"],
        )

        return datapoint

    def save(self):
        self.storage.save()
