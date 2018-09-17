from functools import lru_cache

from pytheory import TonedScale

from constants.synth import SCALES


@lru_cache()
def get_note(tonic, scale, degree):
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
