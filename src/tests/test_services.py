from unittest.mock import Mock, patch

from services import get_note


class TestGetNote:

    def test_returns_not_name(self):
        note = get_note(tonic="c1", scale="major", degree=0)
        assert "C" == note

    def test_returns_degree_plus_one_when_scale_is_not_found(self):
        note = get_note(tonic="C1", scale="myscale", degree=0)

        assert "1" == note

    @patch('services.TonedScale')
    def test_uses_toned_scale(self, mock_t_scale):
        mock_note = Mock()
        mock_note.name = "M1"

        mock_t_scale.return_value = {
            "fake_scale": [mock_note],
        }

        note = get_note(tonic="M1", scale="fake_scale", degree=0)

        mock_t_scale.assert_called_once_with(tonic="M1")
        assert "M1" == note
