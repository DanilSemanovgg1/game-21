import tkinter as tk
import random

class CardGame:
    def __init__(self, root):
        self.root = root
        self.width = 700
        self.height = 500
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.resizable(False, False)

        self.deck = list(range(2, 12)) * 4 * 4
        random.shuffle(self.deck)

        self.card_value = 0
        self.player_points = 0
        self.dealer_points = 0
        self.score = 50
        self.bet = 10

        self.score_frame = tk.Frame(self.root, width=50, bg="grey")
        self.score_frame.pack(side="left", fill="y")

        self.bet_frame = tk.Frame(self.root, width=50, bg="grey")
        self.bet_frame.pack(side="right", fill="y")

        self.score_label = tk.Label(self.score_frame, text='Счет: {}'.format(self.score), font=("Arial", 24), bg="grey")
        self.score_label.pack(pady=20)

        self.bet_label = tk.Label(self.bet_frame, text='Ставка: {}'.format(self.bet), font=("Arial", 24), bg="grey")
        self.bet_label.pack(pady=20)

        self.middle_frame = tk.Frame(self.root, bg="red")
        self.middle_frame.pack(fill="both", expand=True)

        self.result_label = tk.Label(self.middle_frame, text='', font=("Arial", 20), bg="red")
        self.result_label.pack(pady=20)

        self.cards_area = tk.Frame(self.middle_frame, bg="green", height=int(self.height*0.35))
        self.cards_area.pack(side="left", fill="both", expand=True)

        self.player_labels = []

        self.root.bind("<Return>", self.hit)
        self.root.bind("<space>", self.stand)
        self.root.bind("<Escape>", self.pause_game)
        self.root.bind("<Shift-+>", self.raise_bet)

    def get_card(self, player=True):
        card = self.deck.pop()
        if player:
            self.card_value += card
        else:
            self.dealer_points += card
        return card

    def hit(self, event=None):
        self.result_label["text"] = ""
        card = self.get_card()
        card_label = tk.Label(self.cards_area, text=str(card), font=("Arial", 24), bg="white")
        card_label.pack(side="left")
        self.player_labels.append(card_label)
        self.player_points = self.card_value
        if self.player_points > 21:
            self.result_label["text"] = "Перебор! Вы проиграли"
            self.score -= self.bet
            self.bet = 10
            self.root.after(1000, self.start_new_round)

    def stand(self, event=None):
        if len(self.player_labels) > 0 and self.player_points <= 21:
            self.root.unbind("<Return>")
            self.root.unbind("<space>")
            self.check_game()

    def start_new_round(self):
        self.card_value = 0
        self.player_points = 0
        self.dealer_points = 0
        self.remove_cards()
        self.root.bind("<Return>", self.hit)
        self.root.bind("<space>", self.stand)

    def pause_game(self, event=None):
        pass  # Here you could implement the logic for the Pause functionality.

    def raise_bet(self, event=None):
        self.bet += 10
        self.bet_label["text"] = "Ставка: " + str(self.bet)

    def remove_cards(self):
        for label in self.player_labels:
            label.destroy()
        self.player_labels.clear()

    def check_game(self):
        self.dealer_turn()
        player_diff = 21 - self.player_points if self.player_points <= 21 else float("inf")
        dealer_diff = 21 - self.dealer_points if self.dealer_points <= 21 else float("inf")

        if player_diff < dealer_diff:
            winner = "Игрок выиграл!"
            self.score += self.bet
            self.bet = 10
        elif dealer_diff < player_diff:
            winner = "Дилер выиграл!"
            self.score -= self.bet
            self.bet = 10
        else:
            winner = "Ничья!"
        self.score_label["text"] = "Счет: " + str(self.score)
        self.result_label["text"] = winner
        self.bet = 10
        self.root.after(2000, self.start_new_round)

    def dealer_turn(self):
        while self.dealer_points <= 16:
            self.get_card(False)


root = tk.Tk()
game = CardGame(root)
root.mainloop()