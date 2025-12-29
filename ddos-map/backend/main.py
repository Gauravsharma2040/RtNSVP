from fastapi import FastAPI, WebSocket
from streamer import stream_events
from metrics import StreamMetrics

app = FastAPI()

# Create metrics ONCE (global state)
metrics = StreamMetrics()

@app.websocket("/ws/traffic")
async def traffic_ws(ws: WebSocket):
    await ws.accept()

    async for event in stream_events():
        metrics.update(event)

        await ws.send_json({
            "event": event,
            "metrics": metrics.snapshot()
        })
