import datetime

class VolumeEvent:
    def __init__(self, old_volume, new_volume, distance):
        self.timestamp = datetime.datetime.now()
        self.old_volume = old_volume
        self.new_volume = new_volume
        self.distance = distance

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "old_volume": self.old_volume,
            "new_volume": self.new_volume,
            "finger_distance": self.distance
        }