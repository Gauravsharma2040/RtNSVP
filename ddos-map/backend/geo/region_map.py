# geo/region_map.py
import json
import hashlib
from .base import GeoResolver

class RegionGeoResolver(GeoResolver):
    def __init__(self, region_file: str):
        with open(region_file) as f:
            self.regions = json.load(f)
        self.keys = list(self.regions.keys())
    
    
    def resolve(self, event):
        return self.resolve_with_key(event["label"])

    def resolve_with_key(self, key):
        idx = hash(key) % len(self.keys)
        region = self.keys[idx]
        return self.regions[region]

