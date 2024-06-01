import random
import tkinter as tk

class FruitRollerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fruit Roller")
        self.inventory = {}
        self.words = [
            "Rocket", "Spin", "Chop", "Spring", "Bomb", "Smoke", "Spike", "Flame",
            "Falcon", "Ice", "Sand", "Dark", "Diamond", "Light", "Rubber", "Barrier",
            "Ghost", "Magma", "Quake", "Buddha", "Love", "Spider", "Sound", "Phoenix",
            "Portal", "Rumble", "Pain", "Blizzard", "Gravity", "Mammoth", "T-Rex",
            "Dough", "Shadow", "Venom", "Control", "Spirit", "Dragon", "Leopard", "Kitsune"
        ]
        self.rarest_fruit = None
        
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
        roll_button = tk.Button(root, text="Roll A Fruit", command=self.pick_random_word)
        roll_button.pack(padx=20, pady=20)

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
                # Update the existing entry in the listbox
                for idx, item in enumerate(self.inventory_listbox.get(0, tk.END)):
                    if item.startswith(random_word):
                        self.inventory_listbox.delete(idx)
                        break
            else:
                self.inventory[random_word] = 1
            
            display_word = f"{random_word} x{self.inventory[random_word]}" if self.inventory[random_word] > 1 else random_word
            self.inventory_listbox.insert(tk.END, display_word)

            # Update the rarest fruit if the new fruit is rarer
            if self.rarest_fruit is None or self.words.index(random_word) > self.words.index(self.rarest_fruit):
                self.rarest_fruit = random_word
                self.rarest_fruit_label.config(text=f"Rarest Fruit: {self.rarest_fruit}")

            # Update the fruit rolled label
            self.rolled_fruit_label.config(text=f"Fruit Rolled: {random_word}")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number for the weight multiplier.")

# Create tkinter window
root = tk.Tk()
app = FruitRollerApp(root)

# Run the tkinter event loop
root.mainloop()
