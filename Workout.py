import customtkinter as ctk
from PIL import Image
import time
import threading
import pygame


class WorkoutFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        #Load button icons
        on = Image.open("sound_.png")
        off = Image.open("sound_no.png")
        play = Image.open("play_button.png")
        pause = Image.open("pause_button.png")
        self.sound_on = ctk.CTkImage(on)
        self.sound_off = ctk.CTkImage(off)
        self.resume_b = ctk.CTkImage(play)
        self.pause_b = ctk.CTkImage(pause)

        pygame.mixer.init()
        #Load the music
        self.end_workout_music = "alarm.wav"
        self.rest_music = "rest.wav"
        self.work_music = "work.wav"

        # Variables for settings
        self.work_time = 0
        self.rest_time = 0
        self.rounds = 0
        self.current_phase = "work"
        self.remaining_seconds = 0
        self.rounds_left = 0

        #Flags for state control to differentiate stop from pause, mute functionality
        self.stop_loop = False
        self.t_is_paused = False
        self.is_muted = False
        self.music_paused = False
        self.timer_is_running = False 

        # Button to open settings
        self.settings_button = ctk.CTkButton(self, text="Set the workout", command=self.open_settings)
        self.settings_button.pack(pady=10)

        # Timer display label
        self.time_label = ctk.CTkLabel(self, text="00:00", font=("Helvetica", 50))
        self.time_label.place(relx= 0.5, rely= 0.5, anchor="center")

        # Status label (Work/Rest)
        self.status_label = ctk.CTkLabel(self, text="Get Ready!", font=("Helvetica", 20))
        self.status_label.place(relx= 0.5, rely = 0.8, anchor="center")

        #Round number label
        self.round_status = ctk.CTkLabel(self, text="")
        self.round_status.place(relx=0.5, rely= 0.3, anchor="center")

        # Start/Stop buttons with respectfull frame for ordering purposes
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(side= ctk.BOTTOM, fill= ctk.X)

        self.start_button = ctk.CTkButton(self.button_frame, text="Start", command=self.start_thread)
        self.start_button.pack(side=ctk.LEFT, padx= 10, pady= 10)

        self.stop_button = ctk.CTkButton(self.button_frame, text="Stop", command=self.stop)
        self.stop_button.pack(side=ctk.RIGHT, padx = 10, pady=10)
        
        # Controll Buttons
        self.mute_button = ctk.CTkButton(self, text="", command=self.mute, image=self.sound_on, height=10, width=10)
        self.mute_button.place(relx= 0.9, rely=0.025)


        self.pause_button = ctk.CTkButton(self, text="", command=self.t_pause, image=self.pause_b, height=10, width=10)
    
        self.resume_button = ctk.CTkButton(self, text ="", command=self.t_resume, state="disabled", image=self.resume_b, height=10, width=10)
        

    def open_settings(self):
        SettingsWindow(self)
    
    def destroy_buttons(self):
        self.pause_button.place_forget()
        self.resume_button.place_forget()

    def start_thread(self):
        t = threading.Thread(target=self.start)
        t.start()
        self.start_button.configure(state="disabled")
    

    def t_pause(self):
        """Pause both timer and music."""
        
        self.t_is_paused = True
        self.stop_loop = True 
        self.timer_running = False

        pygame.mixer.music.pause()
        self.music_paused = True

        self.pause_button.configure(state="disabled")
        self.resume_button.configure(state="normal")

    def t_resume(self):
        """Resume both timer and music."""
        if self.t_is_paused:
            self.t_is_paused = False
            self.timer_running = True
            self.stop_loop = False

            
            self.music_paused = False
            pygame.mixer.music.unpause()
            

            threading.Thread(target=self.run_timer).start()

            self.resume_button.configure(state="disabled")
            self.pause_button.configure(state="normal")

    def start(self):
        self.stop_loop = False

        self.pause_button.place(relx = 0.88, rely= 0.6)
        self.resume_button.place(relx = 0.03, rely= 0.6)

        
        if not self.t_is_paused:
            if self.work_time <= 0 or self.rest_time <= 0 or self.rounds <= 0:
                self.status_label.configure(text="Please set valid values!", fg="black")
                return

            self.rounds_left = self.rounds
            self.current_phase = "work"
            self.remaining_seconds = self.work_time

        self.timer_is_running = True
        self.is_paused = False

        self.run_timer()

    def run_timer(self):
        """Run the countdown for each phase + phase specific music."""
        self.timer_is_running = True
        if not self.t_is_paused:
            self.play_music(self.work_music if self.current_phase == "work" else self.rest_music)

        while self.remaining_seconds > 0 and not self.stop_loop:
            if self.stop_loop:
                return
            if self.t_is_paused:
                break

            minutes, seconds = divmod(self.remaining_seconds, 60)
            self.time_label.configure(text=f"{minutes:02d}:{seconds:02d}")
            self.status_label.configure(text=f"{self.current_phase.title()}")
            self.round_status.configure(text=f"{self.rounds_left}")

        
            if self.current_phase == "work":
                self.update_color(bg="green")
            else:
                self.update_color(bg="red")

            self.update()
            time.sleep(1)
            self.remaining_seconds -= 1

        if self.stop_loop:
            return

        
        if self.remaining_seconds == 0:
            if self.current_phase == "work":
                self.current_phase = "rest"
                self.remaining_seconds = self.rest_time
                self.rounds_left -= 1
                self.update_color(bg="red")
 
            
            elif self.rounds_left < 1:
                self.status_label.configure(text="Workout Complete!")
                self.time_label.configure(text="00:00")
                self.update_color(bg="blue")  
                self.play_music(self.end_workout_music, n=1)
                # Mark the timer as stopped
                self.timer_is_running = False 
                self.stop_loop = True
                self.start_button.configure(state="normal")
                self.destroy_buttons()
                return
            else:
                self.current_phase = "work"
                self.remaining_seconds = self.work_time
                self.update_color(bg="green")

        
        if self.rounds_left > 0 or self.current_phase == "rest":
            self.run_timer() 

        if not self.stop_loop:
            self.play_music(self.work_music if self.current_phase == "work" else self.rest_music)
        
        self.start_button(state="normal")

    def update_color(self, bg):
        """Update the background and foreground colors dynamically."""
        
        self.time_label.configure(fg_color=bg)
        self.status_label.configure(fg_color=bg)
        self.button_frame.configure(fg_color=bg)
        self.configure(fg_color=bg)
        self.round_status.configure(fg_color=bg)

    def stop(self):
        self.stop_loop = True
        self.status_label.configure(text="Stopped")
        self.time_label.configure(text="00:00")
        self.update_color(bg="Blue")
        pygame.mixer.music.stop()
        self.destroy_buttons()
        self.start_button.configure(state="normal")


    def play_music(self, file, n=None):
        """Manages the music file loading, and playing."""
        if n is None:
            n = -1
        if not self.is_muted:
            pygame.mixer.music.stop() 
            pygame.mixer.music.load(file)
            pygame.mixer.music.play(loops=n)
    
    def mute(self):
        """Mute or unmute the sound."""
        if self.is_muted:
            self.is_muted = False
            self.mute_button.configure(image=self.sound_on)
            pygame.mixer.music.set_volume(1.0)
        else:
            self.is_muted = True
            self.mute_button.configure(image=self.sound_off)
            pygame.mixer.music.set_volume(0.0) 
        

class SettingsWindow(ctk.CTkToplevel):
    """Settings window for inputting work/rest times and rounds."""
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Settings")
        self.geometry("300x200")

        self.parent = parent

        ctk.CTkLabel(self, text="Work Time (seconds):").grid(row=0, column=0, padx=10, pady=10)
        self.work_entry = ctk.CTkEntry(self)
        self.work_entry.grid(row=0, column=1)

        ctk.CTkLabel(self, text="Rest Time (seconds):").grid(row=1, column=0, padx=10, pady=10)
        self.rest_entry = ctk.CTkEntry(self)
        self.rest_entry.grid(row=1, column=1)

        ctk.CTkLabel(self, text="Number of Rounds:").grid(row=2, column=0, padx=10, pady=10)
        self.rounds_entry = ctk.CTkEntry(self)
        self.rounds_entry.grid(row=2, column=1)

        save_button = ctk.CTkButton(self, text="Save", command=self.save_settings)
        save_button.grid(row=3, column=0, columnspan=2, pady=20)

    def save_settings(self):
        try:
            work_time = int(self.work_entry.get())
            rest_time = int(self.rest_entry.get())
            rounds = int(self.rounds_entry.get())

            if work_time <= 0 or rest_time <= 0 or rounds <= 0:
                raise ValueError

            self.parent.work_time = work_time
            self.parent.rest_time = rest_time
            self.parent.rounds = rounds
            self.parent.status_label.configure(text="The Workout is set!")
            self.destroy()

        except ValueError:
            self.parent.status_label.configure(text="Invalid Input!")


if __name__ == "__main__":
    root = ctk.CTk()
    timer = WorkoutFrame(root)
    timer.pack(expand=True, fill=ctk.BOTH)
    root.geometry("400x400")
    root.mainloop()