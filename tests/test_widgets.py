from unittest.mock import patch


# not working
@patch('widgets.synth_widgets.SynthButton', autospec=True)
def test_create_bottom_sheet(mock_SButton):
    sb = mock_SButton()
    pass
