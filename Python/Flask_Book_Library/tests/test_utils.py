# test_utils.py
from project.utils import sanitize_text

def test_sanitize_text():
    # Test 1: usuwa <script>
    input_text = '<script>alert(1)</script>'
    expected = 'alert(1)'
    assert sanitize_text(input_text) == expected

    # Test 2: usuwa onerror w tagach <img>
    input_text = '<img src="x" onerror="alert(2)">'
    expected = ''
    assert sanitize_text(input_text) == expected

    # Test 3: pozostawia normalny tekst
    input_text = 'Normal Text'
    expected = 'Normal Text'
    assert sanitize_text(input_text) == expected

    # Test 4: usuwa mieszane tagi i atrybuty
    input_text = '<b>Bold</b> <a href="x" onclick="alert(3)">link</a>'
    expected = 'Bold link'
    assert sanitize_text(input_text) == expected

    # Test 5: obsługa pustego stringa
    input_text = ''
    expected = ''
    assert sanitize_text(input_text) == expected

    # Test 6: obsługa None
    input_text = None
    expected = ''
    assert sanitize_text(input_text) == expected
