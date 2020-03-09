def assert_is_place(p):
    assert_is_place_without_distance(p)
    assert 'distance' in p


def assert_is_place_without_distance(p):
    assert 'name' in p
    assert 'numGuides' in p


def assert_is_guide(g):
    assert 'duration' in g
    assert 'description' in g
    assert 'price' in g
    assert 'rating' in g
    assert 'downloadLink' not in g
    assert 'fullText' not in g


def assert_is_downloaded_guide(g):
    assert 'duration' not in g
    assert 'price' not in g
    assert 'downloadLink' in g
    assert 'fullText' in g


def assert_is_user(g):
    assert 'id' in g
    assert 'email' in g
    assert 'name' in g
