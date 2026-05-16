import os, sys, subprocess, time, json, re, curses, requests
from urllib.parse import unquote

# MASTER CONFIG
PASSWORD = "saeka"
PATH = "/prvtspyyy404"
ANIM_FRAMES = ['◜','◠','◝','◞','◡','◟']

class Commander:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.start_color()
        # Pair 1: Success (Green), Pair 2: Error (Red), Pair 3: Info (Yellow), Pair 4: UI (Cyan)
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
        self.stdscr.keypad(True)
        curses.curs_set(0)

    def spin(self, text, sec=1.2):
        """ Circular frames animation logic """
        end = time.time() + sec; i = 0
        while time.time() < end:
            y, _ = self.stdscr.getyx()
            self.stdscr.move(y, 0); self.stdscr.clrtoeol()
            self.stdscr.addstr(f"{text} ", curses.color_pair(4))
            self.stdscr.addstr(f"{ANIM_FRAMES[i % len(ANIM_FRAMES)]}", curses.color_pair(3))
            self.stdscr.refresh()
            time.sleep(0.1); i += 1
        self.stdscr.move(y, 0); self.stdscr.clrtoeol()

    def draw_menu(self, title, options, collapse=True):
        """ Arrows + Enter Navigation with Auto-Replace logic (No Boxes) """
        curr = 0
        start_y, _ = self.stdscr.getyx()
        while True:
            for idx, opt in enumerate(options):
                self.stdscr.move(start_y + idx + 1, 0); self.stdscr.clrtoeol()
                if idx == curr:
                    self.stdscr.addstr(f"> {opt}", curses.color_pair(4) | curses.A_REVERSE)
                else:
                    self.stdscr.addstr(f"  {opt}", curses.color_pair(4))
            self.stdscr.move(start_y, 0); self.stdscr.clrtoeol()
            self.stdscr.addstr(title, curses.color_pair(3) | curses.A_BOLD)
            self.stdscr.refresh()
            
            key = self.stdscr.getch()
            if key == curses.KEY_UP and curr > 0: curr -= 1
            elif key == curses.KEY_DOWN and curr < len(options)-1: curr += 1
            elif key in [10, 13]:
                if collapse:
                    for i in range(len(options) + 1):
                        self.stdscr.move(start_y + i, 0); self.stdscr.clrtoeol()
                    self.stdscr.addstr(start_y, 0, f"{title} ", curses.color_pair(3))
                    self.stdscr.addstr(f"{options[curr]}\n", curses.color_pair(1))
                return options[curr]

    def get_input(self, prompt):
        self.stdscr.addstr(prompt + " ", curses.color_pair(4))
        self.stdscr.refresh()
        curses.echo()
        val = self.stdscr.getstr().decode('utf-8')
        curses.noecho()
        return val

    def run_cmd(self, cmd, step_name):
        """ Command execution with detailed error explanation """
        self.spin(step_name)
        proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if proc.returncode != 0:
            self.stdscr.addstr(f"\n[!] ERROR: {step_name}\n", curses.color_pair(2) | curses.A_BOLD)
            err = proc.stderr.strip()
            self.stdscr.addstr(f"DETAILS: {err[:120]}...\n", curses.color_pair(2))
            if "quota" in err.lower(): expl = "GCP Project reached limits. Switch regions."
            elif "403" in err: expl = "Console link expired or gcloud not logged in."
            else: expl = "Ensure gcloud is installed and project ID is correct."
            self.stdscr.addstr(f"EXPLANATION: {expl}\n", curses.color_pair(3))
            self.stdscr.addstr("\nPRESS ANY KEY", curses.A_BLINK); self.stdscr.getch()
            return False
        self.stdscr.addstr(f"{step_name}: ", curses.color_pair(4))
        self.stdscr.addstr("DONE\n", curses.color_pair(1))
        return True

    def extract_id(self, link):
        """ Advanced decoder for complex Qwiklabs URLs """
        decoded = unquote(unquote(link))
        match = re.search(r'project[=:][\s]*([^&?%\s]+)', decoded)
        return match.group(1).strip() if match else None
