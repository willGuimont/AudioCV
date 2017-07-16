import pygame.midi as midi
from time import sleep


class MidiPlayer():
    inited = False

    def __init__(self, output=0, instrument=0):
        if not MidiPlayer.inited:
            self.init()
        self.__player = midi.Output(output)
        self.__player.set_instrument(instrument)

    def init(self):
        midi.init()

    def play(self, note_id, velocity=127):
        self.__player.note_on(note_id, velocity)

    def stop(self, note_id, velocity=127):
        self.__player.note_off(note_id, velocity)

    def close(self):
        self.__player.close()
