"""
War Card Game - 4 Players
Visual simulation using tkinter (built into Python, no install needed)
"""

import tkinter as tk
from tkinter import font as tkfont
import random


SUITS = ['S', 'H', 'D', 'C']  # Spades, Hearts, Diamonds, Clubs
SUIT_SYMBOLS = {'S': 'Spades', 'H': 'Hearts', 'D': 'Diamonds', 'C': 'Clubs'}
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
RANK_VALUES = {r: i for i, r in enumerate(RANKS, 2)}
RED_SUITS = {'H', 'D'}

PLAYER_COLORS = ['#4FC3F7', '#81C784', '#FFB74D', '#F06292']
PLAYER_NAMES = ['Player 1', 'Player 2', 'Player 3', 'Player 4']
PLAYER_BG = ['#0D2A3A', '#0D2A1A', '#2A1D00', '#2A0D1A']


def make_deck():
    deck = [(r, s) for s in SUITS for r in RANKS]
    random.shuffle(deck)
    return deck


def deal(deck):
    hands = [[], [], [], []]
    for i, card in enumerate(deck):
        hands[i % 4].append(card)
    return hands


def card_value(card):
    return RANK_VALUES[card[0]]



class WarGame:
    def __init__(self):
        self.reset()

    def reset(self):
        deck = make_deck()
        self.hands = deal(deck)
        self.round_num = 0
        self.log = []
        self.game_over = False
        self.winner = None

    def reshuffle_if_needed(self):
        for i, hand in enumerate(self.hands):
            if len(hand) == 0:
                new_deck = make_deck()
                self.hands[i] = new_deck[:13]
                self.log.append(f"  [RESHUFFLE] {PLAYER_NAMES[i]} got a new hand!")

    def play_round(self):
        if self.game_over:
            return None
        self.round_num += 1
        self.reshuffle_if_needed()

        played = []
        for i in range(4):
            if self.hands[i]:
                played.append((i, self.hands[i].pop(0)))
            else:
                played.append((i, None))

        result = self._resolve(played, war_pot=[])
        self._check_winner()
        return result

    def _resolve(self, played, war_pot):
        valid = [(i, c) for i, c in played if c is not None]
        if not valid:
            return {'type': 'no_cards', 'played': played}

        max_val = max(card_value(c) for _, c in valid)
        winners = [(i, c) for i, c in valid if card_value(c) == max_val]
        all_cards = [c for _, c in played if c is not None] + war_pot

        if len(winners) == 1:
            winner_idx = winners[0][0]
            random.shuffle(all_cards)
            self.hands[winner_idx].extend(all_cards)
            return {
                'type': 'win',
                'played': played,
                'winner': winner_idx,
                'pot': all_cards,
            }
        else:
            war_cards = list(all_cards)
            new_played = []
            for i, _ in winners:
                for _ in range(3):
                    if self.hands[i]:
                        war_cards.append(self.hands[i].pop(0))
                face_up = self.hands[i].pop(0) if self.hands[i] else None
                new_played.append((i, face_up))

            return {
                'type': 'war',
                'played': played,
                'sub': self._resolve(new_played, war_cards),
            }

    def _check_winner(self):
        counts = [len(h) for h in self.hands]
        total = sum(counts)
        for i, c in enumerate(counts):
            if c == total:
                self.game_over = True
                self.winner = i
                return
        if self.round_num >= 1000:
            best = max(range(4), key=lambda i: counts[i])
            self.game_over = True
            self.winner = best

    def hand_sizes(self):
        return [len(h) for h in self.hands]



class WarApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("War Card Game - 4 Players")
        self.configure(bg='#1A1A2E')
        self.geometry("640x700")
        self.resizable(True, True)

        self.game = WarGame()
        self.auto_playing = False
        self.auto_speed = 600

        self._build_ui()
        self._refresh_counts()

    def _build_ui(self):
        # Title
        tk.Label(self, text="WAR - 4 Player Card Game",
                 font=('Georgia', 18, 'bold'),
                 bg='#1A1A2E', fg='#E8D5B7').pack(pady=(12, 2))

        tk.Label(self, text="Highest card wins. Ties trigger WAR (3 face-down + 1 face-up).",
                 font=('Georgia', 9),
                 bg='#1A1A2E', fg='#7A8BA0').pack(pady=(0, 8))

        # 2x2 player grid
        arena = tk.Frame(self, bg='#1A1A2E')
        arena.pack(fill='x', padx=16, pady=4)
        arena.columnconfigure(0, weight=1)
        arena.columnconfigure(1, weight=1)

        self.player_frames = []
        self.card_labels = []
        self.count_labels = []
        self.name_labels = []

        positions = [(0, 0), (0, 1), (1, 0), (1, 1)]
        for idx, (row, col) in enumerate(positions):
            arena.rowconfigure(row, weight=1)
            pf = tk.Frame(arena, bg=PLAYER_BG[idx],
                          highlightbackground=PLAYER_COLORS[idx],
                          highlightthickness=2, padx=10, pady=8)
            pf.grid(row=row, column=col, padx=6, pady=6, sticky='nsew')

            name_lbl = tk.Label(pf, text=PLAYER_NAMES[idx],
                                font=('Georgia', 11, 'bold'),
                                bg=PLAYER_BG[idx], fg=PLAYER_COLORS[idx])
            name_lbl.pack()

            # Card display box
            card_lbl = tk.Label(pf, text="---",
                                font=('Courier', 22, 'bold'),
                                width=7, height=2,
                                bg='white', fg='#333',
                                relief='raised', borderwidth=3)
            card_lbl.pack(pady=5)

            count_lbl = tk.Label(pf, text="13 cards",
                                 font=('Courier', 9),
                                 bg=PLAYER_BG[idx], fg='#AAAAAA')
            count_lbl.pack()

            self.player_frames.append(pf)
            self.card_labels.append(card_lbl)
            self.count_labels.append(count_lbl)
            self.name_labels.append(name_lbl)

        # Round + status
        self.round_label = tk.Label(self, text="Round 0",
                                    font=('Georgia', 12, 'bold'),
                                    bg='#1A1A2E', fg='#E8D5B7')
        self.round_label.pack(pady=(8, 2))

        self.status_label = tk.Label(self, text="Press  Next Round  to begin",
                                     font=('Georgia', 10),
                                     bg='#1A1A2E', fg='#90A4AE', wraplength=580)
        self.status_label.pack(pady=(0, 6))

        # Battle log
        log_outer = tk.Frame(self, bg='#0D1117', highlightbackground='#2A2A3E',
                             highlightthickness=1)
        log_outer.pack(fill='both', expand=True, padx=16, pady=(0, 6))

        tk.Label(log_outer, text="Battle Log",
                 bg='#0D1117', fg='#445566',
                 font=('Courier', 9)).pack(anchor='w', padx=6, pady=(4, 0))

        scroll_frame = tk.Frame(log_outer, bg='#0D1117')
        scroll_frame.pack(fill='both', expand=True, padx=4, pady=4)

        self.log_text = tk.Text(scroll_frame, height=9,
                                bg='#0D1117', fg='#8BAABB',
                                font=('Courier', 9),
                                relief='flat', wrap='word')
        self.log_text.pack(side='left', fill='both', expand=True)

        sb = tk.Scrollbar(scroll_frame, command=self.log_text.yview)
        sb.pack(side='right', fill='y')
        self.log_text.config(yscrollcommand=sb.set)

        # Speed control
        spd_frame = tk.Frame(self, bg='#1A1A2E')
        spd_frame.pack(pady=2)
        tk.Label(spd_frame, text="Speed (ms):", bg='#1A1A2E', fg='#7A8BA0',
                 font=('Courier', 9)).pack(side='left')
        self.speed_var = tk.IntVar(value=600)
        tk.Scale(spd_frame, from_=100, to=2000, orient='horizontal',
                 variable=self.speed_var, bg='#1A1A2E', fg='#E8D5B7',
                 troughcolor='#333', highlightthickness=0, length=180,
                 command=lambda v: setattr(self, 'auto_speed', int(v))
                 ).pack(side='left', padx=4)

        # Buttons
        btn_frame = tk.Frame(self, bg='#1A1A2E')
        btn_frame.pack(pady=(4, 12))

        tk.Button(btn_frame, text="Next Round",
                  font=('Georgia', 11, 'bold'), relief='flat',
                  bg='#1B5E20', fg='white', activebackground='#2E7D32',
                  padx=14, pady=6, cursor='hand2',
                  command=self._next_round).pack(side='left', padx=5)

        self.auto_btn = tk.Button(btn_frame, text="Auto Play",
                                  font=('Georgia', 11, 'bold'), relief='flat',
                                  bg='#1A237E', fg='white', activebackground='#283593',
                                  padx=14, pady=6, cursor='hand2',
                                  command=self._toggle_auto)
        self.auto_btn.pack(side='left', padx=5)

        tk.Button(btn_frame, text="New Game",
                  font=('Georgia', 11, 'bold'), relief='flat',
                  bg='#4A1010', fg='white', activebackground='#7B2020',
                  padx=14, pady=6, cursor='hand2',
                  command=self._new_game).pack(side='left', padx=5)


    def _card_display(self, card):
        """Return (text, fg_color) for a card label."""
        if card is None:
            return "  ---  ", '#999999', 'white'
        rank, suit = card
        text = f" {rank} {suit} "
        color = '#CC1100' if suit in RED_SUITS else '#111111'
        return text, color, 'white'

    def _refresh_counts(self):
        sizes = self.game.hand_sizes()
        for i in range(4):
            self.count_labels[i].config(text=f"{sizes[i]} cards")

    def _show_played(self, played_cards, winner_idx=None, war_idxs=None):
        war_idxs = war_idxs or []
        for i, card in enumerate(played_cards):
            text, fg, bg = self._card_display(card)
            if i == winner_idx:
                border = '#FFD700'
                thickness = 4
            elif i in war_idxs:
                border = '#FF3333'
                thickness = 3
            else:
                border = '#CCCCCC'
                thickness = 1
            self.card_labels[i].config(
                text=text, fg=fg, bg=bg,
                highlightbackground=border,
                highlightthickness=thickness
            )

    def _reset_card_displays(self):
        for lbl in self.card_labels:
            lbl.config(text="  ---  ", fg='#999', bg='white', highlightthickness=0)

    def _log(self, line):
        self.log_text.config(state='normal')
        self.log_text.insert('end', line + '\n')
        self.log_text.see('end')
        self.log_text.config(state='disabled')

    def _format_result(self, result, depth=0):
        pad = "  " * depth
        lines = []
        if result['type'] == 'win':
            cards_str = '   '.join(
                f"{PLAYER_NAMES[i]}: {c[0]}-{c[1]}" if c else f"{PLAYER_NAMES[i]}: none"
                for i, c in result['played']
            )
            lines.append(f"{pad}Cards: {cards_str}")
            lines.append(f"{pad}>> {PLAYER_NAMES[result['winner']]} wins {len(result['pot'])} cards!")
        elif result['type'] == 'war':
            cards_str = '   '.join(
                f"{PLAYER_NAMES[i]}: {c[0]}-{c[1]}" if c else f"{PLAYER_NAMES[i]}: none"
                for i, c in result['played']
            )
            lines.append(f"{pad}Cards: {cards_str}")
            lines.append(f"{pad}*** WAR! 3 face-down cards placed ***")
            lines.extend(self._format_result(result['sub'], depth + 1))
        elif result['type'] == 'no_cards':
            lines.append(f"{pad}[!] A player has no cards left.")
        return lines

    def _extract_display_info(self, result):
        """Get card list, winner index, and war player indices for display."""
        if result['type'] == 'win':
            cards = [c for _, c in result['played']]
            return cards, result['winner'], []
        elif result['type'] == 'war':
            cards = [c for _, c in result['played']]
            war_idxs = [i for i, c in result['played'] if c is not None]
            return cards, None, war_idxs
        else:
            return [None, None, None, None], None, []


    def _next_round(self):
        if self.game.game_over:
            return

        result = self.game.play_round()
        if result is None:
            return

        self._refresh_counts()
        self.round_label.config(text=f"Round {self.game.round_num}")

        cards, winner_idx, war_idxs = self._extract_display_info(result)
        self._show_played(cards, winner_idx, war_idxs)

        self._log(f"\n--- Round {self.game.round_num} ---")
        for line in self._format_result(result):
            self._log(line)

        # Show any reshuffle messages from this round
        for msg in self.game.log:
            if '[RESHUFFLE]' in msg:
                self._log(msg)
        self.game.log.clear()

        sizes = self.game.hand_sizes()
        self.status_label.config(
            text="  ".join(f"{PLAYER_NAMES[i]}: {sizes[i]}" for i in range(4)),
            fg='#90A4AE'
        )

        if self.game.game_over:
            self._declare_winner()

    def _declare_winner(self):
        self.auto_playing = False
        self.auto_btn.config(text="Auto Play", bg='#1A237E')
        w = self.game.winner
        sizes = self.game.hand_sizes()
        msg = f"WINNER: {PLAYER_NAMES[w]} with {sizes[w]} cards after {self.game.round_num} rounds!"
        self._log(f"\n{'=' * 45}")
        self._log(msg)
        self._log('=' * 45)
        self.status_label.config(text=msg, fg='#FFD700')
        self.name_labels[w].config(fg='#FFD700')
        self.player_frames[w].config(highlightbackground='#FFD700', highlightthickness=4)

    def _toggle_auto(self):
        if self.game.game_over:
            return
        self.auto_playing = not self.auto_playing
        if self.auto_playing:
            self.auto_btn.config(text="Pause", bg='#B71C1C')
            self._auto_step()
        else:
            self.auto_btn.config(text="Auto Play", bg='#1A237E')

    def _auto_step(self):
        if not self.auto_playing or self.game.game_over:
            return
        self._next_round()
        self.after(self.auto_speed, self._auto_step)

    def _new_game(self):
        self.auto_playing = False
        self.auto_btn.config(text="Auto Play", bg='#1A237E')
        self.game.reset()
        self._reset_card_displays()
        self._refresh_counts()
        self.round_label.config(text="Round 0")
        self.status_label.config(text="Press  Next Round  to begin", fg='#90A4AE')
        self.log_text.config(state='normal')
        self.log_text.delete('1.0', 'end')
        self.log_text.config(state='disabled')
        for i in range(4):
            self.name_labels[i].config(fg=PLAYER_COLORS[i])
            self.player_frames[i].config(
                highlightbackground=PLAYER_COLORS[i], highlightthickness=2)



if __name__ == '__main__':
    app = WarApp()
    app.mainloop()