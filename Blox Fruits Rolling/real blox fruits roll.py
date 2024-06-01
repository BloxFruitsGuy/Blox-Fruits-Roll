import random
import tkinter as tk
import time
import os
import json

class FruitRollerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fruit Roller")
        self.inventory = {}
        self.load_inventory()  # Load inventory from file
        self.words = [
            "Rocket", "Spin", "Chop", "Spring", "Bomb", "Smoke", "Spike", "Flame",
            "Falcon", "Ice", "Sand", "Dark", "Diamond", "Light", "Rubber", "Barrier",
            "Ghost", "Magma", "Quake", "Buddha", "Love", "Spider", "Sound", "Phoenix",
            "Portal", "Rumble", "Pain", "Blizzard", "Gravity", "Mammoth", "T-Rex",
            "Dough", "Shadow", "Venom", "Control", "Spirit", "Dragon", "Leopard", "Kitsune"
        ]
        self.rarest_fruit = None
        self.last_roll_time = 0
        self.remaining_time = tk.StringVar()
        self.invalid_code_message = tk.StringVar()
        self.cooldown_seconds = 7200
        
        # Path to store last roll time
        self.last_roll_time_path = "LastRollTime.txt"
        
        # Load last roll time from file
        self.load_last_roll_time()
        
        # Allow the window to be resizable
        self.root.resizable(True, True)

        # Create and place the weight entry box with a label
        weight_label = tk.Label(root, text="Weight Multiplier:")
        weight_label.pack(padx=20, pady=5)

        self.weight_entry = tk.Entry(root)
        self.weight_entry.pack(padx=20, pady=5)
        self.weight_entry.insert(0, "1.5")

        # Create and place the recommended weight value label
        recommended_label = tk.Label(root, text="Recommended Weight Value Is 1.5")
        recommended_label.pack(padx=20, pady=5)

        # Create and place the button with padding
        self.roll_button = tk.Button(root, text="Roll A Fruit", command=self.roll_fruit)
        self.roll_button.pack(padx=20, pady=20)

        # Create and place the remaining cooldown label
        self.cooldown_label = tk.Label(root, textvariable=self.remaining_time)
        self.cooldown_label.pack(padx=20, pady=5)

        # Create and place the inventory display
        self.inventory_label = tk.Label(root, text="Inventory:")
        self.inventory_label.pack(padx=20, pady=5)

        self.inventory_listbox = tk.Listbox(root)
        self.inventory_listbox.pack(padx=20, pady=5)

        # Create and place the rarest fruit display
        self.rarest_fruit_label = tk.Label(root, text="Rarest Fruit: None")
        self.rarest_fruit_label.pack(padx=20, pady=5)

        # Create and place the fruit rolled display with a larger font size
        self.rolled_fruit_label = tk.Label(root, text="", font=("Helvetica", 16))
        self.rolled_fruit_label.pack(padx=20, pady=5)

        # Create and place the Developer Code entry box with a label
        developer_code_label = tk.Label(root, text="Developer Code:")
        developer_code_label.pack(padx=20, pady=5)

        self.developer_code_entry = tk.Entry(root)
        self.developer_code_entry.pack(padx=20, pady=5)

        # Create and place the invalid code message label
        self.invalid_code_label = tk.Label(root, textvariable=self.invalid_code_message, fg="red")
        self.invalid_code_label.pack(padx=20, pady=5)

        self.reset_button = tk.Button(root, text="Reset Timer", command=self.check_developer_code)
        self.reset_button.pack(padx=20, pady=20)

        # Create and place the save inventory button
        self.save_inventory_button = tk.Button(root, text="Save Inventory", command=self.save_inventory)
        self.save_inventory_button.pack(padx=20, pady=20)

        # Initialize timer if there's remaining cooldown
        if time.time() - self.last_roll_time < self.cooldown_seconds:
            self.roll_button.config(state=tk.DISABLED)
            self.update_timer()
            self.root.after(1000, self.update_timer)

    def load_last_roll_time(self):
        try:
            with open(self.last_roll_time_path, "r") as file:
                self.last_roll_time = float(file.read())
        except (FileNotFoundError, ValueError):
            self.last_roll_time = 0

    def save_last_roll_time(self):
        with open(self.last_roll_time_path, "w") as file:
            file.write(str(self.last_roll_time))

    def load_inventory(self):
        try:
            with open("inventory.json", "r") as file:
                self.inventory = json.load(file)
        except FileNotFoundError:
            pass

    def save_inventory(self):
        with open("inventory.json", "w") as file:
            json.dump(self.inventory, file)

    def roll_fruit(self):
        current_time = time.time()
        if current_time - self.last_roll_time >= self.cooldown_seconds:
            self.pick_random_word()
            self.last_roll_time = current_time
            self.save_last_roll_time()
            self.roll_button.config(state=tk.DISABLED)
            self.update_cooldown()
            self.root.after(self.cooldown_seconds * 1000, self.enable_roll_button)
        else:
            remaining_time = int(self.cooldown_seconds - (current_time - self.last_roll_time))
            hours = remaining_time // 3600
            minutes = (remaining_time % 3600) // 60
            seconds = remaining_time % 60
            self.remaining_time.set(f"Next roll in: {hours} hours, {minutes} minutes, and {seconds} seconds")

    def update_timer(self):
        current_time = time.time()
        remaining_time = int(self.cooldown_seconds - (current_time - self.last_roll_time))
        if remaining_time <= 0:
            self.remaining_time.set("")
        else:
            hours = remaining_time // 3600
            minutes = (remaining_time % 3600) // 60
            seconds = remaining_time % 60
            self.remaining_time.set(f"Next roll in: {hours} hours, {minutes} minutes, and {seconds} seconds")
            self.root.after(1000, self.update_timer)

    def enable_roll_button(self):
        self.roll_button.config(state=tk.NORMAL)

    def update_cooldown(self):
        self.remaining_time.set("Next roll in: 2 hours")

    def check_developer_code(self):
        code = self.developer_code_entry.get()
        if code == "928492":
            self.last_roll_time = 0
            self.save_last_roll_time()
            self.roll_button.config(state=tk.NORMAL)
            self.remaining_time.set("Developer code accepted, timer reset.")
            self.invalid_code_message.set("")
        else:
            self.invalid_code_message.set("Invalid developer code.")

    def pick_random_word(self):
        try:
            # Get the multiplier from the entry box
            multiplier = float(self.weight_entry.get())

            # Define weights for each word based on their position inversely and the multiplier
            weights = [1 / ((i + 1) ** multiplier) for i in range(len(self.words))]

            # Normalize weights so they sum up to 1
            total_weight = sum(weights)
            weights = [weight / total_weight for weight in weights]

            # Pick a random word using weighted probability
            random_word = random.choices(self.words, weights=weights)[0]

            # Add the word to the inventory and update the listbox
            if random_word in self.inventory:
                self.inventory[random_word] += 1
            else:
                self.inventory[random_word] = 1
            
            # Clear the listbox and repopulate it with the updated inventory
            self.inventory_listbox.delete(0, tk.END)
            for item, count in self.inventory.items():
                display_word = f"{item} x{count}" if count > 1 else item
                self.inventory_listbox.insert(tk.END, display_word)

            # Update the rarest fruit if the new fruit is rarer
            if self.rarest_fruit is None or self.words.index(random_word) > self.words.index(self.rarest_fruit):
                self.rarest_fruit = random_word
                self.rarest_fruit_label.config(text=f"Rarest Fruit: {self.rarest_fruit}")

            # Update the fruit rolled label
            self.rolled_fruit_label.config(text=f"Fruit Rolled: {random_word}")
            
            # Save inventory
            self.save_inventory()
        except ValueError:
            tk.messagebox.showerror("Input Error", "Please enter a valid number for the weight multiplier.")

    def __del__(self):
        self.save_inventory()  # Save inventory when the application exits

# Create tkinter window
root = tk.Tk()
app = FruitRollerApp(root)

# Run the tkinter event loop
root.mainloop()

