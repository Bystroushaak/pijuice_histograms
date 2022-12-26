import time
from datetime import datetime

from matplotlib import pyplot
from matplotlib.dates import DateFormatter

from pijuice_histograms.orm import Storage


def _print_all_values(path: str):
    storage = Storage(path)
    for datapoint in storage.get_datapoints_between(*_get_timestamps_for_today()):
        print(datapoint)


def generate_graph_for_today(storage: Storage):
    timestamps = []
    status = []
    for datapoint in storage.get_datapoints_between(*_get_timestamps_for_today()):
        timestamps.append(datetime.fromtimestamp(datapoint.timestamp))
        status.append(datapoint.power_type.value)

    pyplot.title(f"SolarPi status for {time.strftime('%Y-%m-%d')}")
    pyplot.xlabel("Time")
    pyplot.ylabel("Solar status")
    pyplot.axhline(y=3, color="b", linestyle=":", label="Present")
    pyplot.axhline(y=2, color="orange", linestyle=":", label="Weak")
    pyplot.axhline(y=1, color="r", linestyle=":", label="Bad or not present")
    pyplot.legend(loc = 'best')
    pyplot.xlim(*_get_datetimes_for_today())

    date_fmt = DateFormatter("%H:%M:%S")
    pyplot.gca().xaxis.set_major_formatter(date_fmt)

    pyplot.bar(timestamps, status)
    pyplot.gcf().autofmt_xdate()
    pyplot.show()


def _get_timestamps_for_today():
    start, end = _get_datetimes_for_today()

    start_ts = datetime.timestamp(start)
    end_ts = datetime.timestamp(end)

    return (start_ts, end_ts)


def _get_datetimes_for_today():
    start = datetime.now()
    start = start.replace(hour=0, minute=0, second=0, microsecond=0)

    end = datetime.now()
    end = end.replace(hour=23, minute=59, second=59, microsecond=0)

    return start, end


if __name__ == "__main__":
    storage = Storage("/home/bystrousak/Desktop/c0d3z/python/tools/pijuice_histograms/data.sqlite")
    generate_graph_for_today(
        storage
    )
