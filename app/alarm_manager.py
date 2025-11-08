import time
from typing import Dict

class AlarmManager:

    def __init__(self, cooldown_seconds: float):
        self.cooldown = cooldown_seconds
        self._states: Dict[int, dict] = {}

    def update_track(self, track_id: int, in_zone: bool):
        now = time.time()
        st = self._states.get(track_id)
        if st is None:
            st = {"in_zone": False, "last_seen_in_zone": 0.0, "alarm": False}
            self._states[track_id] = st

        if in_zone:
            st["in_zone"] = True
            st["last_seen_in_zone"] = now
            st["alarm"] = True
        else:
            if st["in_zone"]:
                st["last_seen_in_zone"] = now
            st["in_zone"] = False
            if st["alarm"] and (now - st["last_seen_in_zone"]) >= self.cooldown:
                st["alarm"] = False

    def is_alarm_on(self, track_id: int) -> bool:
        st = self._states.get(track_id)
        return bool(st and st.get("alarm", False))
