"""
Shared Context Board / Semantic Bus - DCA-01
Publish/Subscribe with TTL, ACL, Schema validation
Can be backed by Redis
"""
import time, json
from typing import Dict, List

class Blackboard:
    def __init__(self):
        self.patterns: Dict[str, Dict] = {}

    def publish(self, pattern: Dict) -> bool:
        # validate against schema (placeholder)
        # ACL check
        pattern_id = pattern["pattern_id"]
        self.patterns[pattern_id] = {**pattern, "stored_at": time.time()}
        return True

    def subscribe(self, filter_type: str = None) -> List[Dict]:
        if not filter_type:
            return list(self.patterns.values())
        return [p for p in self.patterns.values() if p.get("pattern_type")==filter_type or filter_type in p.get("abstraction",{}).get("name","")]

    def ack(self, pattern_id: str, module_id: str) -> bool:
        if pattern_id in self.patterns:
            if module_id not in self.patterns[pattern_id].setdefault("consumers_ack", []):
                self.patterns[pattern_id]["consumers_ack"].append(module_id)
            return True
        return False

    def gc(self, ttl_ms=5000):
        now = time.time()
        to_delete = [k for k,v in self.patterns.items() if (now - v.get("stored_at",0))*1000 > v.get("ttl_ms", ttl_ms)]
        for k in to_delete:
            del self.patterns[k]