from midiutil.MidiFile import MIDIFile
from note.note import Note


class MidiWriter:
    def __init__(self, track_name, filepath, bpm=120):
        """
        Wraper around MIDIFile
        :param track_name: Track name
        :param bpm: Beat per minute, default=120
        """
        self.__midi_file = MIDIFile(1, adjust_origin=0)  # Single track
        self.__track = 0
        time = 0

        self.__track_name = track_name
        self.__midi_file.addTrackName(self.__track, time, self.__track_name)

        self.__midi_file.addTempo(self.__track, time, bpm)
        self.__channel = 0
        self.__filepath = filepath

    def write(self, note):
        """
        Add a note to the midi file
        :param note: note object to be added
        :return: None
        """
        duration = note.duration_tick
        if duration == 0:
            duration = 1
        for pitch in note.pitch_id:
            self.__midi_file.addNote(self.__track, self.__channel, pitch,
                                 note.start_time_tick, duration, note.volume)

    def close(self):
        """
        Write out the midi file
        :return: None
        """
        print(self.__filepath)
        with open(self.__filepath, 'wb') as out_file:
            self.__midi_file.writeFile(out_file)

if __name__ == '__main__':
    from midiutil.MidiFile import MIDIFile

    # create your MIDI object
    mf = MIDIFile(1)  # only 1 track
    track = 0  # the only track

    time = 0  # start at the beginning
    mf.addTrackName(track, time, "Sample Track")
    mf.addTempo(track, time, 120)

    # add some notes
    channel = 0
    volume = 100

    pitch = 60  # C4 (middle C)
    time = 0  # start on beat 0
    duration = 1  # 1 beat long
    mf.addNote(track, channel, pitch, time, duration, volume)

    pitch = 64  # E4
    time = 2  # start on beat 2
    duration = 1  # 1 beat long
    mf.addNote(track, channel, pitch, time, duration, volume)

    pitch = 67  # G4
    time = 4  # start on beat 4
    duration = 1  # 1 beat long
    mf.addNote(track, channel, pitch, time, duration, volume)

    # write it to disk
    with open("output.mid", 'wb') as outf:
        mf.writeFile(outf)