import tkinter as tk
from tkinter import ttk, colorchooser
import random
import time

class JeuMath:
    def __init__(self, root):
        self.root = root
        self.root.title("Jeu de Questions Mathématiques")
        self.root.geometry("600x400")
        self.default_bg_color = "#2c3e50"
        self.default_fg_color = "white"
        self.default_progress_color = "#3498db"
        self.root.configure(bg=self.default_bg_color)

        self.temps_de_reponse = 5
        self.points = 0
        self.nb_questions = 0
        self.current_question = 0
        self.nom_joueur = ""
        self.resultats = []

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TButton", font=("Helvetica", 14), padding=10, background=self.default_bg_color, foreground=self.default_fg_color)
        self.style.map("TButton",
                       foreground=[('active', 'white'), ('disabled', 'grey')],
                       background=[('active', '#1a5276'), ('disabled', self.default_bg_color)])
        self.style.configure("TLabel", font=("Helvetica", 16), background=self.default_bg_color, foreground=self.default_fg_color)
        self.style.configure("TFrame", background=self.default_bg_color)
        self.style.configure("TEntry", font=("Helvetica", 14), padding=5)
        self.style.configure("TProgressbar", thickness=20, troughcolor=self.default_bg_color, background=self.default_progress_color)

        self.frame_main = ttk.Frame(root, style="TFrame")
        self.frame_main.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        self.label_title = ttk.Label(self.frame_main, text="Jeu de Questions Mathématiques", style="TLabel", font=("Helvetica", 24, "bold"))
        self.label_title.pack(pady=20)

        self.button_start = ttk.Button(self.frame_main, text="Commencer", command=self.afficher_page_nom_nb_questions, style="TButton")
        self.button_start.pack(pady=20)

        self.frame_nom_nb_questions = ttk.Frame(root, style="TFrame")
        self.label_nom = ttk.Label(self.frame_nom_nb_questions, text="Nom du joueur :", style="TLabel")
        self.label_nom.pack(pady=5)
        self.entry_nom = ttk.Entry(self.frame_nom_nb_questions, style="TEntry")
        self.entry_nom.pack(pady=5)
        self.label_nb_questions = ttk.Label(self.frame_nom_nb_questions, text="Nombre de questions :", style="TLabel")
        self.label_nb_questions.pack(pady=5)
        self.entry_nb_questions = ttk.Entry(self.frame_nom_nb_questions, style="TEntry")
        self.entry_nb_questions.pack(pady=5)
        self.button_valider_nom_nb = ttk.Button(self.frame_nom_nb_questions, text="Valider", command=self.commencer_jeu, style="TButton")
        self.button_valider_nom_nb.pack(pady=20)

        self.frame_nb_questions = ttk.Frame(root, style="TFrame")
        self.label_nb_questions_recommencer = ttk.Label(self.frame_nb_questions, text="Nombre de questions :", style="TLabel")
        self.label_nb_questions_recommencer.pack(pady=5)
        self.entry_nb_questions_recommencer = ttk.Entry(self.frame_nb_questions, style="TEntry")
        self.entry_nb_questions_recommencer.pack(pady=5)
        self.button_valider_nb = ttk.Button(self.frame_nb_questions, text="Valider", command=self.valider_nb_questions_recommencer, style="TButton")
        self.button_valider_nb.pack(pady=20)

        self.frame_question = ttk.Frame(root, style="TFrame")
        self.label_nom_joueur = ttk.Label(self.frame_question, text="", style="TLabel")
        self.label_nom_joueur.pack(pady=10)
        self.label_question = ttk.Label(self.frame_question, text="", style="TLabel")
        self.label_question.pack(pady=10)
        self.entry_reponse = ttk.Entry(self.frame_question, style="TEntry")
        self.entry_reponse.pack(pady=10)
        self.entry_reponse.bind("<Return>", self.check_reponse)
        self.button_reponse = ttk.Button(self.frame_question, text="Répondre", command=self.check_reponse, style="TButton")
        self.button_reponse.pack(pady=10)
        self.label_temps = ttk.Label(self.frame_question, text="", style="TLabel")
        self.label_temps.pack(pady=10)
        self.label_resultat = ttk.Label(self.frame_question, text="", style="TLabel")
        self.label_resultat.pack(pady=10)
        self.progress = ttk.Progressbar(self.frame_question, orient="horizontal", length=300, mode="determinate", style="TProgressbar")
        self.progress.pack(pady=10)

        self.frame_resultats = ttk.Frame(root, style="TFrame")

        self.creer_menu()

    def creer_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        menu_cascade = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Menu", menu=menu_cascade)
        menu_cascade.add_command(label="Commencer", command=self.afficher_page_nom_nb_questions)
        menu_cascade.add_command(label="Recommencer", command=self.afficher_page_nb_questions)
        menu_cascade.add_separator()
        menu_cascade.add_command(label="Paramètres", command=self.ouvrir_parametres)
        menu_cascade.add_separator()
        menu_cascade.add_command(label="Quitter", command=self.root.destroy)

    def ouvrir_parametres(self):
        parametres_window = tk.Toplevel(self.root)
        parametres_window.title("Paramètres")
        parametres_window.geometry("400x300")
        parametres_window.configure(bg=self.default_bg_color)

        label_bg = ttk.Label(parametres_window, text="Couleur de fond :", style="TLabel")
        label_bg.pack(pady=10)
        button_bg = ttk.Button(parametres_window, text="Choisir couleur", command=self.choisir_couleur_fond, style="TButton")
        button_bg.pack(pady=10)

        label_fg = ttk.Label(parametres_window, text="Couleur du texte :", style="TLabel")
        label_fg.pack(pady=10)
        button_fg = ttk.Button(parametres_window, text="Choisir couleur", command=self.choisir_couleur_texte, style="TButton")
        button_fg.pack(pady=10)

        label_progress = ttk.Label(parametres_window, text="Couleur de la barre de progression :", style="TLabel")
        label_progress.pack(pady=10)
        button_progress = ttk.Button(parametres_window, text="Choisir couleur", command=self.choisir_couleur_progress, style="TButton")
        button_progress.pack(pady=10)

    def choisir_couleur_fond(self):
        couleur = colorchooser.askcolor()[1]
        if couleur:
            self.default_bg_color = couleur
            self.root.configure(bg=couleur)
            self.style.configure("TFrame", background=couleur)
            self.style.configure("TLabel", background=couleur)
            self.style.configure("TProgressbar", troughcolor=couleur)
            self.update_all_widgets()

    def choisir_couleur_texte(self):
        couleur = colorchooser.askcolor()[1]
        if couleur:
            self.default_fg_color = couleur
            self.style.configure("TLabel", foreground=couleur)
            self.style.configure("TButton", foreground=couleur)
            self.update_all_widgets()

    def choisir_couleur_progress(self):
        couleur = colorchooser.askcolor()[1]
        if couleur:
            self.default_progress_color = couleur
            self.style.configure("TProgressbar", background=couleur)
            self.update_all_widgets()

    def update_all_widgets(self):
        for widget in self.root.winfo_children():
            widget.update()

    def afficher_page_nom_nb_questions(self):
        self.frame_main.pack_forget()
        self.frame_nb_questions.pack_forget()
        self.frame_nom_nb_questions.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

    def afficher_page_nb_questions(self):
        self.frame_question.pack_forget()
        self.frame_resultats.pack_forget()
        self.frame_nb_questions.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

    def commencer_jeu(self):
        self.nom_joueur = self.entry_nom.get().strip()
        if not self.nom_joueur:
            self.entry_nom.focus_set()
            return
        
        nb_questions_str = self.entry_nb_questions.get().strip()
        if not nb_questions_str or not nb_questions_str.isdigit():
            self.entry_nb_questions.focus_set()
            return
        
        self.nb_questions = int(nb_questions_str)
        self.points = 0
        self.resultats = []
        self.current_question = 0
        self.label_nom_joueur.config(text=f"Joueur: {self.nom_joueur}")
        self.progress["maximum"] = self.nb_questions
        self.progress["value"] = 0

        self.frame_nom_nb_questions.pack_forget()
        self.frame_question.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        self.nouvelle_question()

    def recommencer_jeu(self):
        self.points = 0
        self.resultats = []
        self.current_question = 0
        self.progress["value"] = 0
        self.afficher_page_nb_questions()

    def valider_nb_questions_recommencer(self):
        nb_questions_str = self.entry_nb_questions_recommencer.get().strip()
        if not nb_questions_str or not nb_questions_str.isdigit():
            self.entry_nb_questions_recommencer.focus_set()
            return

        self.nb_questions = int(nb_questions_str)
        self.points = 0
        self.resultats = []
        self.current_question = 0
        self.progress["maximum"] = self.nb_questions
        self.progress["value"] = 0

        self.frame_nb_questions.pack_forget()
        self.frame_question.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        self.nouvelle_question()

    def nouvelle_question(self):
        if self.current_question < self.nb_questions:
            self.current_question += 1
            operateurs = ["+", "-", "*", "//"]
            a = random.randint(1, 10)
            b = random.randint(1, 10)
            self.operateur = random.choice(operateurs)
            
            if self.operateur == "//" and b == 0:
                b = random.randint(1, 10)
            
            if self.operateur == "//":
                a, b = b, a
            
            self.question = f"{b} {self.operateur} {a}"
            self.label_question.config(text=f"Question {self.current_question}: {self.question} = ?")
            self.entry_reponse.delete(0, tk.END)
            self.label_resultat.config(text="")
            self.start_time = time.time()
            self.update_timer()
            self.button_reponse.config(state=tk.NORMAL)
        else:
            self.afficher_resultats()

    def check_reponse(self, event=None):
        temps_ecoule = time.time() - self.start_time
        correct = False

        try:
            reponse = int(self.entry_reponse.get())
            if temps_ecoule > self.temps_de_reponse:
                self.label_resultat.config(text="Temps écoulé ! Réponse non prise en compte.")
            elif reponse == eval(self.question.replace("//", "/")):
                self.label_resultat.config(text="Réponse correcte !")
                self.points += 1
                correct = True
            else:
                self.label_resultat.config(text="Réponse incorrecte !")
        except (ZeroDivisionError, ValueError):
            self.label_resultat.config(text="Erreur dans la réponse ou division par zéro !")
            reponse = "Erreur"
        
        self.resultats.append((self.question, reponse, "Correct" if correct else "Incorrect", f"{temps_ecoule:.2f}s"))
        self.button_reponse.config(state=tk.DISABLED)
        self.progress["value"] = self.current_question
        self.root.after(1000, self.nouvelle_question)

    def update_timer(self):
        elapsed_time = int(time.time() - self.start_time)
        remaining_time = self.temps_de_reponse - elapsed_time
        if remaining_time > 0:
            self.label_temps.config(text=f"Temps restant: {remaining_time} secondes")
            self.root.after(1000, self.update_timer)
        else:
            self.label_temps.config(text="Temps écoulé !")
            self.check_reponse()

    def afficher_resultats(self):
        self.frame_question.pack_forget()
        self.frame_resultats.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        for widget in self.frame_resultats.winfo_children():
            widget.destroy()

        if self.points == self.nb_questions:
            message = f"Félicitations {self.nom_joueur} ! Vous avez répondu correctement à toutes les questions !"
        elif self.points > self.nb_questions / 2:
            message = f"Bien joué {self.nom_joueur} ! Vous avez obtenu {self.points} points sur {self.nb_questions}."
        else:
            message = f"Bonne tentative {self.nom_joueur} ! Vous avez obtenu {self.points} points sur {self.nb_questions}. Continuez à pratiquer !"

        label_points = ttk.Label(self.frame_resultats, text=message, style="TLabel")
        label_points.pack(pady=20)

        tree = ttk.Treeview(self.frame_resultats, columns=("Question", "Réponse", "État", "Temps"), show="headings")
        tree.heading("Question", text="Question")
        tree.heading("Réponse", text="Réponse")
        tree.heading("État", text="État")
        tree.heading("Temps", text="Temps")
        
        for resultat in self.resultats:
            tree.insert("", "end", values=resultat)
        
        tree.pack(expand=True, fill=tk.BOTH)

        self.button_restart = ttk.Button(self.frame_resultats, text="Recommencer", command=self.recommencer_jeu, style="TButton")
        self.button_restart.pack(pady=20)

