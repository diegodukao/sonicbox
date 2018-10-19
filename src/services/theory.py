from functools import lru_cache

from pytheory import TonedScale

from constants.synth import SCALES


@lru_cache()
def get_note_name(tonic, scale, degree):
    tonic = tonic.upper()

    if not (tonic and scale):
        return str(degree + 1)

    tone = TonedScale(tonic=tonic)

    try:
        scale_ = tone[scale]
    except KeyError:
        return str(degree + 1)

    return scale_[degree].name


def is_octave(note, scale):
    return bool(note % SCALES[scale] == 0)


def get_chord_name(tonic, key_type, degree):
    tonic = tonic.upper()[:-1]

    try:
        return CHORDS[key_type][tonic][degree]
    except KeyError:
        return degree


CHORDS = {
    "major": {
        "C": {
            "I": "C",
            "II": "Dm",
            "III": "Em",
            "IV": "F",
            "V": "G",
            "VI": "Am",
            "VII": "Bdim",
        },
        "D": {
            "I": "D",
            "II": "Em",
            "III": "F#m",
            "IV": "G",
            "V": "A",
            "VI": "Bm",
            "VII": "C#dim",
        },
        "E": {
            "I": "E",
            "II": "F#m",
            "III": "G#m",
            "IV": "A",
            "V": "B",
            "VI": "C#m",
            "VII": "D#dim",
        },
    },
    "minor": {
        "C": {
            "I": "Cm",
            "II": "Ddim",
            "III": "Eb",
            "IV": "Fm",
            "V": "Gm",
            "VI": "Ab",
            "VII": "Bb",
        },
        "E": {
            "I": "Em",
            "II": "F#dim",
            "III": "G",
            "IV": "Am",
            "V": "Bm",
            "VI": "C",
            "VII": "D",
        },
        "G": {
            "I": "Gm",
            "II": "Adim",
            "III": "Bb",
            "IV": "Cm",
            "V": "Dm",
            "VI": "Eb",
            "VII": "F",
        },
    },
}
