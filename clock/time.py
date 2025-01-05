import customtkinter as ctk
import time


class TimeFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.label = ctk.CTkLabel(self)
        self.label.pack(pady=20)
        self.update_time()

    def update_time(self):
        h = time.strftime("%I")
        m = time.strftime("%M")
        s = time.strftime("%S")
        am_pm = time.strftime("%p")
        text = f"{h}:{m}:{s} {am_pm}"
        self.label.configure(text=text)
        self.label.after(1000, self.update_time)
    
if __name__ == "__main__":
    root = ctk.CTk()
    timer = TimeFrame(root)
    timer.pack(expand=True, fill=ctk.BOTH)
    root.geometry("400x400")
    root.mainloop()
