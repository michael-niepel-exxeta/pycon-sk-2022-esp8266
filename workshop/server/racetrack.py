from enum import Enum

class TrackState(Enum):
    IDLE = 0
    RUNNING = 1


class Racetrack():
    TRACK_0_ID = 0
    TRACK_1_ID = 1

    MAX_DISTANCE = 50 # Max distance sensor distance we read
    DISTANCE_SPEED_RATIO = 2

    SPEED_CONSTANT = 100

    INITIAL_SPEED = 80

    LAPS_TO_WIN = 20

    def __init__(self):
        self.STATE = TrackState.IDLE
        self.start_time = None
        self.__init_laps()

    def start_race(self, time):
        self.STATE = TrackState.RUNNING
        self.start_time = time

    def stop_race(self):
        self.STATE = TrackState.IDLE
        self.__init_laps()

    def lap(self, track_id):
        self.laps[track_id] += 1
        print(f"Laps: {self.laps}")
        if self.laps[track_id] >= Racetrack.LAPS_TO_WIN:
            self.stop_race()
            return track_id
        return -1

    def __init_laps(self):
        self.laps = {
            Racetrack.TRACK_0_ID: 0,
            Racetrack.TRACK_1_ID: 0
        }


    # speed from distance
    @staticmethod
    def speed_from_distance(distance):
        # distance is 0-50 cm, we want speed 0-90 inverted
        distance_inverted = Racetrack.MAX_DISTANCE - distance

        speed = Racetrack.SPEED_CONSTANT + (distance_inverted * Racetrack.DISTANCE_SPEED_RATIO)

        return int(speed)

