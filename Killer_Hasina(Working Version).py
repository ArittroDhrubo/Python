import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random
from enum import Enum
from typing import List, Dict, Optional
import threading
import time

class Role(Enum):
    KILLER = "Killer"
    DOCTOR = "Doctor"
    POLICE = "Police"
    CIVILIAN = "Civilian"

class PlayerStatus(Enum):
    ALIVE = "Alive"
    DEAD = "Dead"
    DISMISSED = "Dismissed"

class Player:
    def __init__(self, name: str, role: Role):
        self.name = name
        self.role = role
        self.status = PlayerStatus.ALIVE
        self.votes = 0
        self.keyword = ""  # For killers to use instead of real names

class GamePhase(Enum):
    SETUP = "Setup"
    KILLER_TURN = "Killer's Turn"
    DOCTOR_TURN = "Doctor's Turn"
    POLICE_TURN = "Police's Turn"
    PUBLIC_DISCUSSION = "Public Discussion"
    VOTING = "Voting"
    INDIVIDUAL_VOTING = "Individual Voting"
    GAME_OVER = "Game Over"

class KillerHasinaGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Killer Hasina - Professional Edition")
        self.root.geometry("1400x900")
        self.root.configure(bg="#1a1a2e")
        
        # Game state
        self.players: List[Player] = []
        self.current_phase = GamePhase.SETUP
        self.round_number = 0
        self.killer_survival_rounds = 0
        self.target_killed = None
        self.doctor_saved = None
        self.police_guess = None
        self.police_correct = False
        self.votes: Dict[str, int] = {}
        self.individual_votes: Dict[str, str] = {}  # Player name -> Voted target
        self.current_voter_index = 0
        self.keywords_assigned = False
        
        # Discussion timer
        self.discussion_time_left = 60  # 60 seconds
        self.discussion_timer = None
        
        # UI Setup
        self.setup_styles()
        self.create_main_interface()
        
    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Custom colors
        self.colors = {
            'bg': '#1a1a2e',
            'secondary': '#16213e',
            'accent': '#0f3460',
            'highlight': '#e94560',
            'text': '#ffffff',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c'
        }
        
        # Configure styles
        self.style.configure('Title.TLabel', 
                           background=self.colors['bg'], 
                           foreground=self.colors['highlight'],
                           font=('Arial', 24, 'bold'))
        
        self.style.configure('Header.TLabel', 
                           background=self.colors['bg'], 
                           foreground=self.colors['text'],
                           font=('Arial', 16, 'bold'))
        
        self.style.configure('Custom.TButton',
                           background=self.colors['accent'],
                           foreground=self.colors['text'],
                           font=('Arial', 12, 'bold'),
                           padding=10)
        
        self.style.configure('Danger.TButton',
                           background=self.colors['danger'],
                           foreground=self.colors['text'],
                           font=('Arial', 12, 'bold'),
                           padding=10)
        
        self.style.configure('Success.TButton',
                           background=self.colors['success'],
                           foreground=self.colors['text'],
                           font=('Arial', 12, 'bold'),
                           padding=10)
        
    def create_main_interface(self):
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(main_frame, text="🎭 KILLER HASINA 🎭", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Game info frame
        self.info_frame = tk.Frame(main_frame, bg=self.colors['secondary'], relief=tk.RAISED, bd=2)
        self.info_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.phase_label = ttk.Label(self.info_frame, text="Phase: Setup", style='Header.TLabel')
        self.phase_label.pack(pady=10)
        
        self.round_label = ttk.Label(self.info_frame, text="Round: 0", style='Header.TLabel')
        self.round_label.pack(pady=(0, 10))
        
        # Timer label for discussion phase
        self.timer_label = ttk.Label(self.info_frame, text="", style='Header.TLabel')
        
        # Content area
        self.content_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Start with setup screen
        self.show_setup_screen()
        
    def show_setup_screen(self):
        self.clear_content()
        
        setup_frame = tk.Frame(self.content_frame, bg=self.colors['bg'])
        setup_frame.pack(expand=True)
        
        # Player registration
        ttk.Label(setup_frame, text="Register Players (3-10 players)", style='Header.TLabel').pack(pady=20)
        
        # Player list
        self.player_listbox = tk.Listbox(setup_frame, bg=self.colors['secondary'], 
                                       fg=self.colors['text'], font=('Arial', 12),
                                       height=8, width=40)
        self.player_listbox.pack(pady=10)
        
        # Input frame
        input_frame = tk.Frame(setup_frame, bg=self.colors['bg'])
        input_frame.pack(pady=10)
        
        self.player_entry = tk.Entry(input_frame, font=('Arial', 12), width=20)
        self.player_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.player_entry.bind('<Return>', lambda e: self.add_player())
        
        ttk.Button(input_frame, text="Add Player", command=self.add_player, 
                  style='Custom.TButton').pack(side=tk.LEFT)
        
        # Control buttons
        button_frame = tk.Frame(setup_frame, bg=self.colors['bg'])
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Remove Selected", command=self.remove_player,
                  style='Danger.TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="Start Game", command=self.start_game,
                  style='Custom.TButton').pack(side=tk.LEFT)
        
    def add_player(self):
        name = self.player_entry.get().strip()
        if name and len(self.players) < 10:
            if not any(p.name == name for p in self.players):
                self.players.append(Player(name, Role.CIVILIAN))  # Temporary role
                self.player_listbox.insert(tk.END, name)
                self.player_entry.delete(0, tk.END)
            else:
                messagebox.showwarning("Duplicate Name", "Player name already exists!")
        elif len(self.players) >= 10:
            messagebox.showwarning("Maximum Players", "Maximum 10 players allowed!")
            
    def remove_player(self):
        selected = self.player_listbox.curselection()
        if selected:
            index = selected[0]
            self.player_listbox.delete(index)
            self.players.pop(index)
            
    def start_game(self):
        if len(self.players) < 3:
            messagebox.showwarning("Not Enough Players", "Minimum 3 players required!")
            return
            
        self.assign_roles()
        self.assign_keywords()
        self.show_game_info()
        self.current_phase = GamePhase.KILLER_TURN
        self.round_number = 1
        self.update_info_display()
        self.show_game_screen()
        self.start_killer_turn()
        
    def assign_roles(self):
        # Shuffle players
        random.shuffle(self.players)
        
        # Assign roles based on player count
        num_players = len(self.players)
        num_killers = 2 if num_players >= 7 else 1
        
        # Assign killer(s)
        for i in range(num_killers):
            self.players[i].role = Role.KILLER
            
        # Assign doctor and police
        self.players[num_killers].role = Role.DOCTOR
        self.players[num_killers + 1].role = Role.POLICE
        
        # Rest remain civilians
        
    def assign_keywords(self):
        """Assign keywords to each player for killers to use"""
        keywords = ["Alpha", "Beta", "Gamma", "Delta", "Echo", "Foxtrot", "Golf", "Hotel", "India", "Juliet"]
        for i, player in enumerate(self.players):
            player.keyword = keywords[i]
        self.keywords_assigned = True
        
    def show_game_info(self):
        """Show number of killers and keywords to all players"""
        num_killers = len([p for p in self.players if p.role == Role.KILLER])
        
        info_message = f"GAME INFORMATION:\n\n"
        info_message += f"Total Players: {len(self.players)}\n"
        info_message += f"Number of Killers: {num_killers}\n\n"
        info_message += "PLAYER KEYWORDS (for killers to use):\n\n"
        
        for player in self.players:
            info_message += f"{player.name} = {player.keyword}\n"
            
        info_message += "\nKillers will use these keywords instead of real names!"
        
        messagebox.showinfo("Game Setup Complete", info_message)
        
    def show_game_screen(self):
        self.clear_content()
        
        # Create two-column layout
        left_frame = tk.Frame(self.content_frame, bg=self.colors['secondary'], width=400)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_frame.pack_propagate(False)
        
        right_frame = tk.Frame(self.content_frame, bg=self.colors['secondary'])
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Player list (left side)
        ttk.Label(left_frame, text="Players & Keywords", style='Header.TLabel').pack(pady=10)
        
        self.player_display = tk.Text(left_frame, bg=self.colors['accent'], fg=self.colors['text'],
                                    font=('Arial', 11), height=25, width=35, state=tk.DISABLED)
        self.player_display.pack(padx=10, pady=(0, 10), fill=tk.BOTH, expand=True)
        
        # Game action area (right side)
        ttk.Label(right_frame, text="Game Actions", style='Header.TLabel').pack(pady=10)
        
        self.action_frame = tk.Frame(right_frame, bg=self.colors['secondary'])
        self.action_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        self.update_player_display()
        
    def update_player_display(self):
        self.player_display.config(state=tk.NORMAL)
        self.player_display.delete(1.0, tk.END)
        
        for i, player in enumerate(self.players, 1):
            status_icon = "💀" if player.status == PlayerStatus.DEAD else \
                         "🚫" if player.status == PlayerStatus.DISMISSED else "✅"
            
            self.player_display.insert(tk.END, f"{i}. {status_icon} {player.name}\n")
            self.player_display.insert(tk.END, f"   Keyword: {player.keyword}\n")
            if player.status == PlayerStatus.DEAD:
                self.player_display.insert(tk.END, f"   Status: DEAD\n")
            elif player.status == PlayerStatus.DISMISSED:
                self.player_display.insert(tk.END, f"   Status: DISMISSED\n")
            self.player_display.insert(tk.END, "\n")
            
        self.player_display.config(state=tk.DISABLED)
        
    def update_info_display(self):
        self.phase_label.config(text=f"Phase: {self.current_phase.value}")
        self.round_label.config(text=f"Round: {self.round_number}")
        
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
    def clear_action_frame(self):
        for widget in self.action_frame.winfo_children():
            widget.destroy()
            
    def start_killer_turn(self):
        self.current_phase = GamePhase.KILLER_TURN
        self.update_info_display()
        self.clear_action_frame()
        
        # Get alive killers
        killers = [p for p in self.players if p.role == Role.KILLER and p.status == PlayerStatus.ALIVE]
        if not killers:
            self.end_game("Civilians win! All killers eliminated.")
            return
            
        ttk.Label(self.action_frame, text=f"🔪 KILLERS' TURN", 
                 style='Header.TLabel').pack(pady=20)
        
        killer_names = ", ".join([k.name for k in killers])
        ttk.Label(self.action_frame, text=f"Killers: {killer_names}\nDiscuss and choose your target using KEYWORDS:", 
                 background=self.colors['secondary'], foreground=self.colors['text'],
                 font=('Arial', 12)).pack(pady=10)
        
        # Target selection using keywords
        alive_targets = [p for p in self.players if p.status == PlayerStatus.ALIVE and p.role != Role.KILLER]
        
        self.target_var = tk.StringVar()
        target_frame = tk.Frame(self.action_frame, bg=self.colors['secondary'])
        target_frame.pack(pady=10)
        
        ttk.Label(target_frame, text="Select target by KEYWORD:", 
                 background=self.colors['secondary'], foreground=self.colors['warning'],
                 font=('Arial', 11, 'bold')).pack(pady=(0, 10))
        
        for target in alive_targets:
            tk.Radiobutton(target_frame, text=f"{target.keyword} ({target.name})", 
                          variable=self.target_var, value=target.name, 
                          bg=self.colors['secondary'], fg=self.colors['text'], 
                          font=('Arial', 11), selectcolor=self.colors['accent']).pack(anchor=tk.W)
        
        ttk.Button(self.action_frame, text="Confirm Kill", 
                  command=self.killer_action, 
                  style='Danger.TButton').pack(pady=20)
        
    def killer_action(self):
        target_name = self.target_var.get()
        if not target_name:
            messagebox.showwarning("No Selection", "Please select a target!")
            return
            
        self.target_killed = next(p for p in self.players if p.name == target_name)
        target_keyword = self.target_killed.keyword
        messagebox.showinfo("Action Confirmed", f"Killers have chosen target: {target_keyword}")
        self.start_doctor_turn()
        
    def start_doctor_turn(self):
        self.current_phase = GamePhase.DOCTOR_TURN
        self.update_info_display()
        self.clear_action_frame()
        
        doctor = next((p for p in self.players if p.role == Role.DOCTOR and p.status == PlayerStatus.ALIVE), None)
        if not doctor:
            self.resolve_night_actions()
            return
            
        ttk.Label(self.action_frame, text=f"🏥 DOCTOR'S TURN", 
                 style='Header.TLabel').pack(pady=20)
        
        ttk.Label(self.action_frame, text=f"Doctor: {doctor.name}\nSomeone was attacked! Choose who to save:", 
                 background=self.colors['secondary'], foreground=self.colors['text'],
                 font=('Arial', 12)).pack(pady=10)
        
        # Save selection
        alive_players = [p for p in self.players if p.status == PlayerStatus.ALIVE]
        
        self.save_var = tk.StringVar()
        save_frame = tk.Frame(self.action_frame, bg=self.colors['secondary'])
        save_frame.pack(pady=10)
        
        for player in alive_players:
            tk.Radiobutton(save_frame, text=player.name, variable=self.save_var, 
                          value=player.name, bg=self.colors['secondary'], 
                          fg=self.colors['text'], font=('Arial', 11),
                          selectcolor=self.colors['accent']).pack(anchor=tk.W)
        
        ttk.Button(self.action_frame, text="Confirm Save", 
                  command=self.doctor_action, 
                  style='Custom.TButton').pack(pady=20)
        
    def doctor_action(self):
        save_name = self.save_var.get()
        if not save_name:
            messagebox.showwarning("No Selection", "Please select someone to save!")
            return
            
        self.doctor_saved = next(p for p in self.players if p.name == save_name)
        messagebox.showinfo("Action Confirmed", f"Doctor has chosen to save: {save_name}")
        self.start_police_turn()
        
    def start_police_turn(self):
        self.current_phase = GamePhase.POLICE_TURN
        self.update_info_display()
        self.clear_action_frame()
        
        police = next((p for p in self.players if p.role == Role.POLICE and p.status == PlayerStatus.ALIVE), None)
        if not police:
            self.resolve_night_actions()
            return
            
        ttk.Label(self.action_frame, text=f"👮 POLICE'S TURN", 
                 style='Header.TLabel').pack(pady=20)
        
        ttk.Label(self.action_frame, text=f"Police: {police.name}\nWho do you think is the killer?", 
                 background=self.colors['secondary'], foreground=self.colors['text'],
                 font=('Arial', 12)).pack(pady=10)
        
        # Suspect selection
        alive_players = [p for p in self.players if p.status == PlayerStatus.ALIVE and p != police]
        
        self.suspect_var = tk.StringVar()
        suspect_frame = tk.Frame(self.action_frame, bg=self.colors['secondary'])
        suspect_frame.pack(pady=10)
        
        for player in alive_players:
            tk.Radiobutton(suspect_frame, text=player.name, variable=self.suspect_var, 
                          value=player.name, bg=self.colors['secondary'], 
                          fg=self.colors['text'], font=('Arial', 11),
                          selectcolor=self.colors['accent']).pack(anchor=tk.W)
        
        ttk.Button(self.action_frame, text="Confirm Suspicion", 
                  command=self.police_action, 
                  style='Custom.TButton').pack(pady=20)
        
    def police_action(self):
        suspect_name = self.suspect_var.get()
        if not suspect_name:
            messagebox.showwarning("No Selection", "Please select a suspect!")
            return
            
        self.police_guess = next(p for p in self.players if p.name == suspect_name)
        self.police_correct = self.police_guess.role == Role.KILLER
        
        result = "CORRECT! You found a killer!" if self.police_correct else "WRONG! That's not the killer."
        messagebox.showinfo("Investigation Result", f"Police guess: {suspect_name}\n{result}")
        
        self.resolve_night_actions()
        
    def resolve_night_actions(self):
        # Check if doctor saved the target
        if self.doctor_saved and self.target_killed and self.doctor_saved == self.target_killed:
            # Target was saved
            messagebox.showinfo("Night Result", f"{self.target_killed.name} was attacked but saved by the doctor!")
        else:
            # Target dies
            if self.target_killed:
                self.target_killed.status = PlayerStatus.DEAD
                messagebox.showinfo("Night Result", f"💀 {self.target_killed.name} was killed!")
        
        self.update_player_display()
        self.start_public_discussion()
        
        
    def start_public_discussion(self):
        self.current_phase = GamePhase.PUBLIC_DISCUSSION
        self.update_info_display()
        self.clear_action_frame()
        self.discussion_time_left = 60
        
        ttk.Label(self.action_frame, text="🗣️ PUBLIC DISCUSSION", 
                 style='Header.TLabel').pack(pady=20)
        
        # Show night results
        if self.target_killed and self.target_killed.status == PlayerStatus.DEAD:
            ttk.Label(self.action_frame, text=f"💀 {self.target_killed.name} was found dead!", 
                     background=self.colors['secondary'], foreground=self.colors['danger'],
                     font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Timer display
        self.timer_label.pack(pady=5)
        self.update_timer_display()
        
        # Discussion area
        discussion_frame = tk.Frame(self.action_frame, bg=self.colors['accent'], relief=tk.RAISED, bd=2)
        discussion_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        ttk.Label(discussion_frame, text="Discussion Time - Talk about who might be the killer!", 
                 background=self.colors['accent'], foreground=self.colors['text'],
                 font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Manual proceed button
        ttk.Button(self.action_frame, text="Skip Discussion & Proceed to Voting", 
                  command=self.end_discussion, 
                  style='Custom.TButton').pack(pady=10)
        
        # Start countdown timer
        self.start_discussion_timer()
        
    def start_discussion_timer(self):
        """Start the discussion countdown timer"""
        if self.discussion_time_left > 0:
            self.update_timer_display()
            self.discussion_timer = self.root.after(1000, self.countdown_discussion)
        else:
            self.end_discussion()
            
    def countdown_discussion(self):
        """Countdown function for discussion timer"""
        self.discussion_time_left -= 1
        if self.discussion_time_left > 0:
            self.update_timer_display()
            self.discussion_timer = self.root.after(1000, self.countdown_discussion)
        else:
            self.end_discussion()
            
    def update_timer_display(self):
        """Update the timer display"""
        self.timer_label.config(text=f"Discussion Time: {self.discussion_time_left}s")
        
    def end_discussion(self):
        """End discussion and move to voting"""
        if self.discussion_timer:
            self.root.after_cancel(self.discussion_timer)
        self.timer_label.pack_forget()
        self.start_individual_voting()
        
    def start_individual_voting(self):
        self.current_phase = GamePhase.INDIVIDUAL_VOTING
        self.update_info_display()
        self.individual_votes = {}
        self.current_voter_index = 0
        
        # Get alive players for voting
        alive_players = [p for p in self.players if p.status == PlayerStatus.ALIVE]
        
        if not alive_players:
            self.end_game("Game Over - No players left!")
            return
            
        self.conduct_individual_vote(alive_players)
        
    def conduct_individual_vote(self, alive_players):
        """Conduct individual voting for each player"""
        if self.current_voter_index >= len(alive_players):
            self.process_votes()
            return
            
        current_voter = alive_players[self.current_voter_index]
        self.clear_action_frame()
        
        ttk.Label(self.action_frame, text="🗳️ INDIVIDUAL VOTING", 
                 style='Header.TLabel').pack(pady=20)
        
        ttk.Label(self.action_frame, text=f"Voter: {current_voter.name}\nWho do you think is the killer?", 
                 background=self.colors['secondary'], foreground=self.colors['text'],
                 font=('Arial', 14, 'bold')).pack(pady=20)
        
        # Voting options (excluding the current voter)
        vote_candidates = [p for p in alive_players if p != current_voter]
        
        self.individual_vote_var = tk.StringVar()
        vote_frame = tk.Frame(self.action_frame, bg=self.colors['secondary'])
        vote_frame.pack(pady=20)
        
        # Skip option
        tk.Radiobutton(vote_frame, text="Skip (No Vote)", variable=self.individual_vote_var, 
                      value="SKIP", bg=self.colors['secondary'], 
                      fg=self.colors['warning'], font=('Arial', 12, 'bold'),
                      selectcolor=self.colors['accent']).pack(anchor=tk.W, pady=5)
        
        for candidate in vote_candidates:
            tk.Radiobutton(vote_frame, text=candidate.name, variable=self.individual_vote_var, 
                          value=candidate.name, bg=self.colors['secondary'], 
                          fg=self.colors['text'], font=('Arial', 12),
                          selectcolor=self.colors['accent']).pack(anchor=tk.W, pady=2)
        
        ttk.Button(self.action_frame, text="Cast Vote", 
                  command=lambda: self.record_individual_vote(current_voter), 
                  style='Custom.TButton').pack(pady=30)
        
    def record_individual_vote(self, voter):
        """Record the individual vote and move to next voter"""
        vote = self.individual_vote_var.get()
        if not vote:
            messagebox.showwarning("No Selection", "Please make a selection!")
            return
            
        self.individual_votes[voter.name] = vote
        messagebox.showinfo("Vote Recorded", f"{voter.name}'s vote has been recorded.")
        
        self.current_voter_index += 1
        alive_players = [p for p in self.players if p.status == PlayerStatus.ALIVE]
        self.conduct_individual_vote(alive_players)
        
    def process_votes(self):
        """Process all individual votes and determine the result"""
        self.clear_action_frame()
        
        # Count votes
        vote_counts = {}
        total_votes = 0
        skip_votes = 0
        
        for voter, vote in self.individual_votes.items():
            if vote == "SKIP":
                skip_votes += 1
            else:
                vote_counts[vote] = vote_counts.get(vote, 0) + 1
                total_votes += 1
        
        # Display voting results
        ttk.Label(self.action_frame, text="🗳️ VOTING RESULTS", 
                 style='Header.TLabel').pack(pady=20)
        
        results_text = "Vote Summary:\n\n"
        for candidate, count in vote_counts.items():
            results_text += f"{candidate}: {count} vote(s)\n"
        results_text += f"Skipped: {skip_votes} vote(s)\n"
        results_text += f"Total Valid Votes: {total_votes}"
        
        tk.Label(self.action_frame, text=results_text, 
                bg=self.colors['secondary'], fg=self.colors['text'],
                font=('Arial', 12), justify=tk.LEFT).pack(pady=20)
        
        # Determine if someone should be eliminated
        if not vote_counts:
            messagebox.showinfo("Vote Result", "No one received any votes. Round continues.")
            self.killer_survival_rounds += 1
        else:
            # Find the player with most votes
            most_voted = max(vote_counts.items(), key=lambda x: x[1])
            most_voted_player = next(p for p in self.players if p.name == most_voted[0])
            
            # Check if they got 50% or more of total alive players
            alive_count = len([p for p in self.players if p.status == PlayerStatus.ALIVE])
            required_votes = alive_count // 2 + 1  # More than 50%
            
            if most_voted[1] >= required_votes:
                # Eliminate the most voted player
                if most_voted_player.role == Role.KILLER:
                    most_voted_player.status = PlayerStatus.DISMISSED
                    
                    # Check if all killers are eliminated
                    remaining_killers = len([p for p in self.players if p.role == Role.KILLER and p.status == PlayerStatus.ALIVE])
                    
                    if remaining_killers == 0:
                        messagebox.showinfo("Vote Result", 
                                          f"🎉 {most_voted_player.name} was voted out and was a KILLER!\nAll killers eliminated - Civilians win!")
                        self.end_game("Civilians win! All killers eliminated by vote!")
                        return
                    else:
                        messagebox.showinfo("Vote Result", 
                                          f"🎉 {most_voted_player.name} was voted out and was a KILLER!\nBut there are still killers remaining...")
                else:
                    most_voted_player.status = PlayerStatus.DISMISSED
                    messagebox.showinfo("Vote Result", 
                                      f"❌ {most_voted_player.name} was voted out but was innocent!\nGame continues...")
                
                self.killer_survival_rounds += 1
            else:
                messagebox.showinfo("Vote Result", 
                                  f"{most_voted_player.name} got the most votes ({most_voted[1]}) but didn't reach 50% threshold ({required_votes} needed).\nNo elimination.")
                self.killer_survival_rounds += 1
        
        self.update_player_display()
        
        # Check win conditions
        if self.killer_survival_rounds >= 3:
            self.end_game("Killers win! Survived 3 rounds!")
            return
            
        alive_killers = len([p for p in self.players if p.role == Role.KILLER and p.status == PlayerStatus.ALIVE])
        alive_others = len([p for p in self.players if p.role != Role.KILLER and p.status == PlayerStatus.ALIVE])
        
        if alive_killers == 0:
            self.end_game("Civilians win! All killers eliminated!")
            return
        elif alive_killers >= alive_others:
            self.end_game("Killers win! They equal or outnumber the civilians!")
            return
            
        # Continue to next round
        self.round_number += 1
        self.target_killed = None
        self.doctor_saved = None
        self.police_guess = None
        self.police_correct = False
        
        # Small delay before next round
        self.root.after(3000, self.start_killer_turn)
        
    def end_game(self, message):
        self.current_phase = GamePhase.GAME_OVER
        self.update_info_display()
        self.clear_action_frame()
        
        # Cancel any running timers
        if self.discussion_timer:
            self.root.after_cancel(self.discussion_timer)
        self.timer_label.pack_forget()
        
        ttk.Label(self.action_frame, text="🎯 GAME OVER", 
                 style='Title.TLabel').pack(pady=20)
        
        ttk.Label(self.action_frame, text=message, 
                 background=self.colors['secondary'], foreground=self.colors['highlight'],
                 font=('Arial', 14, 'bold')).pack(pady=20)
        
        # Reveal roles
        role_text = "ROLE REVEALS:\n\n"
        for player in self.players:
            role_emoji = {"Killer": "🔪", "Doctor": "🏥", "Police": "👮", "Civilian": "👤"}
            status_text = ""
            if player.status == PlayerStatus.DEAD:
                status_text = " (DEAD)"
            elif player.status == PlayerStatus.DISMISSED:
                status_text = " (DISMISSED)"
            role_text += f"{role_emoji[player.role.value]} {player.name}: {player.role.value}{status_text}\n"
        
        role_label = tk.Label(self.action_frame, text=role_text, 
                             bg=self.colors['secondary'], fg=self.colors['text'],
                             font=('Arial', 11), justify=tk.LEFT)
        role_label.pack(pady=20)
        
        ttk.Button(self.action_frame, text="New Game", 
                  command=self.reset_game, 
                  style='Custom.TButton').pack(pady=20)
        
    def reset_game(self):
        # Cancel any running timers
        if self.discussion_timer:
            self.root.after_cancel(self.discussion_timer)
        self.timer_label.pack_forget()
        
        # Reset all game variables
        self.players = []
        self.current_phase = GamePhase.SETUP
        self.round_number = 0
        self.killer_survival_rounds = 0
        self.target_killed = None
        self.doctor_saved = None
        self.police_guess = None
        self.police_correct = False
        self.votes = {}
        self.individual_votes = {}
        self.current_voter_index = 0
        self.keywords_assigned = False
        self.discussion_time_left = 60
        self.discussion_timer = None
        
        self.update_info_display()
        self.show_setup_screen()
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = KillerHasinaGame()
    game.run()