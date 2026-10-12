import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random
from enum import Enum
from typing import List, Optional
import math

class Color(Enum):
    RED = "#FF4444"
    YELLOW = "#FFDD44"
    GREEN = "#44FF44"
    BLUE = "#4444FF"
    WILD = "#444444"

class CardType(Enum):
    NUMBER = "Number"
    SKIP = "Skip"
    REVERSE = "Reverse"
    DRAW_TWO = "Draw Two"
    WILD = "Wild"
    WILD_DRAW_FOUR = "Wild Draw Four"

class Card:
    def __init__(self, color: Color, card_type: CardType, number: Optional[int] = None):
        self.color = color
        self.card_type = card_type
        self.number = number
        self.original_color = color  # Store original color for wild cards
    
    def __str__(self):
        if self.card_type == CardType.NUMBER:
            return f"{self.number}"
        elif self.card_type == CardType.WILD:
            return "W"
        elif self.card_type == CardType.WILD_DRAW_FOUR:
            return "W+4"
        elif self.card_type == CardType.SKIP:
            return "⊘"
        elif self.card_type == CardType.REVERSE:
            return "⟲"
        elif self.card_type == CardType.DRAW_TWO:
            return "+2"
        else:
            return "?"
    
    def can_play_on(self, other_card: 'Card') -> bool:
        if self.card_type in [CardType.WILD, CardType.WILD_DRAW_FOUR]:
            return True
        return (self.color == other_card.color or 
                self.card_type == other_card.card_type or 
                (self.card_type == CardType.NUMBER and 
                 other_card.card_type == CardType.NUMBER and 
                 self.number == other_card.number))

class Player:
    def __init__(self, name: str, is_human: bool = True):
        self.name = name
        self.hand = []
        self.is_human = is_human
    
    def add_card(self, card: Card):
        self.hand.append(card)
    
    def remove_card(self, card: Card):
        if card in self.hand:
            self.hand.remove(card)
    
    def get_playable_cards(self, top_card: Card) -> List[Card]:
        return [card for card in self.hand if card.can_play_on(top_card)]
    
    def has_uno(self) -> bool:
        return len(self.hand) == 1
    
    def has_won(self) -> bool:
        return len(self.hand) == 0

class Deck:
    def __init__(self):
        self.cards = []
        self._create_deck()
        self.shuffle()
    
    def _create_deck(self):
        # Create number cards (0-9)
        for color in [Color.RED, Color.YELLOW, Color.GREEN, Color.BLUE]:
            # One 0 card per color
            self.cards.append(Card(color, CardType.NUMBER, 0))
            # Two of each number 1-9 per color
            for num in range(1, 10):
                self.cards.append(Card(color, CardType.NUMBER, num))
                self.cards.append(Card(color, CardType.NUMBER, num))
            
            # Two of each action card per color
            for _ in range(2):
                self.cards.append(Card(color, CardType.SKIP))
                self.cards.append(Card(color, CardType.REVERSE))
                self.cards.append(Card(color, CardType.DRAW_TWO))
        
        # Four Wild cards and four Wild Draw Four cards
        for _ in range(4):
            self.cards.append(Card(Color.WILD, CardType.WILD))
            self.cards.append(Card(Color.WILD, CardType.WILD_DRAW_FOUR))
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def draw_card(self) -> Optional[Card]:
        return self.cards.pop() if self.cards else None
    
    def add_card(self, card: Card):
        self.cards.append(card)
    
    def is_empty(self) -> bool:
        return len(self.cards) == 0

class ColorChooserDialog:
    def __init__(self, parent):
        self.result = None
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Choose Color")
        self.dialog.geometry("300x200")
        self.dialog.resizable(False, False)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.transient(parent)
        
        tk.Label(self.dialog, text="Choose a color:", font=("Arial", 14)).pack(pady=20)
        
        button_frame = tk.Frame(self.dialog)
        button_frame.pack(pady=20)
        
        colors = [
            (Color.RED, "Red"),
            (Color.YELLOW, "Yellow"),
            (Color.GREEN, "Green"),
            (Color.BLUE, "Blue")
        ]
        
        for i, (color, name) in enumerate(colors):
            btn = tk.Button(button_frame, text=name, bg=color.value, fg="white",
                          font=("Arial", 12, "bold"), width=8, height=2,
                          command=lambda c=color: self.choose_color(c))
            btn.grid(row=i//2, column=i%2, padx=10, pady=5)
    
    def choose_color(self, color):
        self.result = color
        self.dialog.destroy()

class CardWidget(tk.Canvas):
    def __init__(self, parent, card: Card, width=60, height=90, clickable=True):
        super().__init__(parent, width=width, height=height, highlightthickness=1,
                        highlightbackground="gray", cursor="hand2" if clickable else "")
        self.card = card
        self.clickable = clickable
        self.selected = False
        self.draw_card()
        
        if clickable:
            self.bind("<Button-1>", self.on_click)
            self.bind("<Enter>", self.on_enter)
            self.bind("<Leave>", self.on_leave)
    
    def draw_card(self):
        self.delete("all")
        
        # Card background
        if self.card.color == Color.WILD:
            # Gradient effect for wild cards
            colors = ["#FF4444", "#FFDD44", "#44FF44", "#4444FF"]
            for i, color in enumerate(colors):
                self.create_rectangle(i*15, 0, (i+1)*15, 90, fill=color, outline="")
        else:
            self.create_rectangle(0, 0, 60, 90, fill=self.card.color.value, outline="black", width=2)
        
        # Card border highlight if selected
        if self.selected:
            self.create_rectangle(0, 0, 60, 90, outline="gold", width=3)
        
        # Card text
        text_color = "white" if self.card.color != Color.YELLOW else "black"
        self.create_text(30, 45, text=str(self.card), font=("Arial", 16, "bold"), 
                        fill=text_color)
    
    def on_click(self, event):
        if self.clickable:
            self.selected = not self.selected
            self.draw_card()
            self.event_generate("<<CardClicked>>")
    
    def on_enter(self, event):
        if self.clickable:
            self.configure(highlightbackground="gold", highlightthickness=2)
    
    def on_leave(self, event):
        if self.clickable:
            self.configure(highlightbackground="gray", highlightthickness=1)
    
    def set_selected(self, selected):
        self.selected = selected
        self.draw_card()

class UnoGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("UNO Game")
        self.root.geometry("1200x800")
        self.root.configure(bg="#2E8B57")
        
        self.game = None
        self.card_widgets = []
        self.selected_card = None
        
        self.setup_ui()
        self.show_start_screen()
    
    def setup_ui(self):
        # Main game frame
        self.game_frame = tk.Frame(self.root, bg="#2E8B57")
        
        # Top panel - opponents
        self.top_frame = tk.Frame(self.game_frame, bg="#2E8B57", height=150)
        self.top_frame.pack(fill="x", pady=10)
        
        # Center panel - game area
        self.center_frame = tk.Frame(self.game_frame, bg="#2E8B57", height=300)
        self.center_frame.pack(fill="x", pady=20)
        
        # Game info
        self.info_frame = tk.Frame(self.center_frame, bg="#2E8B57")
        self.info_frame.pack(side="left", padx=20)
        
        self.deck_canvas = tk.Canvas(self.info_frame, width=60, height=90, bg="#444444")
        self.deck_canvas.pack(pady=5)
        self.deck_canvas.create_text(30, 45, text="DECK", fill="white", font=("Arial", 8, "bold"))
        
        self.discard_frame = tk.Frame(self.center_frame, bg="#2E8B57")
        self.discard_frame.pack(side="left", padx=20)
        
        tk.Label(self.discard_frame, text="Current Card:", bg="#2E8B57", fg="white", 
                font=("Arial", 12)).pack()
        
        # Control buttons
        self.button_frame = tk.Frame(self.center_frame, bg="#2E8B57")
        self.button_frame.pack(side="right", padx=20)
        
        self.draw_button = tk.Button(self.button_frame, text="Draw Card", font=("Arial", 12),
                                   command=self.draw_card, bg="#FF6B6B", fg="white")
        self.draw_button.pack(pady=5)
        
        self.uno_button = tk.Button(self.button_frame, text="UNO!", font=("Arial", 12, "bold"),
                                  command=self.call_uno, bg="#FFD93D", fg="black")
        self.uno_button.pack(pady=5)
        
        # Bottom panel - player hand
        self.bottom_frame = tk.Frame(self.game_frame, bg="#2E8B57", height=150)
        self.bottom_frame.pack(fill="x", pady=10)
        
        tk.Label(self.bottom_frame, text="Your Hand:", bg="#2E8B57", fg="white", 
                font=("Arial", 14, "bold")).pack()
        
        self.hand_frame = tk.Frame(self.bottom_frame, bg="#2E8B57")
        self.hand_frame.pack(pady=10)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_bar = tk.Label(self.game_frame, textvariable=self.status_var, 
                                 bg="#1E6B3F", fg="white", font=("Arial", 12))
        self.status_bar.pack(fill="x", side="bottom")
    
    def show_start_screen(self):
        self.start_frame = tk.Frame(self.root, bg="#2E8B57")
        self.start_frame.pack(fill="both", expand=True)
        
        # Title
        title_label = tk.Label(self.start_frame, text="UNO", font=("Arial", 48, "bold"), 
                              bg="#2E8B57", fg="white")
        title_label.pack(pady=50)
        
        # Game setup
        setup_frame = tk.Frame(self.start_frame, bg="#2E8B57")
        setup_frame.pack(pady=20)
        
        tk.Label(setup_frame, text="Number of players:", bg="#2E8B57", fg="white", 
                font=("Arial", 14)).pack()
        
        self.player_count_var = tk.IntVar(value=2)
        player_scale = tk.Scale(setup_frame, from_=2, to=4, orient="horizontal", 
                              variable=self.player_count_var, bg="#2E8B57", fg="white",
                              font=("Arial", 12))
        player_scale.pack(pady=10)
        
        start_button = tk.Button(setup_frame, text="Start Game", font=("Arial", 16, "bold"),
                               command=self.start_new_game, bg="#4CAF50", fg="white",
                               padx=30, pady=10)
        start_button.pack(pady=20)
    
    def start_new_game(self):
        num_players = self.player_count_var.get()
        
        # Get player names
        player_names = ["You"]
        for i in range(1, num_players):
            player_names.append(f"CPU {i}")
        
        # Create players
        players = []
        players.append(Player("You", is_human=True))
        for i in range(1, num_players):
            players.append(Player(f"CPU {i}", is_human=False))
        
        # Initialize game
        self.game = UnoGame(players, self)
        
        # Hide start screen and show game
        self.start_frame.destroy()
        self.game_frame.pack(fill="both", expand=True)
        
        self.update_display()
        self.game.start_game()
    
    def update_display(self):
        if not self.game:
            return
        
        # Clear previous card widgets
        for widget in self.card_widgets:
            widget.destroy()
        self.card_widgets.clear()
        
        # Update player hand
        human_player = self.game.get_human_player()
        if human_player:
            for i, card in enumerate(human_player.hand):
                card_widget = CardWidget(self.hand_frame, card)
                card_widget.bind("<<CardClicked>>", lambda e, c=card: self.select_card(c))
                card_widget.grid(row=0, column=i, padx=2)
                self.card_widgets.append(card_widget)
        
        # Update top card
        if hasattr(self, 'discard_widget'):
            self.discard_widget.destroy()
        
        if self.game.discard_pile:
            self.discard_widget = CardWidget(self.discard_frame, self.game.get_top_card(), 
                                           clickable=False)
            self.discard_widget.pack()
        
        # Update status
        current_player = self.game.get_current_player()
        direction = "Clockwise" if self.game.direction == 1 else "Counter-clockwise"
        self.status_var.set(f"Current: {current_player.name} | Direction: {direction} | "
                          f"Cards left: {', '.join([f'{p.name}: {len(p.hand)}' for p in self.game.players])}")
        
        self.root.update()
    
    def select_card(self, card):
        # Deselect previous card
        if self.selected_card:
            for widget in self.card_widgets:
                if widget.card == self.selected_card:
                    widget.set_selected(False)
        
        # Select new card
        self.selected_card = card
        for widget in self.card_widgets:
            if widget.card == card:
                widget.set_selected(True)
        
        # Try to play the card
        self.play_selected_card()
    
    def play_selected_card(self):
        if not self.selected_card or not self.game:
            return
        
        human_player = self.game.get_human_player()
        if not human_player or self.game.get_current_player() != human_player:
            return
        
        top_card = self.game.get_top_card()
        if self.selected_card.can_play_on(top_card):
            # Handle wild cards
            if self.selected_card.card_type in [CardType.WILD, CardType.WILD_DRAW_FOUR]:
                color_dialog = ColorChooserDialog(self.root)
                self.root.wait_window(color_dialog.dialog)
                if color_dialog.result:
                    self.selected_card.color = color_dialog.result
                else:
                    return  # Cancel if no color chosen
            
            self.game.play_card(human_player, self.selected_card)
            self.selected_card = None
            self.update_display()
            
            # Check for game end
            if human_player.has_won():
                messagebox.showinfo("Game Over", "Congratulations! You won!")
                self.restart_game()
                return
            
            # Continue to next turn
            self.root.after(1000, self.game.continue_turn)
        else:
            messagebox.showwarning("Invalid Move", "You can't play that card!")
            self.selected_card = None
            self.update_display()
    
    def draw_card(self):
        if not self.game:
            return
        
        human_player = self.game.get_human_player()
        if not human_player or self.game.get_current_player() != human_player:
            return
        
        self.game.draw_cards(human_player, 1)
        self.update_display()
        self.game.next_player()
        self.root.after(1000, self.game.continue_turn)
    
    def call_uno(self):
        messagebox.showinfo("UNO!", "UNO called!")
    
    def restart_game(self):
        self.game_frame.destroy()
        self.setup_ui()
        self.show_start_screen()
    
    def run(self):
        self.root.mainloop()

class UnoGame:
    def __init__(self, players: List[Player], gui: UnoGUI):
        self.players = players
        self.gui = gui
        self.deck = Deck()
        self.discard_pile = []
        self.current_player_index = 0
        self.direction = 1
        self.game_over = False
        
        # Deal initial cards
        for _ in range(7):
            for player in self.players:
                card = self.deck.draw_card()
                if card:
                    player.add_card(card)
        
        # Set initial top card
        while True:
            top_card = self.deck.draw_card()
            if top_card and top_card.card_type not in [CardType.WILD, CardType.WILD_DRAW_FOUR]:
                self.discard_pile.append(top_card)
                break
    
    def get_current_player(self) -> Player:
        return self.players[self.current_player_index]
    
    def get_human_player(self) -> Optional[Player]:
        for player in self.players:
            if player.is_human:
                return player
        return None
    
    def next_player(self):
        self.current_player_index = (self.current_player_index + self.direction) % len(self.players)
    
    def reverse_direction(self):
        self.direction *= -1
    
    def get_top_card(self) -> Card:
        return self.discard_pile[-1]
    
    def reshuffle_deck(self):
        if len(self.discard_pile) > 1:
            top_card = self.discard_pile.pop()
            self.deck.cards.extend(self.discard_pile)
            self.deck.shuffle()
            self.discard_pile = [top_card]
    
    def draw_cards(self, player: Player, count: int):
        for _ in range(count):
            if self.deck.is_empty():
                self.reshuffle_deck()
            card = self.deck.draw_card()
            if card:
                player.add_card(card)
    
    def play_card(self, player: Player, card: Card):
        player.remove_card(card)
        self.discard_pile.append(card)
        
        # Handle special cards
        if card.card_type == CardType.SKIP:
            self.next_player()
        elif card.card_type == CardType.REVERSE:
            self.reverse_direction()
        elif card.card_type == CardType.DRAW_TWO:
            self.next_player()
            self.draw_cards(self.get_current_player(), 2)
            return
        elif card.card_type == CardType.WILD_DRAW_FOUR:
            self.next_player()
            self.draw_cards(self.get_current_player(), 4)
            return
        
        self.next_player()
    
    def cpu_play_turn(self):
        current_player = self.get_current_player()
        if current_player.is_human:
            return
        
        top_card = self.get_top_card()
        playable_cards = current_player.get_playable_cards(top_card)
        
        if playable_cards:
            # Simple AI: play first available card
            chosen_card = playable_cards[0]
            
            # Handle wild cards
            if chosen_card.card_type in [CardType.WILD, CardType.WILD_DRAW_FOUR]:
                # Choose most common color in hand
                color_counts = {Color.RED: 0, Color.YELLOW: 0, Color.GREEN: 0, Color.BLUE: 0}
                for card in current_player.hand:
                    if card.color in color_counts:
                        color_counts[card.color] += 1
                chosen_card.color = max(color_counts, key=color_counts.get)
            
            self.play_card(current_player, chosen_card)
            
            if current_player.has_won():
                messagebox.showinfo("Game Over", f"{current_player.name} wins!")
                self.gui.restart_game()
                return
        else:
            self.draw_cards(current_player, 1)
            self.next_player()
        
        self.gui.update_display()
    
    def continue_turn(self):
        if self.game_over:
            return
        
        current_player = self.get_current_player()
        if not current_player.is_human:
            self.cpu_play_turn()
            self.gui.root.after(1500, self.continue_turn)
    
    def start_game(self):
        if not self.get_current_player().is_human:
            self.gui.root.after(1000, self.continue_turn)

if __name__ == "__main__":
    game_gui = UnoGUI()
    game_gui.run()