import asyncio
import pandas as pd

async def stream_events(delay=0.5):
    while True:
        df = pd.read_csv("dataset/traffic.csv")
        for _, row in df.iterrows():
            yield {
                "timestamp": row["timestamp"],
                "src_ip": row["src_ip"],
                "dst_ip": row["dst_ip"],
                "bytes": int(row["bytes"]),
                "label": row["label"]
            }
            await asyncio.sleep(delay)
