import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os
from pygame import mixer

flag = True
class CardGame:
    def __init__(self, root):
        global delpoint
        self.root = root
        self.width = 900
        self.height = 500
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.resizable(False, False)

        self.deck = [(value, suit) for value in range(2, 11) for suit in ['clubs', 'diamonds', 'hearts', 'spades']] * 4
        random.shuffle(self.deck)
        self.deck1 = [(value1, suit1) for value1 in range(2, 11) for suit1 in ['clubs', 'diamonds', 'hearts', 'spades']] * 4
        random.shuffle(self.deck1)

        self.card_value = 0
        self.card_value1 = 0
        self.player_points = 0
        self.dealer_points = 0
        self.score = 100
        self.bet = 20
        delpoint = 0

        mixer.init()
        mixer.music.load("muzyka.wav")
        mixer.music.set_volume(0.1)
        mixer.music.play(-1)

        self.score_frame = tk.Frame(self.root, width=60, bg="white")
        self.score_frame.pack(side="left", fill="y")

        self.bet_frame = tk.Frame(self.root, width=60, bg="white")
        self.bet_frame.pack(side="right", fill="y")

        self.score_label = tk.Label(self.score_frame, text='Счет: {}'.format(self.score), font=("Arial", 24), bg="grey")
        self.score_label.pack(pady=20)

        self.bet_label = tk.Label(self.bet_frame, text='Ставка: {}'.format(self.bet), font=("Arial", 24), bg="grey")
        self.bet_label.pack(pady=20)

        self.middle_frame = tk.Frame(self.root, bg="red")
        self.middle_frame.pack(fill="both", expand=True)

        self.player_frame = tk.Frame(self.root, bg="green")
        self.player_frame.pack(fill="both", expand=True)

        self.diler_label = tk.Label(self.middle_frame, text='Дилер'.format(self.score), font=("Arial", 12), bg="red", fg="white")
        self.diler_label.pack(pady=10)

        self.player_label = tk.Label(self.player_frame, text='Игрок'.format(self.score), font=("Arial", 12), bg="green", fg="white")
        self.player_label.pack(pady=10)

        self.diler_area = tk.Frame(self.middle_frame, bg="red", height=int(self.height * 0.3))
        self.diler_area.pack(side="top", fill="both", expand=True)

        self.cards_area = tk.Frame(self.player_frame, bg="green", height=int(self.height*0.5))
        self.cards_area.pack(side="bottom", fill="both", expand=True)

        self.player_labels = []
        self.diler_labels = []

        self.root.bind("<Return>", self.hit)
        self.root.bind("<space>", self.stand)
        self.root.bind("<Escape>", self.exit_game)
        self.root.bind("<Shift-+>", self.raise_bet)
        self.root.bind("<Tab>", self.reset_game)

        # self.play_audio()
        self.start_game()
        self.zakr_card()
        delpoint = self.dealer_points
        self.start_game()

    def start_game(self):
        global x1, y1
        card_value1, card_suit1 = self.deck1.pop()
        self.card_value1 += card_value1
        img1_path = os.path.join('image/dealer', f'{card_value1} of {card_suit1}.png')
        img1 = Image.open(img1_path)
        img1 = img1.resize((90, 140), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img1)
        dilers_label = tk.Label(self.diler_area, image=photo)
        dilers_label.image = photo
        dilers_label.pack(side="left")
        x1, y1 = dilers_label.winfo_x(), dilers_label.winfo_y()
        self.diler_labels.append(dilers_label)
        self.dealer_points = self.card_value1

        card_value, card_suit = self.deck.pop()
        self.card_value += card_value
        img_path = os.path.join('image/player', f'{card_value} of {card_suit}.png')
        img = Image.open(img_path)
        img = img.resize((90, 140), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        card_label = tk.Label(self.cards_area, image=photo)
        card_label.image = photo
        card_label.pack(side="left")
        self.player_labels.append(card_label)
        self.player_points = self.card_value

        self.player_label["text"] = "Игрок: " + str(self.card_value)
        self.diler_label["text"] = "Дилер: " + str(self.dealer_points-delpoint)

    def zakr_card(self):
        global dilers1_label
        img2_path = "image/dealer/1.jpg"  # Укажите путь к вашему изображению
        img2 = Image.open(img2_path)
        img2 = img2.resize((90, 140), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img2)
        dilers1_label = tk.Label(self.diler_area, image=photo)
        dilers1_label.image = photo
        dilers1_label.place(x=x1, y=y1 + 31)

    def get_card(self, player=True):
        card_value, card_suit = self.deck.pop()
        self.card_value += card_value
        self.player_label["text"] = "Игрок: "+str(self.card_value)

        return card_value, card_suit

    def hit(self, event=None):
        card_value, card_suit = self.get_card()
        img_path = os.path.join('image/player', f'{card_value} of {card_suit}.png')
        img = Image.open(img_path)
        img = img.resize((90, 140), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        card_label = tk.Label(self.cards_area, image=photo)
        card_label.image = photo
        card_label.pack(side="left")
        self.player_labels.append(card_label)
        self.player_points = self.card_value
        if self.player_points > 21:
            dilers1_label.place(x=10000, y=10000)
            self.diler_label["text"] = "Дилер: " + str(self.dealer_points)
            winner = f"Перебор! Вы проиграли! Ваш счет уменьшен на: {self.bet}"
            messagebox.showinfo("Поражение", winner)
            self.score -= self.bet
            self.bet = 20
            self.remove_cards()
            if self.score <= 0:
                winner = "Вы проиграли. Игра начнется заново..."
                self.score = 100
                messagebox.showinfo("Поражение", winner)
            self.score_label["text"] = "Счет: " + str(self.score)
            self.bet_label["text"] = "Ставка: " + str(self.bet)
            self.root.unbind("<Return>")
            self.root.unbind("<space>")
            self.root.after(50, self.start_new_round)
            return

    def stand(self, event=None):
        if len(self.player_labels) > 0 and self.player_points <= 21:
            dilers1_label.place(x=10000, y=10000)
            self.diler_label["text"] = "Дилер: " + str(self.dealer_points)
            self.root.unbind("<Return>")
            self.root.unbind("<space>")
            self.root.after(100, self.dealer_turn)
            self.root.after(2000, self.check_game)

    def start_new_round(self):
        global delpoint
        delpoint = 0
        self.card_value = 0
        self.card_value1 = 0
        self.player_points = 0
        self.dealer_points = 0
        self.remove_cards()
        self.root.bind("<Return>", self.hit)
        self.root.bind("<space>", self.stand)
        self.start_game()
        self.zakr_card()
        delpoint = self.dealer_points
        self.start_game()

    def reset_game(self, event=None):
        self.score = 100
        self.score_label["text"] = "Счет: " + str(self.score)
        self.bet_label["text"] = "Ставка: " + str(self.bet)
        self.root.unbind("<Return>")
        self.root.unbind("<space>")
        self.root.after(50, self.start_new_round)
        self.remove_cards()

    def exit_game(self, event=None):
        root.destroy()

    def raise_bet(self, event=None):
        self.bet += 10
        self.bet_label["text"] = "Ставка: " + str(self.bet)

    def remove_cards(self):
        for label in self.player_labels:
            label.destroy()
        self.player_labels.clear()
        for label in self.diler_labels:
            label.destroy()
        self.diler_labels.clear()

    def check_game(self):
        player_diff = 21 - self.player_points if self.player_points <= 21 else float("inf")
        dealer_diff = 21 - self.dealer_points if self.dealer_points <= 21 else float("inf")

        if player_diff < dealer_diff:
            self.diler_label["text"] = "Дилер: " + str(self.dealer_points)
            winner = f"Поздравляю, вы выиграли! Ваш счет увеличился на: {self.bet}"
            self.score += self.bet
            self.bet = 20
            self.score_label["text"] = "Счет: " + str(self.score)
        elif dealer_diff < player_diff:
            self.diler_label["text"] = "Дилер: " + str(self.dealer_points)
            winner = f"Вы проиграли. Ваш счет уменьшился на: {self.bet}"
            self.score -= self.bet
            self.bet = 20
            self.score_label["text"] = "Счет: " + str(self.score)
            self.bet_label["text"] = "Ставка: " + str(self.bet)

        else:
            winner = "Ничья"

        if self.score <= 0:
            self.diler_label["text"] = "Дилер: " + str(self.dealer_points)
            winner = "Вы проиграли. Игра начнется заново..."
            self.score = 100
            self.bet = 20
            self.score_label["text"] = "Счет: " + str(self.score)
            self.bet_label["text"] = "Ставка: " + str(self.bet)

        messagebox.showinfo("Конец раунда", winner)
        self.root.after(50, self.start_new_round)
        self.remove_cards()

    def dealer_turn(self):
        while self.dealer_points < 17:
            card_value1, card_suit1 = self.deck1.pop()
            self.card_value1 += card_value1
            img1_path = os.path.join('image/dealer', f'{card_value1} of {card_suit1}.png')
            img1 = Image.open(img1_path)
            img1 = img1.resize((90, 140), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img1)
            dilers_label = tk.Label(self.diler_area, image=photo)
            dilers_label.image = photo
            dilers_label.pack(side="left")
            self.diler_labels.append(dilers_label)
            self.dealer_points = self.card_value1
            self.diler_label["text"] = "Дилер: " + str(self.dealer_points)

root = tk.Tk()
root.title("21 очко")
game = CardGame(root)
root.mainloop()