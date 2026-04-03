import tkinter as tk
import random
import base64
import io
from PIL import Image, ImageTk

# ─────────────────────────────────────────────
#  COLOURS
# ─────────────────────────────────────────────
C = {
    "bg":        "#09090f",
    "panel":     "#111118",
    "panel2":    "#16161f",
    "border":    "#1e1e30",
    "red":       "#E8192C",
    "red_dark":  "#b01020",
    "gold":      "#F0B429",
    "gold_dk":   "#c8920f",
    "text":      "#e8e8f0",
    "muted":     "#6a6a8a",
    "hover":     "#1c1c28",
    "sel_bg":    "#1f0f12",
}

# ─────────────────────────────────────────────
#  HEROES
# ─────────────────────────────────────────────
HEROES = [
    ("Hulk",             "Super Strength",      "💚"),
    ("Iron Man",         "Genius Intelligence", "🤖"),
    ("Spider-Man",       "Agility",              "🕷"),
    ("Thor",             "God Power",           "⚡"),
    ("Doctor Strange",   "Magic",               "🌀"),
    ("Black Panther",    "Stealth",             "🐾"),
    ("Hawkeye",          "Archery",             "🎯"),
    ("Black Widow",      "Combat Skills",       "🕸"),
    ("Captain America", "Leadership",           "🛡"),
    ("Vision",           "Technology",          "💜"),
    ("Scarlet Witch",    "Chaos Magic",         "🔮"),
    ("Quicksilver",      "Speed",               "💨"),
    ("Falcon",           "Flight",              "🦅"),
    ("Luke Cage",        "Durability",          "💪"),
    ("Wolverine",        "Regeneration",        "⚔"),
    ("Ant-Man",          "Size Control",        "🐜"),
    ("Captain Marvel",   "Energy Blast",        "⭐"),
    ("Shang-Chi",        "Martial Arts",        "🥋"),
    ("Loki",             "Mind Tricks",         "🐍"),
    ("Professor X",      "Telepathy",           "🧠"),
]

BASE_Q = [
    "How do you react in danger?",
    "Pick a quality that defines you:",
    "What motivates you most?",
    "Your role in a team?",
    "How do you solve problems?",
    "Choose a weapon:",
    "Your mindset in life?",
    "How do people describe you?",
    "What do you value most?",
    "Your strategy in conflict?",
    "How do you handle stress?",
    "Pick your ideal environment:",
]

OPT_POOL = [
    ["Fight head-on",  "Think logically", "Stay hidden",  "Lead others",  "Manipulate"],
    ["Strength",       "Intelligence",    "Speed",        "Magic",        "Skill"],
    ["Power",          "Knowledge",       "Freedom",      "Justice",      "Control"],
    ["Leader",          "Solo player",     "Support",      "Planner",      "Trickster"],
    ["Direct action",  "Smart thinking",  "Creative way", "Teamwork",     "Deception"],
    ["Hammer",          "Suit",            "Magic",        "Shield",       "Mind"],
    ["Aggressive",      "Calm",            "Focused",      "Creative",      "Strategic"],
    ["Strong",          "Smart",           "Fast",         "Mysterious",   "Dangerous"],
    ["Honor",           "Brains",          "Speed",        "Power",        "Influence"],
    ["Attack",          "Defend",          "Outsmart",     "Escape",       "Control"],
    ["Explode",         "Analyze",         "Adapt",        "Stay calm",    "Dominate"],
    ["Battlefield",     "Lab",             "Space",        "City",         "Unknown"],
]


def make_bank():
    return [{"q": random.choice(BASE_Q),
             "options": random.choice(OPT_POOL),
             "scores": random.sample(range(20), 5)}
            for _ in range(120)]


# ─────────────────────────────────────────────
#  ANIMATED BACKGROUND
# ─────────────────────────────────────────────
class StarField(tk.Canvas):
    def __init__(self, parent, **kw):
        super().__init__(parent, bg=C["bg"], highlightthickness=0, **kw)
        self._particles = []
        self._dots = []
        self._job = None
        self.bind("<Configure>", self._on_size)

    def _on_size(self, e):
        self._make_dots(e.width, e.height)
        self._make_particles(e.width, e.height)
        if not self._job:
            self._tick()

    def _make_dots(self, w, h):
        for item in self._dots:
            self.delete(item)
        self._dots = []
        for y in range(0, h + 28, 28):
            for x in range(0, w + 28, 28):
                item = self.create_oval(
                    x-1.5, y-1.5, x+1.5, y+1.5,
                    fill="#18182a"
                )
                self._dots.append(item)

    def _make_particles(self, w, h):
        self._particles = [{
            "x": random.uniform(0, w),
            "y": random.uniform(0, h),
            "vx": random.uniform(-0.2, 0.2),
            "vy": random.uniform(-0.45, -0.1),
            "r": random.uniform(1, 2.5),
            "col": random.choice([C["red"], C["gold"]]),
            "id": None,
        } for _ in range(22)]

    def _tick(self):
        w, h = self.winfo_width(), self.winfo_height()
        if w < 2:
            self._job = self.after(50, self._tick)
            return

        for p in self._particles:
            if p["id"]:
                self.delete(p["id"])

            p["x"] += p["vx"]
            p["y"] += p["vy"]

            if p["y"] < -10:
                p["y"] = h + 10
                p["x"] = random.uniform(0, w)

            if p["x"] < -10:
                p["x"] = w + 10

            if p["x"] > w + 10:
                p["x"] = -10

            r = p["r"]

            p["id"] = self.create_oval(
                p["x"]-r, p["y"]-r,
                p["x"]+r, p["y"]+r,
                fill=p["col"]
            )

        self._job = self.after(40, self._tick)

    def stop(self):
        if self._job:
            self.after_cancel(self._job)
            self._job = None


# ─────────────────────────────────────────────
#  WIDGET HELPERS
# ─────────────────────────────────────────────
def _light(col, n=30):
    h = col.lstrip("#")
    r,g,b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    return f"#{min(255,r+n):02x}{min(255,g+n):02x}{min(255,b+n):02x}"


def btn(parent, text, cmd, bg=C["red"], fg="white",
        size=11, width=30, pady=10):
    b = tk.Label(parent, text=text, font=("Helvetica", size, "bold"),
                 fg=fg, bg=bg, padx=20, pady=pady, width=width, cursor="hand2")
    b.bind("<Enter>",    lambda e: b.config(bg=_light(bg)))
    b.bind("<Leave>",    lambda e: b.config(bg=bg))
    b.bind("<Button-1>", lambda e: cmd())
    return b


def rule(parent, color=C["border"]):
    tk.Frame(parent, bg=color, height=1).pack(fill="x", pady=10)


def lbl(parent, text, size=10, color=C["text"], bold=False, **kw):
    w = "bold" if bold else "normal"
    return tk.Label(parent, text=text,
                    font=("Helvetica", size, w),
                    fg=color, bg=C["panel"], **kw)


# ─────────────────────────────────────────────
#  MAIN APP
# ─────────────────────────────────────────────
class App(tk.Tk):
    W, H = 680, 580

    def __init__(self):
        super().__init__()
        self.title("Which Marvel Superhero Are You?")
        self.geometry(f"{self.W}x{self.H}")
        self.resizable(False, False)
        self.configure(bg=C["bg"])
        self.update_idletasks()
        ox = (self.winfo_screenwidth()  - self.W) // 2
        oy = (self.winfo_screenheight() - self.H) // 2
        self.geometry(f"{self.W}x{self.H}+{ox}+{oy}")

        # Background
        self._stars = StarField(self)
        self._stars.place(x=0, y=0, relwidth=1, relheight=1)

        # Corner decorations
        self._deco = tk.Canvas(self, bg=C["bg"], highlightthickness=0)
        self._deco.place(x=0, y=0, relwidth=1, relheight=1)
        self._corners()

        # Card
        self._card = tk.Frame(self, bg=C["panel"],
                              highlightbackground=C["border"],
                              highlightthickness=1)
        self._card.place(relx=0.5, rely=0.5, anchor="center",
                         width=560, height=520)

        self._accent = tk.Frame(self._card, bg=C["red"], height=3)
        self._accent.pack(fill="x", side="top")

        self._body = tk.Frame(self._card, bg=C["panel"])
        self._body.pack(fill="both", expand=True, padx=36, pady=22)

        # State
        self._bank      = make_bank()
        self._scores    = [0]*20
        self._qidx      = 0
        self._questions = []
        self._picked    = -1          
        self._opt_rows  = []
        self._photos    = {}

        self._screen_start()

    def _corners(self):
        self._deco.delete("all")
        w,h,s,t = self.W, self.H, 28, 2
        col = C["red"]
        self._deco.create_line(12,12+s, 12,12, 12+s,12, width=t, fill=col)
        self._deco.create_line(w-12-s,12, w-12,12, w-12,12+s, width=t, fill=col)
        self._deco.create_line(12,h-12-s, 12,h-12, 12+s,h-12, width=t, fill=col)
        self._deco.create_line(w-12-s,h-12, w-12,h-12, w-12,h-12-s, width=t, fill=col)

    def _accent_col(self, col): self._accent.config(bg=col)

    def _clear(self):
        for w in self._body.winfo_children():
            w.destroy()

    def _shield(self, parent):
        c = tk.Canvas(parent, width=78, height=78,
                      bg=C["panel"], highlightthickness=0)
        cx, cy = 39, 39
        for i, col in enumerate(["#E8192C","#cccccc","#E8192C","#cccccc"]):
            r = 36 - i*8
            c.create_oval(cx-r,cy-r,cx+r,cy+r, fill=col, outline=C["panel"], width=2)
        c.create_text(cx, cy+1, text="★", font=("Helvetica",12,"bold"), fill="white")
        return c

    def _screen_start(self):
        self._clear()
        self._accent_col(C["red"])
        b = self._body
        tk.Label(b, text=" MARVEL ", font=("Helvetica",14,"bold"),
                 fg="white", bg=C["red"], padx=14, pady=3).pack(pady=(2,2))
        lbl(b,"WHICH SUPERHERO ARE YOU?", 19, "white", bold=True,
            wraplength=460).pack()
        lbl(b,"· PERSONALITY QUIZ  ·  5 QUESTIONS ·", 8, C["muted"]).pack()
        rule(b)
        self._shield(b).pack(pady=4)
        rule(b)
        btn(b, "⚡  BEGIN YOUR ORIGIN STORY", self._screen_warning,
            size=11, width=32, pady=12).pack(pady=(2,0))
        btn(b, "🚪  EXIT THE LAB", self.destroy,
            bg=C["panel2"], fg=C["muted"], size=10,
            width=32, pady=9).pack(pady=(10,0))
        lbl(b,"UNCOVER YOUR TRUE POWERS", 7, C["muted"]).pack(pady=(8,0))

    def _screen_warning(self):
        self._clear()
        self._accent_col(C["gold"])
        b = self._body
        lbl(b,"⚡", 38, C["gold"]).pack(pady=(6,2))
        lbl(b,"YOU ARE ABOUT TO BECOME A SUPERHERO",
            13, "white", bold=True, wraplength=440).pack()
        lbl(b,'"With great power comes great responsibility"',
            9, C["muted"]).pack(pady=(4,0))
        rule(b)
        lbl(b,"ARE YOU READY TO ACCEPT THIS FATE?", 8, C["muted"]).pack(pady=(0,12))
        btn(b,"✔  I AM READY", self._on_ready,
            size=11, width=32, pady=12).pack()
        btn(b,"✖  I CAN'T TAKE THE RESPONSIBILITY",
            self._screen_villain,
            bg=C["panel2"], fg=C["muted"], size=10,
            width=32, pady=10).pack(pady=(10,0))

    def _on_ready(self):
        self._dialog("⚡",
            '"With great power comes\ngreat responsibility"',
            "— Uncle Ben", self._start_quiz)

    def _screen_villain(self):
        self._clear()
        self._accent_col(C["red_dark"])
        b = self._body
        lbl(b,"😈", 42).pack(pady=(8,2))
        lbl(b,"THEN YOU ARE DEFINITELY", 11, C["muted"]).pack()
        lbl(b,"A SUPERVILLAIN", 22, C["red"], bold=True).pack(pady=(0,4))
        rule(b)
        lbl(b,"DO YOU EMBRACE THE DARKNESS?", 8, C["muted"]).pack(pady=(0,12))
        btn(b,"😈  YES — EMBRACE CHAOS",
            self.destroy,
            size=11, width=32, pady=12).pack()
        btn(b,"← NO — TAKE ME BACK",
            self._not_worthy,
            bg=C["panel2"], fg=C["muted"], size=10,
            width=32, pady=10).pack(pady=(10,0))

    def _not_worthy(self):
        self._dialog("💫", "You are not worthy.", "— Odin", self.destroy)

    def _start_quiz(self):
        self._bank      = make_bank()
        self._scores    = [0]*20
        self._qidx      = 0
        self._questions = random.sample(self._bank, 5)
        self._show_q()

    def _show_q(self):
        if self._qidx >= 5:
            self._screen_result()
            return
        self._clear()
        self._accent_col(C["red"])
        self._picked = -1
        self._opt_rows = []
        b = self._body
        q = self._questions[self._qidx]
        pr = tk.Frame(b, bg=C["panel"])
        pr.pack(fill="x", pady=(0,4))
        lbl(pr, f"QUESTION {self._qidx+1} OF 5",
            7, C["muted"], bold=True).pack(side="left")
        lbl(pr, f"{self._qidx*20}% COMPLETE",
            7, C["muted"], bold=True).pack(side="right")
        bar_bg = tk.Frame(b, bg=C["border"], height=4)
        bar_bg.pack(fill="x", pady=(0,14))
        bar_bg.update_idletasks()
        fw = int(bar_bg.winfo_width() * self._qidx / 5)
        if fw > 0:
            tk.Frame(bar_bg, bg=C["gold"], width=fw, height=4).place(x=0,y=0)
        qrow = tk.Frame(b, bg=C["panel"])
        qrow.pack(fill="x", pady=(0,10))
        lbl(qrow, f"{self._qidx+1:02d}", 48, C["border"], bold=True
            ).pack(side="right", padx=(0,0))
        lbl(qrow, q["q"], 14, "white", bold=True,
            wraplength=360, justify="left", anchor="w"
            ).pack(side="left", fill="x", expand=True)
        opt_frame = tk.Frame(b, bg=C["panel"])
        opt_frame.pack(fill="x")
        for i, txt in enumerate(q["options"]):
            self._make_opt(opt_frame, i, "ABCDE"[i], txt)
        rule(b)
        label = "NEXT QUESTION  →" if self._qidx < 4 else "REVEAL MY HERO  ⚡"
        btn(b, label, self._next_q, size=11, width=32, pady=11).pack()

    def _make_opt(self, parent, idx, letter, text):
        row = tk.Frame(parent, bg=C["panel2"],
                       highlightbackground=C["border"],
                       highlightthickness=1, cursor="hand2")
        row.pack(fill="x", pady=2)
        self._opt_rows.append(row)
        bul = tk.Label(row, text=letter, font=("Helvetica",10,"bold"),
                       fg=C["muted"], bg=C["border"], width=3, pady=7)
        bul.pack(side="left")
        txt_lbl = tk.Label(row, text=text, font=("Helvetica",10,"bold"),
                           fg=C["text"], bg=C["panel2"], anchor="w", padx=12)
        txt_lbl.pack(side="left", fill="x", expand=True)
        def select(i=idx):
            self._picked = i
            for j, fr in enumerate(self._opt_rows):
                kids = fr.winfo_children()
                fr.config(bg=C["panel2"], highlightbackground=C["border"])
                if kids: kids[0].config(bg=C["border"], fg=C["muted"])
                if len(kids)>1: kids[1].config(bg=C["panel2"], fg=C["text"])
            row.config(bg=C["sel_bg"], highlightbackground=C["red"])
            bul.config(bg=C["red"], fg="white")
            txt_lbl.config(bg=C["sel_bg"], fg="white")
        def enter(e, i=idx):
            if self._picked != i:
                row.config(bg=C["hover"]); txt_lbl.config(bg=C["hover"])
        def leave(e, i=idx):
            if self._picked != i:
                row.config(bg=C["panel2"]); txt_lbl.config(bg=C["panel2"])
        for w in (row, bul, txt_lbl):
            w.bind("<Button-1>", lambda e, s=select: s())
            w.bind("<Enter>", enter)
            w.bind("<Leave>", leave)

    def _next_q(self):
        if self._picked == -1:
            self._dialog("⚠️", "You must choose your path,\nHero.", "", None)
            return
        q = self._questions[self._qidx]
        hero_idx = q["scores"][self._picked]
        self._scores[hero_idx] += 1
        if self._qidx >= 4:
            self.after(100, self._screen_result)
        else:
            self._qidx += 1
            self._show_q()

    def _screen_result(self):
        if hasattr(self, '_stars'):
            self._stars.stop()
        self._clear()
        self._accent_col(C["gold"])
        b = self._body
        max_s = max(self._scores)
        winners = [i for i,s in enumerate(self._scores) if s == max_s]
        chosen = random.choice(winners)
        name, power, icon = HEROES[chosen]
        lbl(b,"· THE VERDICT IS IN ·", 8, C["muted"]).pack(pady=(2,6))
        img_b64 = HERO_IMAGES.get(name)
        if img_b64 and len(img_b64) > 50:
            try:
                raw = base64.b64decode(img_b64)
                pil = Image.open(io.BytesIO(raw)).resize((138,163), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(pil)
                self._photos[name] = photo
                tk.Label(b, image=photo, bg=C["panel"],
                         highlightbackground=C["gold"], highlightthickness=2).pack()
            except Exception:
                lbl(b, icon, 48).pack()
        else:
            lbl(b, icon, 48).pack()
        lbl(b,"YOU ARE", 8, C["muted"]).pack(pady=(6,0))
        lbl(b, name.upper(), 24, C["gold"], bold=True, wraplength=460).pack(pady=(2,0))
        pw = tk.Frame(b, bg=C["panel"])
        pw.pack(pady=(4,0))
        tk.Label(pw, text=f"  {power.upper()}  ", font=("Helvetica",9,"bold"), 
                 fg="white", bg=C["red"], padx=8, pady=3).pack()
        rule(b)
        lbl(b,"THE UNIVERSE HAS SPOKEN  ·  YOUR DESTINY IS SET", 7, C["muted"]).pack(pady=(0,8))
        btn(b,"↺  SEARCH FOR NEW POWERS", self._start_quiz,
            bg=C["gold_dk"], fg=C["bg"], size=11, width=32, pady=10).pack()
        btn(b,"⌂  RETURN TO BASE", self._screen_start,
            bg=C["panel2"], fg=C["muted"], size=10, width=32, pady=9).pack(pady=(8,0))

    def _dialog(self, icon, msg, sub, callback):
        ov = tk.Frame(self, bg=C["bg"])
        ov.place(x=0, y=0, relwidth=1, relheight=1)
        box = tk.Frame(ov, bg=C["panel"], highlightbackground=C["gold"], highlightthickness=1)
        box.place(relx=0.5, rely=0.5, anchor="center", width=380, height=245)
        tk.Frame(box, bg=C["gold"], height=2).pack(fill="x")
        inner = tk.Frame(box, bg=C["panel"])
        inner.pack(fill="both", expand=True, padx=28, pady=18)
        lbl(inner, icon, 34).pack(pady=(0,6))
        lbl(inner, msg, 11, "white", bold=True, justify="center", wraplength=300).pack()
        if sub: lbl(inner, sub, 8, C["muted"]).pack(pady=(4,0))
        def close():
            ov.destroy()
            if callback: callback()
        btn(inner,"GOT IT", close, size=10, width=16, pady=9).pack(pady=(14,0))

HERO_IMAGES = { 'Hulk': '', 'Iron Man': '', 'Spider-Man': '', 'Thor': '', 'Doctor Strange': '', 'Black Panther': '', 'Hawkeye': '', 'Black Widow': '', 'Captain America': '', 'Vision': '', 'Scarlet Witch': '', 'Quicksilver': '', 'Falcon': '', 'Luke Cage': '', 'Wolverine': '', 'Ant-Man': '', 'Captain Marvel': '', 'Shang-Chi': '', 'Loki': '', 'Professor X': ''}

if __name__ == "__main__":
    app = App()
    app.mainloop()