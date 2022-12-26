import time

from pijuice import PiJuice

from pijuice_histograms.orm import Storage
from pijuice_histograms.orm import Datapoint
from pijuice_histograms.orm import BatteryInfo
from pijuice_histograms.orm import PowerTypeEnum


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
