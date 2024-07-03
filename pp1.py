import tkinter as tk
from tkinter import messagebox
import webbrowser
import datetime
import os
import subprocess
import speech_recognition as sr
import random
import openai

class Model:
    def __init__(self):
        pass

    def handle_user_command(self, command):
        if "hello" in command or "hi" in command:
            return "Hello! How can I assist you today?"
        elif "open website" in command:
            website = command.split("open website ")[1]
            return self.open_website(website)
        elif "play music" in command:
            return self.play_music()
        elif "check time" in command:
            return self.what_the_time()
        elif "use artificial intelligence" in command:
            prompt = command.split("use artificial intelligence ")[1]
            return self.generate_ai_response(prompt)
        elif "search Google for" in command:
            query = command.split("search Google for ")[1]
            return self.search_google(query)
        elif "open safari" in command:
            return self.open_browser("Safari")
        elif "open chrome" in command:
            return self.open_browser("Chrome")
        elif "open firefox" in command:
            return self.open_browser("Firefox")
        elif "open browser" in command:
            return self.open_browser()
        elif "open YouTube" in command:
            return self.open_youtube()
        else:
            return "Sorry, I didn't understand that command."

    def open_website(self, website):
        if not website.startswith("http://") and not website.startswith("https://"):
            website = "http://" + website
        try:
            webbrowser.open(website)
            return f"Opening {website}"
        except Exception as e:
            return f"Failed to open {website}: {str(e)}"

    def play_music(self):
        try:
            self.play_music_script()
            return "Playing music"
        except Exception as e:
            return f"Failed to play music: {str(e)}"

    def play_music_script(self):
        applescript = """
        tell application "Music"
            activate
            play
        end tell
        """
        subprocess.run(['osascript', '-e', applescript])

    def what_the_time(self):
        now = datetime.datetime.now()
        return f"The current time is {now.strftime('%H:%M')}"

    def generate_ai_response(self, prompt):
        openai.api_key = "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" 
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.choices[0].text.strip()

    def search_google(self, query):
        search_url = f"https://www.google.com/search?q={query}"
        return self.open_website(search_url)

    def open_browser(self, browser=None):
        try:
            if browser:
                subprocess.run(['open', '-a', browser])
                return f"Opening {browser}"
            else:
                webbrowser.open_new("about:blank") 
                return "Opening default browser"
        except Exception as e:
            return f"Failed to open browser: {str(e)}"

    def open_youtube(self):
        try:
            webbrowser.open("https://www.youtube.com")
            return "Opening YouTube"
        except Exception as e:
            return f"Failed to open YouTube: {str(e)}"

class LoginView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.title("Voice Assistant Login")
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        self.username_label = tk.Label(self, text="Username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)

        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        self.password_label = tk.Label(self, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)

        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        self.login_button = tk.Button(self, text="Login", command=self.handle_login)
        self.login_button.grid(row=2, column=1, padx=10, pady=5)

        self.bind("<Return>", lambda event: self.handle_login())

    def handle_login(self, event=None):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.controller.validate_credentials(username, password):
            self.controller.login_successful()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

class Controller:
    def __init__(self):
        self.model = Model()
        self.view = LoginView(self)
        self.credentials = {"admin": "123"}  
        self.recognizer = sr.Recognizer()

    def validate_credentials(self, username, password):
        if username in self.credentials and self.credentials[username] == password:
            return True
        return False

    def login_successful(self):
        self.view.destroy()
        self.main_view = MainView(self)

    def handle_user_input(self, user_input):
        return self.model.handle_user_command(user_input)

    def run(self):
        self.view.mainloop()

    def take_voice_input(self):
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.recognizer.listen(source)

            try:
                print("Recognizing...")
                command = self.recognizer.recognize_google(audio)
                print(f"User said: {command}")
                return command
            except sr.UnknownValueError:
                print("Sorry, I could not understand what you said.")
            except sr.RequestError as e:
                print(f"Could not request results: {e}")

class MainView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.title("Voice Assistant")
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        self.command_entry = tk.Entry(self, width=50)
        self.command_entry.pack(pady=10)

        self.submit_button = tk.Button(self, text="Submit", command=self.handle_submit)
        self.submit_button.pack()

        self.voice_button = tk.Button(self, text="Voice Input", command=self.listen_for_voice_command)
        self.voice_button.pack()

        self.result_label = tk.Label(self, text="", wraplength=400, justify=tk.LEFT)
        self.result_label.pack(pady=10)

        self.command_entry.bind("<Return>", lambda event: self.handle_submit())

    def handle_submit(self, event=None):
        user_input = self.command_entry.get()
        result = self.controller.handle_user_input(user_input)
        self.update_result(result)

    def update_result(self, result):
        self.result_label.config(text=result)

    def listen_for_voice_command(self):
        voice_command = self.controller.take_voice_input()
        if voice_command:
            self.command_entry.delete(0, tk.END)
            self.command_entry.insert(0, voice_command)
            self.handle_submit()

if __name__ == "__main__":
    controller = Controller()
    controller.run()
