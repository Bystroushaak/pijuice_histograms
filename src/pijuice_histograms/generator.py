import os
import shutil
from datetime import datetime
from datetime import timedelta
from typing import Tuple

import tqdm
from matplotlib import pyplot
from matplotlib.dates import DateFormatter

from pijuice_histograms.orm import Storage


def generate_webpage_for_last_month(sqlite_path: str, report_path: str):
    storage = Storage(sqlite_path)
    report_path = os.path.join(report_path, "solarpi_report/")

    today = datetime.today()
    ranges = [today]
    for x in range(30):
        ranges.append(today - timedelta(days=x + 1))

    os.makedirs(report_path, exist_ok=True)

    report = open(os.path.join(report_path, "index_.html"), "wt")
    report.write(
        f"""<!DOCTYPE html>
<html>
<head>
  <title>SolarPi report</title>
</head>
<body>
<h1>SolarPi report</h1>
<p>Generated <code>{datetime.now().isoformat()}</code></p>
<p>From the manual:</p>
<ul>
    <li><b>NOT_PRESENT</b> - Power supply is not connected to the PiJuice micro USB connector</li>
    <li><b>BAD</b> - Power supply is connected but is not providing enough power</li>
    <li><b>WEAK</b> - Power supply is connected but is weak i.e. power supply cannot charge the PiJuice and provide power to the Raspberry Pi. DPM is active, see - <a href="https://github.com/PiSupply/PiJuice/tree/master/Hardware#usb-micro-input">https://github.com/PiSupply/PiJuice/tree/master/Hardware#usb-micro-input</a></li>
    <li><b>PRESENT</b> - Power supply is connected and is providing good power to the PiJuice</li>
</ul>
<p>Which basically means that everything under <b>WEAK</b> is <i>"not using the solar cell input at all</i>, and <b>WEAK</b> is <i>using it maybe, sometimes when DPM works</i>. Ideally, it should be <b>PRESENT</b>.</p>
"""
    )

    for cnt, date in tqdm.tqdm(list(enumerate(ranges))):
        report.write(f"<h2>{date.strftime('%Y-%m-%d')}</h2>\n")
        report.write(f"<img src='{cnt}.png' />\n")

        generate_graph_for(storage, date, os.path.join(report_path, f"{cnt}.png"))

    report.write(
        """</body>
</html>"""
    )
    report.close()

    shutil.move(
        os.path.join(report_path, "index_.html"),
        os.path.join(report_path, "index.html"),
    )


def generate_graph_for(storage: Storage, day: datetime = None, path: str = None):
    if day is None:
        day = datetime.now()

    timestamps = []
    status = []
    for timestamp, power_status in storage.get_power_status_between(
        *_get_timestamps_for(day)
    ):
        timestamps.append(datetime.fromtimestamp(timestamp))
        status.append(power_status)

    pyplot.title(f"SolarPi status for {day.strftime('%Y-%m-%d')}")
    pyplot.xlabel("Time")
    pyplot.ylabel("Solar status")
    pyplot.axhline(y=3, color="green", linestyle=":", label="Present")
    pyplot.axhline(y=2, color="orange", linestyle=":", label="Weak")
    pyplot.axhline(y=1, color="r", linestyle=":", label="Bad")
    pyplot.axhline(y=0, color="purple", linestyle=":", label="Not present")
    pyplot.legend(loc="best")
    pyplot.xlim(*_get_dayrange_for(day))

    date_fmt = DateFormatter("%H:%M:%S")
    pyplot.gca().xaxis.set_major_formatter(date_fmt)

    pyplot.plot(timestamps, status)
    pyplot.gcf().autofmt_xdate()

    if path is None:
        pyplot.show()
    else:
        pyplot.gcf().set_size_inches(10, 4)
        pyplot.savefig(path, dpi=150)
        pyplot.close()


def _get_timestamps_for(day: datetime) -> Tuple[float, float]:
    start, end = _get_dayrange_for(day)

    start_ts = datetime.timestamp(start)
    end_ts = datetime.timestamp(end)

    return (start_ts, end_ts)


def _get_dayrange_for(day: datetime) -> Tuple[datetime, datetime]:
    start = day.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)

    return start, end
