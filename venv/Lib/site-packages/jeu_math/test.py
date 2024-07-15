import random
import time
import threading
import sys

def afficher_temps(temps_de_reponse, stop_event):
    for i in range(temps_de_reponse):
        if stop_event.is_set():
            break
        print(f"\rTemps restant: {temps_de_reponse - i} secondes", end="")
        time.sleep(1)
    if not stop_event.is_set():
        print("\rTemps écoulé !              ")

def jeu():
    
    print()
    continuer = True
    temps_de_reponse = 5
    
    print("...............................................")
    print("Bienvenue dans le jeu de questions mathématiques.")
    print("...............................................")
    
    print()

    while continuer:
        points = 0
        nb = int(input("Combien de questions voulez-vous ? : "))
        
        for q in range(1, nb + 1):
            print()
            operateurs = ["+", "-", "*", "//"]
            a = random.randint(1, 10)
            b = random.randint(1, 10)
            operateur = random.choice(operateurs)
            
            if operateur == "//" and b == 0:
                b = random.randint(1, 10)
            
            if operateur == "//":
                a, b = b, a
            
            stop_event = threading.Event()
            print(f"Vous avez {temps_de_reponse} secondes pour répondre.")
            thread = threading.Thread(target=afficher_temps, args=(temps_de_reponse, stop_event))
            thread.start()
            
            debut = time.time()
            try:
                reponse = input(f"\r{b} {operateur} {a} donne : ")
                fin = time.time()

                if fin - debut > temps_de_reponse:
                    print("Temps écoulé ! Réponse non prise en compte.")
                    stop_event.set()
                    thread.join()
                    continue  # Passer à la question suivante

                stop_event.set()
                thread.join()  # Assurer que l'animation est terminée avant de continuer

                reponse = int(reponse)
                if reponse == eval(f"{b} {operateur} {a}"):
                    print("Réponse correcte !")
                    points += 1
                else: 
                    print("Réponse incorrecte !")
                    
            except (ZeroDivisionError, ValueError):
                print("Erreur dans la réponse ou division par zéro !")
                print()
            
            except TimeoutError:
                print("Temps écoulé ! Réponse non prise en compte.")
                
        print(f"Vous avez gagné {points} points.")
        
        print()
        continuer = input("Voulez-vous continuer ? (y/n) : ").lower() == "y"
        
        if not continuer:
            print("Au revoir !")

