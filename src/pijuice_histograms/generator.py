import os
from datetime import datetime
from datetime import timedelta

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
        ranges.append(today - timedelta(days = x + 1))

    os.makedirs(report_path, exist_ok=True)

    report = open(os.path.join(report_path, "report.html"), "wt")
    report.write(f"""<!DOCTYPE html>
<html>
<head>
  <title>SolarPi report</title>
</head>
<body>
<h1>SolarPi report</h1>
<p>Generated <code>{datetime.now().isoformat()}</code></p>
""")

    for cnt, date in tqdm.tqdm(list(enumerate(ranges))):
        report.write(f"<h2>{date.strftime('%Y-%m-%d')}</h2>\n")
        report.write(f"<img src='{cnt}.png' />\n")

        generate_graph_for(storage, date, os.path.join(report_path, f"{cnt}.png"))

    report.write("""</body>
</html>""")
    report.close()

def generate_graph_for(storage: Storage, day=None, path=None):
    if day is None:
        day = datetime.now()

    timestamps = []
    status = []
    for datapoint in storage.get_datapoints_between(*_get_timestamps_for(day)):
        timestamps.append(datetime.fromtimestamp(datapoint.timestamp))
        status.append(datapoint.power_type.value)

    pyplot.title(f"SolarPi status for {day.strftime('%Y-%m-%d')}")
    pyplot.xlabel("Time")
    pyplot.ylabel("Solar status")
    pyplot.axhline(y=3, color="b", linestyle=":", label="Present")
    pyplot.axhline(y=2, color="orange", linestyle=":", label="Weak")
    pyplot.axhline(y=1, color="r", linestyle=":", label="Bad or not present")
    pyplot.legend(loc = 'best')
    pyplot.xlim(*_get_datetimes_for(day, day))

    date_fmt = DateFormatter("%H:%M:%S")
    pyplot.gca().xaxis.set_major_formatter(date_fmt)

    pyplot.bar(timestamps, status)
    pyplot.gcf().autofmt_xdate()

    if path is None:
        pyplot.show()
    else:
        pyplot.gcf().set_size_inches(10, 4)
        pyplot.savefig(path, dpi=150)
        pyplot.close()


def _get_timestamps_for(day):
    start, end = _get_datetimes_for(day, day)

    start_ts = datetime.timestamp(start)
    end_ts = datetime.timestamp(end)

    return (start_ts, end_ts)


def _get_datetimes_for(start, end):
    start = start.replace(hour=0, minute=0, second=0, microsecond=0)
    end = end.replace(hour=23, minute=59, second=59, microsecond=0)

    return start, end
