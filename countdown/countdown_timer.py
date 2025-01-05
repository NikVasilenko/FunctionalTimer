import customtkinter as ctk
import threading
import pygame

class CountdownTimer(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.font = "Helvetica"
        # Labels and Entry fields for minutes and seconds
        self.minutes_label = ctk.CTkLabel(self, font=(self.font, 20), text="Minutes:")
        self.minutes_label.pack(pady=5)

        self.minutes_entry = ctk.CTkEntry(self, font=(self.font, 20))
        self.minutes_entry.pack(pady=5)

        self.seconds_label = ctk.CTkLabel(self, font=(self.font, 20), text="Seconds:")
        self.seconds_label.pack(pady=5)

        self.seconds_entry = ctk.CTkEntry(self, font=(self.font, 20))
        self.seconds_entry.pack(pady=5)

        # Label to display the countdown time
        self.time_label = ctk.CTkLabel(self, font=(self.font, 30), text="Time: 00:00:00")
        self.time_label.pack(pady=10)

        # Frame for bottom buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(side=ctk.BOTTOM, fill=ctk.X, pady=10)

        # Start and Stop buttons
        self.start_button = ctk.CTkButton(button_frame, text="Start", command=self.start_thread)
        self.start_button.pack(side=ctk.LEFT, padx=20)

        self.stop_button = ctk.CTkButton(button_frame, text="Stop", command=self.stop)
        self.stop_button.pack(side=ctk.RIGHT, padx=20)

        self.stop_loop = False

    def start_thread(self):
        t = threading.Thread(target=self.start)
        t.start()

    def start(self):
        self.stop_loop = False

        minutes = 0
        seconds = 0

        # Get input from the user
        try:
            minutes_input = self.minutes_entry.get().strip()
            seconds_input = self.seconds_entry.get().strip()

            #error checking for the input fields
            if not minutes_input.isdigit() and minutes_input != "":
                raise ValueError("Invalid input for minutes.")
            if not seconds_input.isdigit() and seconds_input != "":
                raise ValueError("Invalid input for seconds.")

            minutes = int(minutes_input) if minutes_input.isdigit() else 0
            seconds = int(seconds_input) if seconds_input.isdigit() else 0 
        except ValueError as e:
            print(e)
            self.time_label.configure(text="Invalid input!")
            return

        time_in_seconds = minutes * 60 + seconds

        while time_in_seconds > 0 and not self.stop_loop:
            time_in_seconds -= 1
            
            #divide time_in_seconds by 60 to attribute whole part to minutes and reminder to seconds
            minutes, seconds = divmod(time_in_seconds, 60)

            self.time_label.configure(text=f"Time: {minutes:02d}:{seconds:02d}")

            #update the gui
            self.update()
            
            #pause for 1 sec for the UI fluency
            time.sleep(1)

        if time_in_seconds == 0:
            self.time_label.configure(text="Time: 00:00:00")
            self.play_alarm()

    def stop(self):
        self.stop_loop = True
        self.time_label.configure(text="Time: 00:00:00")

        #Clear the input fields
        self.minutes_entry.delete(0, ctk.END)
        self.seconds_entry.delete(0, ctk.END)

    def play_alarm(self):
        #play alarm sound indefinitely and show the pop-up window
        pygame.mixer.init()
        pygame.mixer.music.load("static/sound/alarm.wav")
        pygame.mixer.music.play(loops=-1)

        self.alarm_popup = ctk.CTkToplevel(self)
        self.alarm_popup.title("Alarm!")
        self.alarm_popup.geometry("300x150")

        

        label = ctk.CTkLabel(self.alarm_popup, text="Time's up!", font=("Helvetica", 20))
        label.pack(pady=20)

        stop_button = ctk.CTkButton(self.alarm_popup, text="End Alarm", font=("Helvetica", 15), command=self.stop_alarm)
        stop_button.pack(pady=20)

    def stop_alarm(self):
        pygame.mixer.music.stop()
        
        if self.alarm_popup:
            self.alarm_popup.destroy()


if __name__ == "__main__":
    root = ctk.CTk()
    timer = CountdownTimer(root)
    timer.pack(expand=True, fill=ctk.BOTH)
    root.geometry("400x400")
    root.mainloop()