import json
from random import randint
from unidecode import unidecode
import os
import time

class Hangman :

    def __init__(self) -> None:
        self.word = self.get_word()
        self.lettres_trouvees = []
        self.lettres_fausses = []
        self.mot_faux = []
        self.mot_cache = [lettre if lettre in self.lettres_trouvees else "_" for lettre in self.word]
        self.attempts = 0

    def clear(self) -> None:
        if os.name == "nt":
            os.system("cls")
        elif os.name == "posix":
            os.system("clear")
        else:
            print("OS not supported")
            exit(1)

    def get_word(self) -> str:
        with open("json/dico.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return  unidecode(data["mots"][randint(0, len(data["mots"])-1)])
    
    def check_win(self):
        if self.attempts == 10:
            self.print_lose()
            exit(0)
        if "_" not in self.mot_cache:
            self.print_win()
            exit(0)
    
    def print_win(self) -> None:
        self.clear()
        self.attempts = 11
        self.print_form()
        print("Vous avez gagné ! le mot était bien", self.word, "!")

    def print_lose(self) -> None:
        self.clear()
        self.attempts = 12
        self.print_form()
        print("Vous avez perdu ! le mot était", self.word)
    
    def check_letter(self, lettre : str) -> None:
        if lettre in self.word:
            if not lettre in self.lettres_trouvees:
                self.lettres_trouvees.append(lettre)
                self.mot_cache = [lettre if lettre in self.lettres_trouvees else "_" for lettre in self.word]
        elif not lettre in self.lettres_fausses:
                self.lettres_fausses.append(lettre)
                self.attempts += 1
    
    def check_word(self, word : str) -> None:
        if word == self.word:
            self.mot_cache = [lettre for lettre in word]
        elif not word in self.mot_faux:
            self.mot_faux.append(word)
            self.attempts += 1

    def print_form(self):
        for i in self.recupform():
            print(i)

    def recupform(self):
        x = self.attempts
        with open("json/hangman.json", "r", encoding="utf-8") as f:
            try :
                if type(x) == int:
                    data = json.load(f)
                    return data['form'][str(x)]
                elif type(x) == str:
                    data = json.load(f)
                    return data['form'][x]
                else:
                    return f"Error: {x} is not int or str"
            except KeyError as e:
                return f"Error: {e} key not found"

    def ask_letter(self) -> None:
        lettre = input("Entrez une lettre : ")
        if lettre.strip() and not lettre.isspace():
            if len(lettre) == 1:
                self.check_letter(lettre)
            else:
                self.check_word(lettre)
        else:
            print("Vous devez entrer une lettre ou un mot !")
            time.sleep(2)

    def print_game(self) -> None:
        self.clear()
        self.print_form()
        print(" ".join(self.mot_cache))
        print("\n",f"Vous avez {self.attempts} erreurs")
        print(f"Lettres trouvées : {', '.join(self.lettres_trouvees)}")
        print(f"Mauvaisses lettres : {', '.join(self.lettres_fausses)}")
        print(f"Mauvais mots : {', '.join(self.mot_faux)}")

    def print_debut(self) -> None:
        self.clear()
        print("Bienvenue dans le jeu du pendu !")
        print("Vous avez 10 chances pour trouver le mot")
        time.sleep(2)
    
    def main(self) -> None:
        self.print_debut()
        while True:
            self.print_game()
            self.check_win()
            self.ask_letter()
        



if __name__ == "__main__":
    hangman = Hangman()
    hangman.main()