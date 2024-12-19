import customtkinter as ctk
from CountdownTimer import CountdownTimer
from Time import TimeFrame
from Workout import WorkoutFrame


def create_menu(parent, main_frame, show_time, show_countdown, show_workout):
    menu = ctk.CTkFrame(parent)

    # Create buttons for the menu
    time_button = ctk.CTkButton(menu, text="Time", command=show_time)
    countdown_button = ctk.CTkButton(menu, text="Countdown", command=show_countdown)
    workout_button = ctk.CTkButton(menu, text="Workout", command=show_workout)

    # Place buttons in a grid layout
    time_button.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    countdown_button.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
    workout_button.grid(row=0, column=2, sticky="ew", padx=5, pady=5)

    # Configure grid columns to expand evenly
    menu.grid_columnconfigure((0, 1, 2), weight=1)

    menu.pack(side=ctk.BOTTOM, fill=ctk.X)
    return menu


def clear_widgets(main_frame):
    for widget in main_frame.winfo_children():
        widget.pack_forget()


def main():
    app = ctk.CTk()
    app.title("The Functional Timer")
    app.geometry("430x500")
    app.minsize(300, 300)

    main_frame = ctk.CTkFrame(app)
    main_frame.pack(expand=True, fill=ctk.BOTH)

    countdown_frame = CountdownTimer(main_frame)
    time_frame = TimeFrame(main_frame)
    workout_frame = WorkoutFrame(main_frame)

    def show_time():
        clear_widgets(main_frame)
        time_frame.pack(expand=True, fill=ctk.BOTH)

    def show_countdown():
        clear_widgets(main_frame)
        countdown_frame.pack(expand=True, fill=ctk.BOTH)

    def show_workout():
        clear_widgets(main_frame)
        workout_frame.pack(expand=True, fill=ctk.BOTH)

    create_menu(app, main_frame, show_time, show_countdown, show_workout)

    show_time()

    app.mainloop()


if __name__ == "__main__":
    main()