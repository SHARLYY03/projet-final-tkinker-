import tkinter as tk
from tkinter import ttk
import re

class Calculatrice:
    def __init__(self, master):
        self.master = master
        self.master.title("Calculatrice")
        self.master.geometry("350x450")
        self.master.resizable(False, False)
        self.master.configure(bg="#f0f0f0")
        
        # Variable pour stocker l'expression
        self.expression = ""
        # Variable pour suivre si le résultat est affiché
        self.resultat_affiche = False
        
        # Création du champ d'affichage
        self.affichage_var = tk.StringVar()
        self.affichage_var.set("0")
        
        # Création des widgets
        self.creer_widgets()
        
    def creer_widgets(self):
        # Style pour les boutons
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 14), padding=10)
        style.configure("Nombre.TButton", background="#ffffff")
        style.configure("Operation.TButton", background="#f0ad4e")
        style.configure("Egal.TButton", background="#5cb85c")
        style.configure("Effacer.TButton", background="#d9534f")
        
        # Frame pour l'affichage
        frame_affichage = tk.Frame(self.master, bg="#f0f0f0", height=100)
        frame_affichage.pack(fill=tk.BOTH, pady=10)
        
        # Affichage de l'expression
        self.affichage = tk.Entry(frame_affichage, font=("Arial", 24), 
                                textvariable=self.affichage_var, 
                                justify="right", bd=5, relief=tk.RIDGE)
        self.affichage.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)
        self.affichage.config(state="readonly")
        
        # Frame pour les boutons
        frame_boutons = tk.Frame(self.master, bg="#f0f0f0")
        frame_boutons.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Configuration des lignes et colonnes
        for i in range(5):
            frame_boutons.rowconfigure(i, weight=1)
        for i in range(4):
            frame_boutons.columnconfigure(i, weight=1)
        
        # Définition des boutons
        boutons = [
            ("C", 0, 0, 1, 1, self.effacer, "Effacer.TButton"),
            ("⌫", 0, 1, 1, 1, self.supprimer_dernier, "Effacer.TButton"),
            ("%", 0, 2, 1, 1, lambda: self.ajouter_a_expression("%"), "Operation.TButton"),
            ("÷", 0, 3, 1, 1, lambda: self.ajouter_a_expression("/"), "Operation.TButton"),
            
            ("7", 1, 0, 1, 1, lambda: self.ajouter_a_expression("7"), "Nombre.TButton"), 
            ("8", 1, 1, 1, 1, lambda: self.ajouter_a_expression("8"), "Nombre.TButton"),
            ("9", 1, 2, 1, 1, lambda: self.ajouter_a_expression("9"), "Nombre.TButton"),
            ("×", 1, 3, 1, 1, lambda: self.ajouter_a_expression("*"), "Operation.TButton"),
            
            ("4", 2, 0, 1, 1, lambda: self.ajouter_a_expression("4"), "Nombre.TButton"),
            ("5", 2, 1, 1, 1, lambda: self.ajouter_a_expression("5"), "Nombre.TButton"),
            ("6", 2, 2, 1, 1, lambda: self.ajouter_a_expression("6"), "Nombre.TButton"),
            ("-", 2, 3, 1, 1, lambda: self.ajouter_a_expression("-"), "Operation.TButton"),
            
            ("1", 3, 0, 1, 1, lambda: self.ajouter_a_expression("1"), "Nombre.TButton"),
            ("2", 3, 1, 1, 1, lambda: self.ajouter_a_expression("2"), "Nombre.TButton"),
            ("3", 3, 2, 1, 1, lambda: self.ajouter_a_expression("3"), "Nombre.TButton"),
            ("+", 3, 3, 1, 1, lambda: self.ajouter_a_expression("+"), "Operation.TButton"),
            
            ("0", 4, 0, 1, 2, lambda: self.ajouter_a_expression("0"), "Nombre.TButton"),
            (".", 4, 2, 1, 1, lambda: self.ajouter_a_expression("."), "Nombre.TButton"),
            ("=", 4, 3, 1, 1, self.calculer, "Egal.TButton")
        ]
        
        # Création des boutons
        for (texte, ligne, colonne, rangee, colonnee, commande, style_nom) in boutons:
            bouton = ttk.Button(frame_boutons, text=texte, command=commande, style=style_nom)
            bouton.grid(row=ligne, column=colonne, rowspan=rangee, columnspan=colonnee, 
                      padx=5, pady=5, sticky="NSEW")
        
        # Ajout de bindings clavier
        self.master.bind("<Return>", lambda event: self.calculer())
        self.master.bind("<Key>", self.appui_clavier)
    
    def appui_clavier(self, event):
        key = event.char
        if key.isdigit() or key in "+-*/.()%":
            self.ajouter_a_expression(key)
        elif key == "\r":  # Enter/Return key
            self.calculer()
        elif key == "\x08":  # Backspace key
            self.supprimer_dernier()
        
    def ajouter_a_expression(self, valeur):
        # Si un résultat est affiché, réinitialiser l'expression
        if self.resultat_affiche:
            if valeur in "0123456789.":
                self.expression = ""
            self.resultat_affiche = False
        
        # Ajouter la valeur à l'expression
        self.expression += valeur
        self.affichage_var.set(self.expression)
    
    def effacer(self):
        self.expression = ""
        self.affichage_var.set("0")
        self.resultat_affiche = False
    
    def supprimer_dernier(self):
        if self.resultat_affiche:
            self.effacer()
        else:
            self.expression = self.expression[:-1]
            if not self.expression:
                self.affichage_var.set("0")
            else:
                self.affichage_var.set(self.expression)
    
    def calculer(self):
        try:
            # Vérifier que l'expression contient uniquement des caractères autorisés
            if not re.match(r'^[0-9+\-*/.()%\s]+$', self.expression):
                raise ValueError("Expression non valide")
            
            # Évaluer l'expression
            resultat = eval(self.expression)
            
            # Formater le résultat
            if isinstance(resultat, float):
                # Supprimer les zéros inutiles
                if resultat.is_integer():
                    self.affichage_var.set(str(int(resultat)))
                else:
                    # Limiter à 8 décimales max
                    self.affichage_var.set(f"{resultat:.8g}")
            else:
                self.affichage_var.set(str(resultat))
            
            self.expression = self.affichage_var.get()
            self.resultat_affiche = True
            
        except Exception as e:
            self.affichage_var.set("Erreur")
            self.expression = ""
            self.resultat_affiche = True

if __name__ == "__main__":
    root = tk.Tk()
    app = Calculatrice(root)
    root.mainloop()