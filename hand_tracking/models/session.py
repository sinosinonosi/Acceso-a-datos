import datetime

class Session:
    def __init__(self):
        self.start_time = datetime.datetime.now()
        self.end_time = None
        self.duration_seconds = 0

    def end_session(self):
        self.end_time = datetime.datetime.now()
        self.duration_seconds = (self.end_time - self.start_time).total_seconds()

    def to_dict(self):
        """Convierte el objeto a diccionario para guardarlo en MongoDB"""
        return {
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration_seconds": self.duration_seconds
        }