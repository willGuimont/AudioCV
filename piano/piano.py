from note.note import Note
from utils.midi_writer import MidiWriter
from midi_player.midi_player import MidiPlayer


class Piano:
    def __init__(self, regions, notes, use_audio=True, track_name="main", filepath="", bpm=120):
        """
        Handle a bunch of regions triggering notes
        :param regions: Region of n-dimensions [list]
        :param notes: Notes to be played when the corresponding region is triggered [list]
        """
        n = len(regions)
        if len(notes) != n:
            raise ValueError("regions and notes must be of the same size")
        # Region, Note
        for note in notes:
            note.bpm = bpm
        self.__regions_notes = [[regions[i], notes[i]]  for i in range(n)]
        self.__time = 0

        self.__midi_player = None
        if use_audio:
            self.__midi_player = MidiPlayer()

        self.__midi_writer = None
        if filepath != "":
            self.__midi_writer = MidiWriter(track_name, filepath, bpm)

    def draw(self, image):
        for region, _ in self.__regions_notes:
            region.draw(image, (255, 0, 0))

    def update(self, points, dt):
        """
        Update the piano
        :param point: List of points that can trigger the regions
        :param dt: Time since the last call
        :return: None
        """
        self.__time += dt
        for region, note in self.__regions_notes:
            playing = False
            for point in points:
                playing = playing or region.is_in_region(point)
            if playing:
                if note.is_playing:
                    self.__on_note_holded(note, dt)
                else:
                    self.__on_note_pressed(note, region, point)
            else:
                if note.is_playing:
                    self.__on_note_released(note)


    def set_note_params(self, note, region, point):
        """
        Vary the volume (or any other param) of the note according to the relative
            positiobn inside of the region
        More usefull if the Kinect is implemented
        Will probably be overriden in subclasses
        :param note: Note to change the param
        :param region: Region responsible for the note
        :param point: Point that triggered the region
        :return: None
        """
        pass

    def __on_note_pressed(self, note, regions, point):
        """
        Called when the note if pressed, duh
        :param note: Note
        :param regions: Region
        :param point: Point
        :return: None
        """
        self.set_note_params(note, regions, point)
        note.is_playing = True
        note.start_time = self.__time

        if self.__midi_player is not None:
            self.__midi_player.play(note.pitch_id)

    def __on_note_released(self, note):
        """
        Called when the note if released, duh
        :param note: Note
        """
        note.is_playing = False

        if self.__midi_player is not None:
            self.__midi_player.stop(note.pitch_id)

        if self.__midi_writer is not None:
            self.__midi_writer.write(note)

        note.reset_duration()

    def __on_note_holded(self, note, dt):
        """
        Called when a note is being pressed for more than one frame
        :param note: Note
        :param dt: Time elapsed
        :return:
        """
        note.add_duration(dt)

    def close(self):
        """
        Will write midi to file
        :return: None
        """
        if self.__midi_player is not None:
            self.__midi_player.close()
        if self.__midi_writer is not None:
            self.__midi_writer.close()