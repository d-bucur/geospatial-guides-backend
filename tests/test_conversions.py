from sql.converters import _format_col_name


def test_model_converter():
    assert _format_col_name('download_link') == 'downloadLink'
    assert _format_col_name('uploader_id') == 'uploaderId'
    assert _format_col_name('place_id') == 'placeId'
    assert _format_col_name('full_text') == 'fullText'
    assert _format_col_name('description') == 'description'
    assert _format_col_name('email') == 'email'
