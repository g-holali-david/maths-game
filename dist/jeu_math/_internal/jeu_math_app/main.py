import random
import time
import tkinter as tk
from tkinter import ttk, colorchooser, messagebox
import json
import os
import sqlite3

CONFIG_FILE = 'config.json'
SCORES_FILE = 'scores.json'
DB_FILE = 'jeu_math.db'
DEFAULT_CONFIG = {
    "nom_joueur": "",
    "nb_questions": 10,
    "temps_de_reponse": 5,
    "bg_color": "#2c3e50",
    "fg_color": "white",
    "progress_color": "#3498db"
}

class JeuMath:
    def __init__(self, root):
        self.root = root
        self.root.title("Jeu de Questions Mathématiques")
        self.load_config()
        self.root.configure(bg=self.config["bg_color"])

        # Agrandir la fenêtre au démarrage
        self.root.geometry("800x600")

        self.temps_de_reponse = self.config["temps_de_reponse"]
        self.points = 0
        self.nb_questions = self.config["nb_questions"]
        self.current_question = 0
        self.nom_joueur = self.config["nom_joueur"]
        self.resultats = []
        self.score_precedent = self.load_scores()

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TButton", font=("Helvetica", 14), padding=10, background=self.config["bg_color"], foreground=self.config["fg_color"])
        self.style.map("TButton",
                       foreground=[('active', 'white'), ('disabled', 'grey')],
                       background=[('active', '#1a5276'), ('disabled', self.config["bg_color"])])
        self.style.configure("TLabel", font=("Helvetica", 16), background=self.config["bg_color"], foreground=self.config["fg_color"])
        self.style.configure("TFrame", background=self.config["bg_color"])
        self.style.configure("TEntry", font=("Helvetica", 14), padding=5)
        self.style.configure("TProgressbar", thickness=20, troughcolor=self.config["bg_color"], background=self.config["progress_color"])

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
        self.entry_nom.insert(0, self.nom_joueur)
        self.label_nb_questions = ttk.Label(self.frame_nom_nb_questions, text="Nombre de questions :", style="TLabel")
        self.label_nb_questions.pack(pady=5)
        self.entry_nb_questions = ttk.Entry(self.frame_nom_nb_questions, style="TEntry")
        self.entry_nb_questions.pack(pady=5)
        self.entry_nb_questions.insert(0, str(self.nb_questions))
        self.button_valider_nom_nb = ttk.Button(self.frame_nom_nb_questions, text="Valider", command=self.commencer_jeu, style="TButton")
        self.button_valider_nom_nb.pack(pady=20)

        self.frame_nb_questions = ttk.Frame(root, style="TFrame")
        self.label_nb_questions_recommencer = ttk.Label(self.frame_nb_questions, text="Nombre de questions :", style="TLabel")
        self.label_nb_questions_recommencer.pack(pady=5)
        self.entry_nb_questions_recommencer = ttk.Entry(self.frame_nb_questions, style="TEntry")
        self.entry_nb_questions_recommencer.pack(pady=5)
        self.entry_nb_questions_recommencer.insert(0, str(self.nb_questions))
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

        # Initialiser la base de données
        self.init_db()

    def creer_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        menu_cascade = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Menu", menu=menu_cascade)
        menu_cascade.add_command(label="Commencer", command=self.afficher_page_nom_nb_questions)
        menu_cascade.add_command(label="Recommencer", command=self.afficher_page_nb_questions)
        menu_cascade.add_command(label="Historique", command=self.afficher_historique)
        menu_cascade.add_command(label="Statistiques", command=self.afficher_statistiques)
        menu_cascade.add_command(label="Classement", command=self.afficher_classement)
        menu_cascade.add_separator()
        menu_cascade.add_command(label="Paramètres", command=self.ouvrir_parametres)
        menu_cascade.add_command(label="Réinitialiser les paramètres", command=self.reinitialiser_parametres)
        menu_cascade.add_separator()
        menu_cascade.add_command(label="Quitter", command=self.root.destroy)

    def ouvrir_parametres(self):
        parametres_window = tk.Toplevel(self.root)
        parametres_window.title("Paramètres")
        parametres_window.geometry("400x400")
        parametres_window.configure(bg=self.config["bg_color"])

        canvas = tk.Canvas(parametres_window)
        scroll_y = tk.Scrollbar(parametres_window, orient="vertical", command=canvas.yview)
        
        scrollable_frame = ttk.Frame(canvas, style="TFrame")
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scroll_y.set)

        label_bg = ttk.Label(scrollable_frame, text="Couleur de fond :", style="TLabel")
        label_bg.pack(pady=10)
        button_bg = ttk.Button(scrollable_frame, text="Choisir couleur", command=self.choisir_couleur_fond, style="TButton")
        button_bg.pack(pady=10)

        label_fg = ttk.Label(scrollable_frame, text="Couleur du texte :", style="TLabel")
        label_fg.pack(pady=10)
        button_fg = ttk.Button(scrollable_frame, text="Choisir couleur", command=self.choisir_couleur_texte, style="TButton")
        button_fg.pack(pady=10)

        label_progress = ttk.Label(scrollable_frame, text="Couleur de la barre de progression :", style="TLabel")
        label_progress.pack(pady=10)
        button_progress = ttk.Button(scrollable_frame, text="Choisir couleur", command=self.choisir_couleur_progress, style="TButton")
        button_progress.pack(pady=10)

        label_temps = ttk.Label(scrollable_frame, text="Temps de réponse (secondes) :", style="TLabel")
        label_temps.pack(pady=10)
        self.entry_temps = ttk.Entry(scrollable_frame, style="TEntry")
        self.entry_temps.pack(pady=10)
        self.entry_temps.insert(0, str(self.config["temps_de_reponse"]))

        button_save = ttk.Button(scrollable_frame, text="Sauvegarder", command=self.sauvegarder_parametres, style="TButton")
        button_save.pack(pady=20)

        canvas.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")

    def choisir_couleur_fond(self):
        couleur = colorchooser.askcolor()[1]
        if couleur:
            self.config["bg_color"] = couleur
            self.root.configure(bg=couleur)
            self.style.configure("TFrame", background=couleur)
            self.style.configure("TLabel", background=couleur)
            self.style.configure("TProgressbar", troughcolor=couleur)
            self.update_all_widgets()
            self.save_config()

    def choisir_couleur_texte(self):
        couleur = colorchooser.askcolor()[1]
        if couleur:
            self.config["fg_color"] = couleur
            self.style.configure("TLabel", foreground=couleur)
            self.style.configure("TButton", foreground=couleur)
            self.update_all_widgets()
            self.save_config()

    def choisir_couleur_progress(self):
        couleur = colorchooser.askcolor()[1]
        if couleur:
            self.config["progress_color"] = couleur
            self.style.configure("TProgressbar", background=couleur)
            self.update_all_widgets()
            self.save_config()

    def update_all_widgets(self):
        for widget in self.root.winfo_children():
            widget.update()

    def afficher_page_nom_nb_questions(self):
        self.frame_main.pack_forget()
        self.frame_nb_questions.pack_forget()
        self.frame_nom_nb_questions.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        self.entry_nom.delete(0, tk.END)  # Réinitialiser le champ de saisie du nom
        self.entry_nb_questions.delete(0, tk.END)  # Réinitialiser le champ de saisie du nombre de questions

    def afficher_page_nb_questions(self):
        self.frame_question.pack_forget()
        self.frame_resultats.pack_forget()
        self.frame_nb_questions.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        self.entry_nb_questions_recommencer.delete(0, tk.END)  # Réinitialiser le champ de saisie du nombre de questions à recommencer

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
        self.config["nom_joueur"] = self.nom_joueur
        self.config["nb_questions"] = self.nb_questions
        self.points = 0
        self.resultats = []
        self.current_question = 0
        self.label_nom_joueur.config(text=f"Joueur: {self.nom_joueur}")
        self.progress["maximum"] = self.nb_questions
        self.progress["value"] = 0

        self.frame_nom_nb_questions.pack_forget()
        self.frame_question.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        self.save_config()
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
        self.config["nb_questions"] = self.nb_questions
        self.points = 0
        self.resultats = []
        self.current_question = 0
        self.progress["maximum"] = self.nb_questions
        self.progress["value"] = 0

        self.frame_nb_questions.pack_forget()
        self.frame_question.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        self.save_config()
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
        if self.current_question > self.nb_questions:
            return

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
        if self.current_question > self.nb_questions:
            return

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

        # Affichage de l'amélioration
        if self.nom_joueur in self.score_precedent:
            score_prec = self.score_precedent[self.nom_joueur]
            if self.points > score_prec:
                message_ameliore = f"Bravo {self.nom_joueur}, vous vous êtes amélioré par rapport à votre score précédent de {score_prec} points!"
            elif self.points < score_prec:
                message_ameliore = f"Continuez à pratiquer {self.nom_joueur}, votre score précédent était de {score_prec} points."
            else:
                message_ameliore = f"Vous avez égalé votre score précédent de {score_prec} points."
        else:
            message_ameliore = f"C'est votre première partie, continuez à vous améliorer {self.nom_joueur}!"

        label_ameliore = ttk.Label(self.frame_resultats, text=message_ameliore, style="TLabel")
        label_ameliore.pack(pady=20)

        # Conteneur pour le score et le tableau des résultats
        frame_score_tableau = ttk.Frame(self.frame_resultats, style="TFrame")
        frame_score_tableau.pack(pady=20, fill=tk.BOTH, expand=True)

        # Canvas pour le cercle du score
        canvas_score = tk.Canvas(frame_score_tableau, width=100, height=100, bg=self.config["bg_color"], highlightthickness=0)
        canvas_score.grid(row=0, column=0, padx=10, pady=10)

        # Dessiner le cercle et le score
        canvas_score.create_oval(10, 10, 90, 90, fill=self.config["progress_color"], outline="")
        canvas_score.create_text(50, 50, text=str(self.points), fill="white", font=("Helvetica", 24, "bold"))

        # Création du tableau de résultats
        self.tree = ttk.Treeview(frame_score_tableau, columns=("Question", "Réponse", "État", "Temps"), show="headings")
        self.tree.heading("Question", text="Question")
        self.tree.heading("Réponse", text="Réponse")
        self.tree.heading("État", text="État")
        self.tree.heading("Temps", text="Temps")
        self.tree.grid(row=0, column=1, sticky='nsew')

        frame_score_tableau.columnconfigure(1, weight=1)
        frame_score_tableau.rowconfigure(0, weight=1)

        for resultat in self.resultats:
            self.tree.insert("", "end", values=resultat)

        self.button_restart = ttk.Button(self.frame_resultats, text="Recommencer", command=self.recommencer_jeu, style="TButton")
        self.button_restart.pack(pady=20)

        self.save_scores()
        self.save_to_db()

    def init_db(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS resultats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom_joueur TEXT,
                question TEXT,
                reponse TEXT,
                etat TEXT,
                temps REAL
            )
        ''')
        self.conn.commit()

    def save_to_db(self):
        for resultat in self.resultats:
            self.cursor.execute('''
                INSERT INTO resultats (nom_joueur, question, reponse, etat, temps)
                VALUES (?, ?, ?, ?, ?)
            ''', (self.nom_joueur, resultat[0], str(resultat[1]), resultat[2], resultat[3]))
        self.conn.commit()

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = DEFAULT_CONFIG

    def save_config(self):
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.config, f, indent=4)

    def load_scores(self):
        if os.path.exists(SCORES_FILE):
            with open(SCORES_FILE, 'r') as f:
                return json.load(f)
        else:
            return {}

    def save_scores(self):
        self.score_precedent[self.nom_joueur] = self.points
        with open(SCORES_FILE, 'w') as f:
            json.dump(self.score_precedent, f, indent=4)

    def afficher_historique(self):
        historique_window = tk.Toplevel(self.root)
        historique_window.title("Historique des Jeux")
        historique_window.geometry("600x400")
        historique_window.configure(bg=self.config["bg_color"])

        historique_tree = ttk.Treeview(historique_window, columns=("ID", "Nom", "Question", "Réponse", "État", "Temps"), show="headings")
        historique_tree.heading("ID", text="ID")
        historique_tree.heading("Nom", text="Nom du joueur")
        historique_tree.heading("Question", text="Question")
        historique_tree.heading("Réponse", text="Réponse")
        historique_tree.heading("État", text="État")
        historique_tree.heading("Temps", text="Temps")
        historique_tree.pack(fill=tk.BOTH, expand=True)

        self.cursor.execute("SELECT * FROM resultats WHERE nom_joueur = ?", (self.nom_joueur,))
        rows = self.cursor.fetchall()
        for row in rows:
            historique_tree.insert("", "end", values=row)

    def afficher_statistiques(self):
        statistiques_window = tk.Toplevel(self.root)
        statistiques_window.title("Statistiques des Jeux")
        statistiques_window.geometry("400x300")
        statistiques_window.configure(bg=self.config["bg_color"])

        self.cursor.execute("SELECT COUNT(*), AVG(temps) FROM resultats WHERE nom_joueur = ?", (self.nom_joueur,))
        stats = self.cursor.fetchone()
        nb_jeux = stats[0]
        temps_moyen = stats[1]

        label_nb_jeux = ttk.Label(statistiques_window, text=f"Nombre de jeux joués : {nb_jeux}", style="TLabel")
        label_nb_jeux.pack(pady=10)
        label_temps_moyen = ttk.Label(statistiques_window, text=f"Temps moyen par question : {temps_moyen:.2f} secondes", style="TLabel")
        label_temps_moyen.pack(pady=10)

    def afficher_classement(self):
        classement_window = tk.Toplevel(self.root)
        classement_window.title("Classement des Joueurs")
        classement_window.geometry("600x400")
        classement_window.configure(bg=self.config["bg_color"])

        classement_tree = ttk.Treeview(classement_window, columns=("Nom", "Score Total"), show="headings")
        classement_tree.heading("Nom", text="Nom du joueur")
        classement_tree.heading("Score Total", text="Score Total")
        classement_tree.pack(fill=tk.BOTH, expand=True)

        self.cursor.execute("SELECT nom_joueur, SUM(CASE WHEN etat = 'Correct' THEN 1 ELSE 0 END) as score FROM resultats GROUP BY nom_joueur ORDER BY score DESC")
        rows = self.cursor.fetchall()
        for row in rows:
            classement_tree.insert("", "end", values=row)

    def sauvegarder_parametres(self):
        try:
            self.config["temps_de_reponse"] = int(self.entry_temps.get())
        except ValueError:
            messagebox.showerror("Erreur", "Le temps de réponse doit être un nombre entier.")
            return

        self.save_config()
        messagebox.showinfo("Paramètres", "Les paramètres ont été sauvegardés avec succès.")
        self.root.destroy()
        self.__init__(tk.Tk())

    def reinitialiser_parametres(self):
        self.config = DEFAULT_CONFIG
        self.save_config()
        messagebox.showinfo("Réinitialisation", "Les paramètres ont été réinitialisés aux valeurs par défaut.")
        self.root.destroy()
        self.__init__(tk.Tk())

if __name__ == "__main__":
    root = tk.Tk()
    jeu = JeuMath(root)
    root.mainloop()
