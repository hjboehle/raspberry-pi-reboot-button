"""module test_log_file"""

import logging
import pytest
from reboot_button.log_file import (
    configure_stdout_logger,
    append_or_create_log_file,
    setup_log_file,
)


@pytest.fixture(name="temp_file_writeable")
def create_temp_file_writeable(tmp_path):
    """
    Fixture to create a temporary file for testing.
    """
    writeable_tmp_file_path = tmp_path / "path" / "temp_writeable_log_file.log"
    writeable_tmp_file_path.parent.mkdir(parents=True, exist_ok=True)
    writeable_tmp_file_path.write_text("Initial content")
    return writeable_tmp_file_path


def test_append_or_create_log_file_creates_file(temp_file_writeable):
    """
    Test that append_or_create_log_file creates a log file.
    """
    log_dir = temp_file_writeable.parent
    log_file_name = temp_file_writeable.name
    result = append_or_create_log_file(str(log_dir), log_file_name)
    assert result is True
    assert temp_file_writeable.exists()


def test_append_or_create_log_file_handles_existing_file(temp_file_writeable):
    """
    Test that append_or_create_log_file appends to an existing log file.
    """
    log_dir = temp_file_writeable.parent
    log_file_name = temp_file_writeable.name
    temp_file_writeable.write_text("Initial content")
    result = append_or_create_log_file(str(log_dir), log_file_name)
    assert result is True
    assert temp_file_writeable.exists()
    assert temp_file_writeable.read_text() == "Initial content"


def test_append_or_create_log_file_handles_invalid_directory(mocker):
    """
    Test that append_or_create_log_file handles an invalid directory.
    """
    mocker.patch("os.makedirs", side_effect=OSError("Permission denied"))
    log_dir = "/invalid/directory"
    log_file_name = "log_file.log"
    result = append_or_create_log_file(log_dir, log_file_name)
    assert result is False


def test_setup_log_file_creates_system_wide_log_file(temp_file_writeable, mocker):
    """
    Test that setup_log_file creates a system-wide log file.
    """
    mock_append_or_create_log_file = mocker.patch(
        "reboot_button.log_file.append_or_create_log_file",
        return_value=True
    )
    mock_setup_file_logger = mocker.patch("reboot_button.log_file.setup_file_logger")
    log_dir_root = temp_file_writeable.parent
    log_dir_home = temp_file_writeable.parent / "home"
    log_file_name = temp_file_writeable.name
    result = setup_log_file(str(log_dir_root), str(log_dir_home), log_file_name)
    assert result["success"] is True
    assert result["log_file_path"] == str(log_dir_root / log_file_name)
    assert mock_append_or_create_log_file.call_args_list[0] == ((str(log_dir_root), log_file_name),)
    assert mock_setup_file_logger.call_args_list[0] == ((str(log_dir_root / log_file_name),),)


def test_setup_log_file_creates_user_specific_log_file(temp_file_writeable, mocker):
    """
    Test that setup_log_file creates a user-specific log file if system-wide fails.
    """
    mock_append_or_create_log_file = mocker.patch(
        "reboot_button.log_file.append_or_create_log_file",
        side_effect=[False, True]
    )
    mock_setup_file_logger = mocker.patch("reboot_button.log_file.setup_file_logger")
    log_dir_root = temp_file_writeable.parent / "invalid"
    log_dir_home = temp_file_writeable.parent
    log_file_name = temp_file_writeable.name
    result = setup_log_file(str(log_dir_root), str(log_dir_home), log_file_name)
    assert result["success"] is True
    assert result["log_file_path"] == str(log_dir_home / log_file_name)
    assert mock_append_or_create_log_file.call_args_list[0] == ((str(log_dir_root), log_file_name),)
    assert mock_append_or_create_log_file.call_args_list[1] == ((str(log_dir_home), log_file_name),)
    assert mock_setup_file_logger.call_args_list[0] == ((str(log_dir_home / log_file_name),),)


def test_setup_log_file_fails(temp_file_writeable, mocker):
    """
    Test that setup_log_file fails if both system-wide and user-specific log file creation fails.
    """
    mock_append_or_create_log_file = mocker.patch(
        "reboot_button.log_file.append_or_create_log_file",
        return_value=False
    )
    log_dir_root = temp_file_writeable.parent / "invalid"
    log_dir_home = temp_file_writeable.parent / "invalid_home"
    log_file_name = temp_file_writeable.name
    result = setup_log_file(str(log_dir_root), str(log_dir_home), log_file_name)
    assert result["success"] is False
    assert result["log_file_path"] == ""
    assert mock_append_or_create_log_file.call_args_list[0] == ((str(log_dir_root), log_file_name),)
    assert mock_append_or_create_log_file.call_args_list[1] == ((str(log_dir_home), log_file_name),)


def test_configure_stdout_logger_creates_logger(mocker):
    """
    Test that configure_stdout_logger creates a logger with a StreamHandler.
    """
    mock_get_logger = mocker.patch("logging.getLogger")
    mock_logger = mocker.Mock()
    mock_get_logger.return_value = mock_logger
    mock_logger.hasHandlers.return_value = False
    logger = configure_stdout_logger("test_logger")
    assert logger == mock_logger
    mock_get_logger.assert_called_once_with("test_logger")
    mock_logger.hasHandlers.assert_called_once()
    mock_logger.addHandler.assert_called_once()
    mock_logger.setLevel.assert_called_once_with(logging.INFO)


def test_configure_stdout_logger_reuses_existing_logger(mocker):
    """
    Test that configure_stdout_logger reuses an existing logger if it already has handlers.
    """
    mock_get_logger = mocker.patch("logging.getLogger")
    mock_logger = mocker.Mock()
    mock_get_logger.return_value = mock_logger
    mock_logger.hasHandlers.return_value = True
    logger = configure_stdout_logger("test_logger")
    assert logger == mock_logger
    mock_get_logger.assert_called_once_with("test_logger")
    mock_logger.hasHandlers.assert_called_once()
    mock_logger.addHandler.assert_not_called()
    mock_logger.setLevel.assert_not_called()
