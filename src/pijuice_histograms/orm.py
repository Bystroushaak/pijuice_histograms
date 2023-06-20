import time
import sqlite3
from enum import Enum
from typing import Tuple, Iterator, Optional


class PowerTypeEnum(Enum):
    NOT_PRESENT = 0
    BAD = 1
    WEAK = 2
    PRESENT = 3


class BatteryInfo:
    def __init__(self, voltage, current, temperature, charge):
        self.voltage = voltage
        self.current = current
        self.temperature = temperature
        self.charge = charge


class Datapoint:
    timestamp: float
    power_type: Optional[PowerTypeEnum]
    battery: Optional[BatteryInfo]

    def __init__(self, timestamp=None, power_type=None, battery=None):
        self.timestamp = timestamp or time.time()
        self.power_type = power_type
        self.battery = battery

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
        charge={self.battery.charge},
    ),
)"""


class Storage:
    def __init__(self, path: str):
        self.path = path

        self.database = sqlite3.connect(self.path)
        self.database.row_factory = sqlite3.Row

        self.create_storage()

    def create_storage(self):
        cursor = self.database.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS SolarPi(
                timestamp INT PRIMARY KEY,
                power_type INT,
                voltage INT,
                current INT,
                temperature INT,
                charge INT
            );
            """
        )

        self.save()

    def add_datapoint(self, datapoint: Datapoint):
        print(datapoint)

        cursor = self.database.cursor()
        cursor.execute(
            """
            INSERT INTO SolarPi(timestamp, power_type, voltage, current, temperature, charge)
            VALUES (?, ?, ?, ?, ?, ?);
            """,
            (
                datapoint.timestamp,
                datapoint.power_type.value,
                datapoint.battery.voltage,
                datapoint.battery.current,
                datapoint.battery.temperature,
                datapoint.battery.charge,
            )
        )

    def get_status_between(self, from_ts, to_ts) -> Iterator[Tuple[int, int, int]]:
        cursor = self.database.cursor()

        cursor.execute(
            "SELECT timestamp, power_type, charge FROM SolarPi WHERE timestamp BETWEEN ? AND ?;",
            (from_ts, to_ts),
        )
        for data in cursor.fetchall():
            yield (data["timestamp"], data["power_type"], data["charge"])

    def get_datapoints_between(self, from_ts, to_ts) -> Iterator[Datapoint]:
        cursor = self.database.cursor()

        cursor.execute(
            "SELECT * FROM SolarPi WHERE timestamp BETWEEN ? AND ?;",
            (from_ts, to_ts),
        )
        for data in cursor.fetchall():
            yield Datapoint(
                data["timestamp"],
                PowerTypeEnum(data["power_type"]),
                BatteryInfo(
                    voltage=data["voltage"],
                    current=data["current"],
                    temperature=data["temperature"],
                    charge=data["charge"]
                )
            )

    def save(self):
        self.database.commit()

    def close(self):
        self.database.close()
