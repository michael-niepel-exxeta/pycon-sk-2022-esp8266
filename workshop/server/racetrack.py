from enum import Enum

class TrackState(Enum):
    IDLE = 0
    RUNNING = 1


class Racetrack():
    TRACK_0_ID = 0
    TRACK_1_ID = 1

    MAX_DISTANCE = 50 # Max distance sensor distance we read
    DISTANCE_SPEED_RATIO = 2

    INITIAL_SPEED = 80

    def __init__(self):
        self.STATE = TrackState.IDLE
        self.start_time = None
        self.laps = {
            Racetrack.TRACK_0_ID: 0,
            Racetrack.TRACK_1_ID: 0
        }

    # button state
    def button_pressed(self, time):
        if self.STATE == TrackState.IDLE:
            self._start_race(time)
        elif self.STATE == TrackState.RUNNING:
            self._stop_race(time)

    def _start_race(self, time):
        self.STATE = TrackState.RUNNING
        self.start_time = time

    def _stop_race(self, time):
        self.STATE = TrackState.IDLE
        self.stop_time = time

    # speed from distance
    @staticmethod
    def speed_from_distance(distance):
        # distance is 0-50 cm, we want speed 0-90 inverted
        distance_inverted = Racetrack.MAX_DISTANCE - distance

        speed = distance_inverted * Racetrack.DISTANCE_SPEED_RATIO

        return int(speed)

