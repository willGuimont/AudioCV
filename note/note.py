

class Note:
    def __init__(self, pitch_id, bpm=120, volume=127):
        """
        Stuct class for a midi note (pithc_id, is_playing, duration, volume)
        :param pitch_id: Midi note (C4 = 60, see note.notes_defines.py)
        :param volume: initial volume of the note
        """
        self.__bpm = bpm

        if not isinstance(pitch_id, list):
            pitch_id = [pitch_id]

        self.__pitch_id = pitch_id
        self.__is_playing = False
        self.__volume = volume
        self.__duration = 0
        self.__start_time = 0

    def reset_duration(self):
        """
        Set duration to 0
        :return: None
        """
        self.__duration = 0

    def add_duration(self, dt):
        """

        :param dt:
        :return:
        """
        self.__duration += dt

    def __seconds_to_tick(self, value):
        """
        Transform seconds to ticks
        :param value: Time value (seconds)
        :param bmp: Beat per minutes (usually 120 bpm)
        :return: Tick
        """
        # seconds * (beat / minutes) / (60 seconds / minutes)
        return value * self.__bpm / 60

    def get_tick_duration(self):
        return self.__seconds_to_tick(self.duration)

    def get_tick_time(self):
        return self.__seconds_to_tick(self.start_time)

    @property
    def bpm(self):
        return self.__bpm

    @bpm.setter
    def bpm(self, value):
        self.__bpm = value

    @property
    def start_time_tick(self):
        return self.__seconds_to_tick(self.__start_time)

    @property
    def start_time(self):
        return self.__start_time

    @start_time.setter
    def start_time(self, value):
        self.__start_time = value

    @property
    def pitch_id(self):
        return self.__pitch_id

    @pitch_id.setter
    def pitch(self, value):
        self.__pitch_id = value

    @property
    def is_playing(self):
        return self.__is_playing

    @is_playing.setter
    def is_playing(self, value):
        self.__is_playing = value

    @property
    def volume(self):
        return self.__volume

    @volume.setter
    def volume(self, value):
        if value < 0:
            value = 0
        elif value > 127:
            value = 127
        self.__volume = value

    @property
    def duration_tick(self):
        return self.__duration

    @property
    def duration(self):
        return self.__duration

    @duration.setter
    def duration(self, value):
        self.__duration = value
