"""module test_log_file"""

import os
import pytest
from reboot_button.log_file import is_log_file_writable


@pytest.fixture
def create_temp_file(tmp_path):
    """
    Fixture to create a temporary file for testing.
    """
    temp_file = tmp_path / "temp_log_file.log"
    temp_file.write_text("Initial content")
    return temp_file


def test_is_log_file_writable_existing_file(create_temp_file): # pylint: disable=redefined-outer-name
    """
    Test that is_log_file_writable returns True for an existing writable file.
    """
    assert is_log_file_writable(create_temp_file), "Existing log file is not writable."


def test_is_log_file_writable_nonexistent_file(tmp_path):
    """
    Test that is_log_file_writable returns False for a nonexistent file.
    """
    nonexistent_file = tmp_path / "nonexistent_log_file.log"
    assert not is_log_file_writable(nonexistent_file), "Nonexistent log file is writable."


def test_is_log_file_writable_non_writable_file(tmp_path):
    """
    Test that is_log_file_writable returns False for a non-writable file.
    """
    non_writable_file = tmp_path / "non_writable_log_file.log"
    non_writable_file.write_text("Initial content")
    os.chmod(non_writable_file, 0o444)  # Set file to read-only
    assert not is_log_file_writable(non_writable_file), "Non-writable log file is writable."
