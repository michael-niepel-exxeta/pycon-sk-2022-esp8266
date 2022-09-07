from enum import Enum
from datetime import datetime, timedelta
class TrackState(Enum):
    IDLE = 0
    RUNNING = 1


class Racetrack():
    TRACK_0_ID = 0
    TRACK_1_ID = 1

    MAX_DISTANCE = 50 # Max distance sensor distance we read
    DISTANCE_SPEED_RATIO = 2.5

    SPEED_CONSTANT = 100

    INITIAL_SPEED = SPEED_CONSTANT + 80

    LAPS_TO_WIN = 10

    OVERHEAT_IN_C = 30
    OVERHEAT_SPEED_CRIPPLE = 50

    def __init__(self):
        self.STATE = TrackState.IDLE
        self.start_time = None
        self.__init_laps()
        self.__init_overheat()

    def start_race(self, time):
        self.STATE = TrackState.RUNNING
        self.start_time = datetime.strptime(time, '%H:%M:%S.%f').time()

    def stop_race(self):
        self.STATE = TrackState.IDLE
        self.__init_laps()
        self.__init_overheat()

    def lap(self, track_id, time):
        self.laps[track_id] += 1
        print(f"Laps: {self.laps}")
        if self.laps[track_id] >= Racetrack.LAPS_TO_WIN:
            lap_at_time = datetime.strptime(time, '%H:%M:%S.%f').time()
            elapsed_time = timedelta(
                hours=(lap_at_time.hour - self.start_time.hour),
                minutes=(lap_at_time.minute - self.start_time.minute),
                seconds=(lap_at_time.second - self.start_time.second),
                microseconds=(lap_at_time.microsecond - self.start_time.microsecond))
            self.stop_race()
            return track_id, elapsed_time.total_seconds()
        return -1, -1

    def overheat(self, track_id, overheated=True):
        self.overheated[track_id] = overheated
        print(f"Overheat: {self.overheated}")

    def __init_laps(self):
        self.laps = {
            Racetrack.TRACK_0_ID: 0,
            Racetrack.TRACK_1_ID: 0
        }

    def __init_overheat(self):
        self.overheated = {
            Racetrack.TRACK_0_ID: False,
            Racetrack.TRACK_1_ID: False
        }

    # speed from distance
    def speed_from_distance(self, distance, track_id):
        # distance is 0-50 cm, we want speed 0-90 inverted
        distance_inverted = Racetrack.MAX_DISTANCE - distance

        speed = Racetrack.SPEED_CONSTANT + (distance_inverted * Racetrack.DISTANCE_SPEED_RATIO)
        print(f"Speed -> {speed}")
        # if car overheated 
        if (speed >= Racetrack.OVERHEAT_SPEED_CRIPPLE) and self.overheated[track_id]:
            speed = speed - Racetrack.OVERHEAT_SPEED_CRIPPLE
        print(f"Speed after overheated check -> {speed}")

        return int(speed)

