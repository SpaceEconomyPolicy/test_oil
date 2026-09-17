import pytest

streamlit = pytest.importorskip("streamlit")
from streamlit.testing.v1 import AppTest


def test_streamlit_app_starts_without_uncaught_exception():
    at = AppTest.from_file("app.py", default_timeout=30).run()
    assert not at.exception
