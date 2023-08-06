from __future__ import annotations

from datetime import datetime, timedelta
import requests


def get_noaa_opendap_urls(last_n: int = None):
    now = datetime.utcnow() - timedelta(days=1)
    hour = 18
    now = now.replace(hour=hour, minute=0, second=0, microsecond=0)
    dataset_times = [now - timedelta(hours=6 * i) for i in range(0, 10)]
    datasets = [
        f"gfs{dataset_datetime.strftime('%Y%m%d')}/gfs_0p25_1hr_{dataset_datetime.hour:02d}z"
        for dataset_datetime in dataset_times
    ]
    urls = []
    for dataset in datasets:
        info_url = f"https://nomads.ncep.noaa.gov/dods/gfs_0p25_1hr/{dataset}.info"
        response = requests.get(info_url)

        if "error" in response.text:
            next
        else:
            urls.append(f"http://nomads.ncep.noaa.gov:80/dods/gfs_0p25_1hr/{dataset}")
    if last_n:
        return urls[:last_n]
    else:
        return urls
