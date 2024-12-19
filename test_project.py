import pytest
from unittest.mock import MagicMock, patch
import customtkinter as ctk
from CountdownTimer import CountdownTimer
from Time import TimeFrame
from Workout import WorkoutFrame
from project import create_menu, clear_widgets, main


@pytest.fixture
def setup_main_frame():
    app = ctk.CTk()
    main_frame = ctk.CTkFrame(app)
    main_frame.pack(expand=True, fill=ctk.BOTH)
    yield main_frame
    app.destroy()


def test_create_menu(setup_main_frame):
    main_frame = setup_main_frame

    show_time = MagicMock()
    show_countdown = MagicMock()
    show_workout = MagicMock()

    menu = create_menu(main_frame, main_frame, show_time, show_countdown, show_workout)

    assert isinstance(menu, ctk.CTkFrame)
    assert len(menu.winfo_children()) == 3 

    buttons = menu.winfo_children()
    buttons[0].invoke()
    buttons[1].invoke()
    buttons[2].invoke()

    show_time.assert_called_once()
    show_countdown.assert_called_once()
    show_workout.assert_called_once()


def test_clear_widgets(setup_main_frame):
    main_frame = setup_main_frame

    for _ in range(3):
        ctk.CTkLabel(main_frame, text="Test").pack()

    assert len(main_frame.winfo_children()) == 3

    clear_widgets(main_frame)



@patch("project.create_menu")
@patch("project.CountdownTimer")
@patch("project.TimeFrame")
@patch("project.WorkoutFrame")
def test_main(mock_workout_frame, mock_time_frame, mock_countdown_timer, mock_create_menu):
    with patch("customtkinter.CTk.mainloop", return_value=None):
        main()

    mock_countdown_timer.assert_called_once()
    mock_time_frame.assert_called_once()
    mock_workout_frame.assert_called_once()
    mock_create_menu.assert_called_once()


if __name__ == "__main__":
    pytest.main()