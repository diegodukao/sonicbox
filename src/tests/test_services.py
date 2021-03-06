from unittest.mock import Mock, patch

from services.theory import get_note_name, is_octave


class TestGetNoteName:

    def test_returns_not_name(self):
        note = get_note_name(tonic="c1", scale="major", degree=0)
        assert "C" == note

    def test_returns_degree_plus_one_when_scale_is_not_found(self):
        note = get_note_name(tonic="C1", scale="myscale", degree=0)

        assert "1" == note

    @patch('services.theory.TonedScale')
    def test_uses_toned_scale(self, mock_t_scale):
        mock_note = Mock()
        mock_note.name = "M1"

        mock_t_scale.return_value = {
            "fake_scale": [mock_note],
        }

        note = get_note_name(tonic="M1", scale="fake_scale", degree=0)

        mock_t_scale.assert_called_once_with(tonic="M1")
        assert "M1" == note

    @patch('services.theory.TonedScale')
    def test_result_is_cached(self, mock_t_scale):
        get_note_name(tonic="N1", scale="fake_scale", degree=0)
        mock_t_scale.assert_called_once_with(tonic="N1")

        get_note_name(tonic="N1", scale="fake_scale", degree=0)
        # still called just once
        mock_t_scale.assert_called_once_with(tonic="N1")


class TestIsOctave:

    def test_is_octave(self):
        assert is_octave(14, "minor")
        assert not is_octave(9, "major")
        assert is_octave(18, "blues_minor")
        assert not is_octave(21, "minor_pentatonic")
