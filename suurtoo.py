# 3. Lemmikloomade varjupaiga haldamise sĆ¼steem

# EesmĆ¤rk: arendada Pythoni ja Tkinteri abil rakendus, mis simuleerib lemmikloomade varjupaiga haldamise sĆ¼steemi. Rakendus vĆµimaldab kasutajal sisestada, vaadata, muuta ja kustutada lemmikloomade andmeid, sealhulgas nime, liiki, vanust, sugu ja pilti. Iga lemmiklooma kohta genereeritakse sĆ¼steemi lisamisel unikaalne ID.

# Funktsionaalsus:
# * Andmete sisestamine: Kasutajad saavad sisestada lemmikloomade andmeid, sealhulgas nime, liiki (koer, kass jne), vanust, sugu ja laadida Ć¼les pildi. Sisestamisel genereerib sĆ¼steem iga lemmiklooma jaoks unikaalse ID.
# * Andmete vaatamine: Rakendus kuvab kĆµigi varjupaigas olevate lemmikloomade nimekirja. Kasutajad saavad otsida lemmikloomi nende unikaalse ID vĆµi muude omaduste alusel.
# * Andmete muutmine ja Kustutamine: Kasutajad saavad muuta olemasolevate lemmikloomade andmeid vĆµi kustutada neid sĆ¼steemist, et peegeldada lemmikloomade varjupaigas toimuvaid muutusi.
# * Andmete salvestamine: Andmed salvestatakse failisĆ¼steemi, kasutades CSV vĆµi TXT failivormingut, mis vĆµimaldab hĆµlpsat andmete haldamist ja taaskasutamist.

# NĆµuded:
# * Kasutajaliides tuleb luua Tkinteri abil, pakkudes kasutajasĆµbralikku navigeerimist ja interaktsiooni.
# * Rakendus peab tagama andmete jĆ¤rjepidevuse ja turvalisuse, kasutades failipĆµhist salvestusviisi.
# * Unikaalse ID genereerimine peab tagama, et iga lemmiklooma identifikaator on ainulaadne.
# * Lemmikloomade piltide haldamine peab olema integreeritud sĆ¼steemi, vĆµimaldades piltide lihtsat lisamist ja kuvamist koos muu teabega.
# * Failid peavad olema kĆ¤ttesaadavad Githubis
# -----------------------------


import csv
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import random
from PIL import Image, ImageTk
import atexit
import os

class AnimalShelterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lemmikloomade varjupaiga haldamine")

        self.animals = []

        self.create_widgets()
        self.load_data()

        # Register the save_data method to be called when the program exits
        atexit.register(self.save_data)

    def create_widgets(self):
        self.label = tk.Label(self.root, text="Lemmikloomade varjupaik")
        self.label.pack()

        self.search_entry = tk.Entry(self.root)
        self.search_entry.pack()
        self.search_button = tk.Button(self.root, text="Otsi", command=self.search_animals)
        self.search_button.pack()

        self.listbox = tk.Listbox(self.root, width=50)
        self.listbox.pack(pady=10)
        self.listbox.bind("<Double-Button-1>", self.show_animal_details)  # Double-click event handler

        self.add_button = tk.Button(self.root, text="Lisa lemmikloom", command=self.add_animal)
        self.add_button.pack()

        self.delete_button = tk.Button(self.root, text="Kustuta valitud lemmikloom", command=self.delete_animal)
        self.delete_button.pack()

        # Additional window for editing
        self.edit_window = None
        self.edit_index = None

    def load_data(self):
        filename = "varjupaiga_andmed.csv"  # Assuming the file is in the same directory
        if os.path.isfile(filename):  # Check if the file exists
            try:
                with open(filename, 'r', newline='') as file:
                    reader = csv.reader(file)
                    self.animals = list(reader)
                    self.listbox.delete(0, tk.END)
                    for animal in self.animals:
                        self.listbox.insert(tk.END, animal[1])  # Inserting only the names
            except FileNotFoundError:
                messagebox.showinfo("Faili teade", "Andmefaili ei leitud.")
        else:
            # If the file doesn't exist, create an empty list
            self.animals = []

    def add_animal(self):
        animal_data = []
        animal_data.append(self.generate_unique_id()) # Unique ID
        name = simpledialog.askstring("Sisesta lemmiklooma nimi", "Sisesta lemmiklooma nimi:")
        animal_data.append(name)
        species = simpledialog.askstring("Sisesta liik", "Sisesta liik (nt. koer, kass):")
        animal_data.append(species)
        age = simpledialog.askinteger("Sisesta vanus", "Sisesta vanus:")
        animal_data.append(age)
        gender = simpledialog.askstring("Sisesta sugu", "Sisesta sugu:")
        animal_data.append(gender)

        # Ask the user to select an image file
        file_path = filedialog.askopenfilename(title="Vali pildi fail", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            animal_data.append(file_path)
        else:
            animal_data.append("")  # If no file is selected, store an empty string

        self.animals.append(animal_data)
        self.listbox.insert(tk.END, name)  # Inserting only the name
        self.save_data()  # Save data after adding an animal

    def delete_animal(self):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            self.listbox.delete(index)
            del self.animals[index]
            self.save_data()  # Save data after deleting an animal

    def search_animals(self):
        search_term = self.search_entry.get().lower()
        self.listbox.delete(0, tk.END)
        for animal in self.animals:
            if search_term in animal[1].lower():  # Search by name (index 1)
                self.listbox.insert(tk.END, animal[1])  # Inserting only the names

    def show_animal_details(self, event):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            animal_data = self.animals[index]

            if self.edit_window:
                self.edit_window.destroy()

            self.edit_window = tk.Toplevel(self.root)
            self.edit_window.title("Looma detailid")
            self.edit_window.geometry("400x300")

            labels = ["ID", "Nimi", "Liik", "Vanus", "Sugu", "Pilt"]
            for label, detail in zip(labels, animal_data):
                detail_label = tk.Label(self.edit_window, text=f"{label}: {detail}")
                detail_label.pack()

            # Display the image
            picture_path = animal_data[-1]
            if picture_path:  # Check if there's a picture path available
                try:
                    image = Image.open(picture_path)
                    image.thumbnail((200, 200))
                    photo = ImageTk.PhotoImage(image)

                    image_label = tk.Label(self.edit_window, image=photo)
                    image_label.image = photo
                    image_label.pack()
                except Exception as e:
                    print(f"Error loading image: {e}")

            self.edit_index = index

    def generate_unique_id(self):
        while True:
            unique_id = ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz', k=6))
            if unique_id not in [animal[0] for animal in self.animals]:
                return unique_id

    def save_data(self):
        filename = "varjupaiga_andmed.csv"  # Assuming the file is in the same directory
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(self.animals)

root = tk.Tk()
app = AnimalShelterApp(root)
root.mainloop()







   







