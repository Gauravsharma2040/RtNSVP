import asyncio
import pandas as pd
import random
from geo.region_map import RegionGeoResolver

FILES = [
    "dataset/DNS-testing.parquet",
    "dataset/NTP-testing.parquet",
    "dataset/Syn-testing.parquet"
]

geo_resolver = RegionGeoResolver("geo/data/regions.json")


def jitter(lat, lon, radius=1.5):
    return (
        lat + random.uniform(-radius, radius),
        lon + random.uniform(-radius, radius)
    )


async def stream_events(delay=0.5):
    dataframes = [pd.read_parquet(f) for f in FILES]

    while True:
        for df in dataframes:
            for row in df.itertuples(index=False):
                event = {
                    "label": row.Label,
                    "protocol": row.Protocol,
                    "flow_duration": getattr(row, "Flow_Duration", None)
                }

                # Resolve region
                key = f"{event['label']}_{random.randint(0, 10)}"
                base_lat, base_lon = geo_resolver.resolve_with_key(key) 
                # Apply jitter
                lat, lon = jitter(base_lat, base_lon)

                event["lat"] = lat
                event["lon"] = lon

                yield event
                await asyncio.sleep(0.5)
