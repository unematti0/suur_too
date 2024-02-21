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

class AnimalShelterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lemmikloomade varjupaiga haldamine")

        self.animals = []

        self.create_widgets()

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

        self.load_button = tk.Button(self.root, text="Laadi varjupaiga andmed", command=self.load_data)
        self.load_button.pack()

        self.add_button = tk.Button(self.root, text="Lisa lemmikloom", command=self.add_animal)
        self.add_button.pack()

        self.delete_button = tk.Button(self.root, text="Kustuta valitud lemmikloom", command=self.delete_animal)
        self.delete_button.pack()

        self.save_button = tk.Button(self.root, text="Salvesta andmed", command=self.save_data)
        self.save_button.pack()

        # Additional window for editing
        self.edit_window = None
        self.edit_index = None

    def load_data(self):
        filename = filedialog.askopenfilename(title="Vali fail", filetypes=[("CSV files", "*.csv")])
        if filename:
            with open(filename, 'r', newline='') as file:
                reader = csv.reader(file)
                self.animals = list(reader)
                self.listbox.delete(0, tk.END)
                for animal in self.animals:
                    self.listbox.insert(tk.END, animal[1])  # Inserting only the names

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
        picture_name = simpledialog.askstring("Sisesta pildi nimi", "Sisesta pildi nimi:")
        animal_data.append(picture_name)

        self.animals.append(animal_data)
        self.listbox.insert(tk.END, name)  # Inserting only the name

    def delete_animal(self):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            self.listbox.delete(index)
            del self.animals[index]

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
            self.edit_window.geometry("300x200")

            labels = ["Nimi", "Liik", "Vanus", "Sugu", "Pildi nimi"]
            for label, detail in zip(labels, animal_data[1:]):  # Skip unique ID, start from index 1
                detail_label = tk.Label(self.edit_window, text=f"{label}: {detail}")
                detail_label.pack()

            for i, label in enumerate(labels):  # Skip unique ID, start from index 1
                edit_button = tk.Button(self.edit_window, text=f"Muuda {label}", command=lambda i=i: self.edit_animal_detail(index, i+1))
                edit_button.pack()

            self.edit_index = index

    def edit_animal_detail(self, index, detail_index):
        animal_data = self.animals[index]

        new_value = simpledialog.askstring(f"Muuda {animal_data[detail_index]}", f"Sisesta uus {animal_data[detail_index]}:", initialvalue=animal_data[detail_index])
        if new_value:
            animal_data[detail_index] = new_value

        self.animals[index] = animal_data

        self.listbox.delete(0, tk.END)
        for animal in self.animals:
            self.listbox.insert(tk.END, animal[1])  # Inserting only the names

        self.edit_window.destroy()

    def generate_unique_id(self):
        if self.animals:
            last_id = int(self.animals[-1][0])
            return str(last_id + 1)
        else:
            return "1"

    def save_data(self):
        filename = filedialog.asksaveasfilename(title="Vali fail", defaultextension=".csv",
                                                filetypes=[("CSV files", "*.csv")])
        if filename:
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(self.animals)
            messagebox.showinfo("Salvestamine", "Andmed on edukalt salvestatud.")

root = tk.Tk()
app = AnimalShelterApp(root)
root.mainloop()





   







