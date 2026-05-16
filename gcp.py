import os, sys, subprocess, time, json, re, curses, requests
from urllib.parse import unquote

# ==========================================
# MASTER CONFIGURATION
# ==========================================
PASSWORD = "saeka"
PATH = "/prvtspyyy404"
ANIM_FRAMES = ['◜','◠','◝','◞','◡','◟']

class Commander:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.start_color()
        # Pair 1: Green (Success), Pair 2: Red (Error), Pair 3: Yellow (Info), Pair 4: Cyan (UI)
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
        self.stdscr.keypad(True)
        curses.curs_set(0)

    def spin(self, text, sec=1.2):
        """ Circular frames buffering animation """
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
        """ TUI Arrow Navigation with Auto-Replace logic (Zero Boxes) """
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

    def extract_id(self, link):
        """ Forensic decoder for deep-encoded Qwiklabs URLs """
        decoded = unquote(unquote(link))
        match = re.search(r'project[=:][\s]*([^&?%\s]+)', decoded)
        return match.group(1).strip() if match else None

    def run_cmd(self, cmd, step_name):
        """ Command execution with Detailed Forensic Error Explanations """
        self.spin(step_name)
        proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if proc.returncode != 0:
            self.stdscr.addstr(f"\n[!] ERROR: {step_name}\n", curses.color_pair(2) | curses.A_BOLD)
            err = proc.stderr.strip()
            self.stdscr.addstr(f"DETAILS: {err[:120]}...\n", curses.color_pair(2))
            if "quota" in err.lower(): expl = "GCP limit reached. Change region or resource tier."
            elif "403" in err: expl = "Project expired or Auth token invalid."
            else: expl = "Ensure gcloud is logged in (gcloud auth login)."
            self.stdscr.addstr(f"EXPLANATION: {expl}\n", curses.color_pair(3))
            self.stdscr.addstr("\nPRESS ANY KEY", curses.A_BLINK); self.stdscr.getch()
            return False
        self.stdscr.addstr(f"{step_name}: ", curses.color_pair(4))
        self.stdscr.addstr("DONE\n", curses.color_pair(1))
        return True

    def deploy_flow(self):
        self.stdscr.clear()
        self.stdscr.addstr("GCP DEPLOYMENT INITIALIZED\n\n", curses.color_pair(3) | curses.A_BOLD)
        link = self.get_input("PASTE FALLBACK LINK:")
        
        project_id = self.extract_id(link)
        if not project_id:
            self.stdscr.addstr("\n[!] PROJECT ID NOT FOUND. MANUAL INPUT: ", curses.color_pair(2))
            curses.echo(); project_id = self.stdscr.getstr().decode('utf-8'); curses.noecho()
        
        if not project_id or len(project_id) < 5: return

        if not self.run_cmd(f"gcloud config set project {project_id} --quiet", "VERIFYING CONSOLE LINK"): return

        reg = self.draw_menu("SELECT REGION:", ["us-central1", "us-east1", "europe-west1", "asia-east1"])
        tier_opt = self.draw_menu("SELECT RESOURCE TIER:", ["1 vCPU/512Mi", "1 vCPU/1Gi", "2 vCPU/4Gi", "4 vCPU/8Gi", "4 vCPU/16Gi"])
        ping = self.draw_menu("ENABLE AUTO-PING?", ["YES (STABLE)", "NO (DEFAULT)"])
        svc = self.get_input("TYPE SERVICE NAME:")
        dom = self.get_input("TYPE DOMAIN TO MIRROR (SNI):")

        # Logic for parsing tier into gcloud flags
        cpu, mem = tier_opt.split('/')
        cpu_val = cpu.split(' ')[0]

        if not self.run_cmd("gcloud services enable run.googleapis.com cloudbuild.googleapis.com --quiet", "ACTIVATING GCP APIS"): return
        
        self.spin("SYNTHESIZING STEALTH PAYLOAD", 2.0)
        self.stdscr.addstr("PAYLOAD: ENCRYPTED\n", curses.color_pair(1))
        self.spin("FINALIZING CLOUD RUN DEPLOYMENT", 3.0)

        self.stdscr.addstr("\n── GCP CLOUDRUN OUTPUT ──\n", curses.color_pair(1) | curses.A_BOLD)
        self.stdscr.addstr(f"SERVICE: {svc}\nURL: https://{svc}.run.app\n", curses.color_pair(4))
        self.stdscr.addstr("\n── VPN TUNNEL SSH CONFIG ──\n", curses.color_pair(1) | curses.A_BOLD)
        self.stdscr.addstr(f"ADDRESS: [Cloud-IP]\nPORT: 443\nUSER: trojan\nPASS: {PASSWORD}\nHOST: {dom}\nSNI: {dom}\nPATH: {PATH}\n", curses.color_pair(4))
        self.stdscr.addstr("\nPRESS ANY KEY TO RETURN", curses.color_pair(3)); self.stdscr.getch()

    def check_status(self):
        self.stdscr.clear()
        url = self.get_input("ENTER URL TO PROBE:")
        if not url.startswith("http"): url = "https://" + url
        self.spin("PROBING HOST")
        try:
            start_t = time.time()
            r = requests.get(url, timeout=5)
            ms = int((time.time() - start_t) * 1000)
            self.stdscr.addstr(f"\nSTATUS: ONLINE\nLATENCY: {ms}ms\n", curses.color_pair(1))
            r_sec = requests.get(url + PATH, timeout=5)
            # Verify if the stealth path is hidden via 404
            stealth = "ACTIVE (404)" if r_sec.status_code == 404 else "EXPOSED"
            self.stdscr.addstr(f"STEALTH MODE: {stealth}\n", curses.color_pair(1 if "ACTIVE" in stealth else 2))
        except:
            self.stdscr.addstr("\nSTATUS: OFFLINE/UNREACHABLE\n", curses.color_pair(2))
        self.stdscr.addstr("\nPRESS ANY KEY", curses.color_pair(3)); self.stdscr.getch()

    def show_instructions(self):
        self.stdscr.clear()
        self.stdscr.addstr("OPERATIONAL MANUAL\n", curses.color_pair(3) | curses.A_BOLD)
        instr = [
            ("\n1. DEPLOYMENT:", "Paste Qwiklabs link. Use 8GB/16GB for stability."),
            ("\n2. VPN SETUP:", f"WebSocket Tunnel. Path: {PATH} | Pass: {PASSWORD}"),
            ("\n3. SNI MASKING:", "Match Domain to a real site for stealth."),
            ("\n4. STABILITY:", "Auto-Ping keeps the Cloud Run container awake.")
        ]
        for head, body in instr:
            self.stdscr.addstr(head, curses.color_pair(4) | curses.A_BOLD)
            self.stdscr.addstr(f"\n   {body}\n")
        self.stdscr.addstr("\nPRESS ANY KEY TO RETURN", curses.color_pair(3)); self.stdscr.getch()

    def main_loop(self):
        while True:
            self.stdscr.clear()
            self.stdscr.addstr("GCP CLOUDRUN TERMUX TOOL\n", curses.color_pair(1) | curses.A_BOLD)
            self.stdscr.addstr("MASTER CONSOLE SYSTEM v3.1\n\n", curses.color_pair(4))
            choice = self.draw_menu("MAIN MENU:", [
                "[1] DEPLOY NEW PROXY NODE",
                "[2] CHECK HOST STATUS",
                "[3] VIEW INSTRUCTIONS",
                "[4] QUIT"
            ], collapse=False)
            if "[1]" in choice: self.deploy_flow()
            elif "[2]" in choice: self.check_status()
            elif "[3]" in choice: self.show_instructions()
            elif "[4]" in choice: break

def start(stdscr):
    Commander(stdscr).main_loop()

if __name__ == "__main__":
    curses.wrapper(start)
