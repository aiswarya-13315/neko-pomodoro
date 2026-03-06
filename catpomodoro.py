import tkinter as tk
from tkinter import messagebox
import math

# paletteee
C = {
    "bg":        "#ffb7c5",
    "bg2":       "#ffd6e0",
    "card":      "#fff0f5",
    "border":    "#ff85a1",
    "black":     "#1a1a2e",
    "accent":    "#ff4d79",
    "accent2":   "#ff85a1",
    "text":      "#3d0015",
    "sub":       "#cc3366",
    "white":     "#fff8fa",
    "green":     "#a8e6cf",
    "yellow":    "#ffe8a3",
    "shadow":    "#e8809a",
    "nose":      "#ff9eb5",
    "cheek":     "#ffccd5",
}

WORK_TIME   = 25 * 60
SHORT_BREAK =  5 * 60
LONG_BREAK  = 15 * 60

# pixel cat sprites
# X = black body, n = pink nose, e = eye, c = cheek blush, w = white belly, . = empty

CAT_SITTING = """\
....................
....XX......XX......
...XXXX....XXXX.....
..XXXXXXXXXXXXXXXXX.
..XXeXXXXXXXXXeXXX.
..XXeXXXXXXXXXeXXX.
..XXXXXXnXXXXXXXXX.
..XXXXXXXXXXXXXXXXXX
...XXXXXXXXXXXXXXXXX
....XXXXXXXXXXXXXww.
....XXXXXXXXXXXXXww.
....XXXXXXXXXXXXwww.
....XX.cXXXXc.XXXXX.
....XX..XXXXX..XXXX.
....XXXXXXXXXXXXXXXXX
.....XXXXXXXXXXXXXXX.
....XX..........XX..
....XXXXXXXXXXXXXXXXXXXX
"""

CAT_SLEEPING = """\
....................
....................
....XX......XX......
...XXXX....XXXX.....
..XXXXXXXXXXXXXXXXX.
..XX-XXXXXXXXXXX-XX.
..XX-XXXXXXXXXXX-XX.
..XXXXXXnXXXXXXXXXX.
..XXXXXXXXXXXXXXXXXXX
...XXXXXXXXXXXXXXXXX.
....XXXXXXXXXXXXXwww
....XXXXXXXXXXXXwwww
....XX.cXXXXc.XXXXXX
....XX..XXXXX..XXXXX
.....XXXXXXXXXXXXXXX.
....XXXXXXXXXXXXXXXXX
....XX..........XXXX
....XXXXXXXXXXXXXXXX
"""

CAT_HAPPY = """\
....................
....XX......XX......
...XXXX....XXXX.....
..XXXXXXXXXXXXXXXXX.
..XXuXXXXXXXXXuXXX.
..XXuXXXXXXXXXuXXX.
..XXXXXXwXXXXXXXXX.
..XXXXXXXXXXXXXXXXXXX
...XXXXXXXXXXXXXXXXX.
....XXXXXXXXXXXXXwww
....XXXXXXXXXXXXXwww
....XXXXXXXXXXXXwwww
....XX.cXXXXc.XXXXXX
....XX..XXXXX..XXXXX
....XXXXXXXXXXXXXXXXX
.....XXXXXXXXXXXXXXX.
....XX..........XXXX
....XXXXXXXXXXXXXXXX
"""

def parse_sprite(s):
    cells = []
    for r, row in enumerate(s.strip().split('\n')):
        for c, ch in enumerate(row):
            if ch != '.':
                cells.append((r, c, ch))
    return cells

SPRITES = {
    "sitting":  parse_sprite(CAT_SITTING),
    "sleeping": parse_sprite(CAT_SLEEPING),
    "happy":    parse_sprite(CAT_HAPPY),
}

# button
class PixelBtn(tk.Canvas):
    def __init__(self, parent, text, command, w=110, h=38, face=None):
        self._face = face or C["accent"]
        super().__init__(parent, width=w, height=h,
                         bg=C["bg"], highlightthickness=0, cursor="hand2")
        self._text = text; self._cmd = command; self.w = w; self.h = h
        self._draw(False)
        self.bind("<ButtonPress-1>",   lambda e: self._draw(True))
        self.bind("<ButtonRelease-1>", lambda e: [self._draw(False), self._cmd()])

    def _draw(self, pressed):
        self.delete("all")
        o = 3 if pressed else 0
        s = 0 if pressed else 4
        self.create_rectangle(s, s, self.w-1+s, self.h-1+s,
                               fill=C["shadow"], outline="")
        self.create_rectangle(o, o, self.w-1, self.h-1,
                               fill=self._face, outline=C["border"], width=2)
        for x, y in [(o+2,o+2),(self.w-4,o+2),(o+2,self.h-4),(self.w-4,self.h-4)]:
            self.create_rectangle(x, y, x+3, y+3, fill=C["white"], outline="")
        self.create_text(self.w//2+o//2, self.h//2+o//2,
                          text=self._text, font=("Courier",11,"bold"), fill=C["white"])

    def update_face(self, face):
        self._face = face; self._draw(False)


# canvas for cat
class CatCanvas(tk.Canvas):
    def __init__(self, parent, **kw):
        super().__init__(parent, width=140, height=110,
                          bg=C["card"], highlightthickness=0)
        self._sprite = "sitting"
        self._frame  = 0
        self._blink  = 0
        self._animate()

    def set_sprite(self, name):
        self._sprite = name

    def _animate(self):
        if not self.winfo_exists(): return
        self.delete("all")

        px   = 5
        cells = SPRITES.get(self._sprite, SPRITES["sitting"])
        bob  = int(math.sin(self._frame * 0.13) * 3)

        # blink timer
        self._blink += 1
        blinking = (self._blink % 50) < 3

        for (r, c, ch) in cells:
            x0 = 6 + c * px
            y0 = 2 + r * px + bob

            if ch == 'X':
                color = C["black"]
            elif ch == 'n':                        # normal nose
                color = C["nose"]
            elif ch == 'w':                        # white belly / happy nose
                color = "#ffffff" if self._sprite != "happy" else C["nose"]
            elif ch == 'e':                        # normal eyes
                color = C["bg2"] if blinking else "#ffffff"
            elif ch == '-':                        # sleeping eyes (line)
                color = C["bg2"]
            elif ch == 'u':                        # happy eyes (^)
                color = C["bg2"] if blinking else C["accent2"]
            elif ch == 'c':                        # cheek blush
                color = C["cheek"]
            else:
                color = C["black"]

            if ch in ('e', 'u'):
                # draw eyes as small ovals (cutesy)
                self.create_oval(x0, y0, x0+px+1, y0+px+1,
                                  fill=color, outline="")
            elif ch == 'c':
                # blush as soft oval
                self.create_oval(x0-1, y0, x0+px+2, y0+px-1,
                                  fill=color, outline="")
            elif ch == 'n' or ch == 'w':
                self.create_oval(x0, y0, x0+px-1, y0+px-2,
                                  fill=color, outline="")
            else:
                self.create_rectangle(x0, y0, x0+px-1, y0+px-1,
                                       fill=color, outline="")

        # zzz for sleeping
        if self._sprite == "sleeping":
            z_bob = int(math.sin(self._frame * 0.08) * 2)
            self.create_text(118, 22+z_bob, text="z",
                              font=("Courier", 9, "bold"), fill=C["sub"])
            self.create_text(126, 14+z_bob, text="z",
                              font=("Courier", 7), fill=C["accent2"])

        # wagging tail
        tail_x = 108 + int(math.sin(self._frame * 0.18) * 8)
        tail_y = 72 + bob
        self.create_oval(tail_x, tail_y, tail_x+9, tail_y+9,
                          fill=C["black"], outline="")
        self.create_oval(tail_x+2, tail_y+2, tail_x+7, tail_y+7,
                          fill=C["black"], outline="")

        # heart above head when happy
        if self._sprite == "happy":
            hx = 60 + int(math.sin(self._frame*0.1)*3)
            hy = 2 + bob - int(abs(math.sin(self._frame*0.1))*4)
            self.create_text(hx, hy, text="♥",
                              font=("Courier", 10, "bold"), fill=C["accent"])

        self._frame += 1
        self.after(80, self._animate)


# timer for ring
class RingTimer(tk.Canvas):
    def __init__(self, parent):
        super().__init__(parent, width=220, height=220,
                          bg=C["card"], highlightthickness=0)
        self._progress = 1.0
        self._color    = C["accent"]
        self._label    = "25:00"
        self._mode_lbl = "focus time!"
        self._draw()

    def update(self, progress, color, label, mode_lbl):
        self._progress = progress
        self._color    = color
        self._label    = label
        self._mode_lbl = mode_lbl
        self._draw()

    def _draw(self):
        self.delete("all")
        cx, cy, r = 110, 110, 88
        # bg track
        self.create_oval(cx-r, cy-r, cx+r, cy+r, outline=C["bg2"], width=14)
        # progress arc
        extent = -360 * self._progress
        if abs(extent) > 0.5:
            self.create_arc(cx-r, cy-r, cx+r, cy+r,
                             start=90, extent=extent,
                             outline=self._color, width=14, style="arc")
        # tip dot
        angle = math.radians(90 + 360 * self._progress)
        dx = cx + r * math.cos(angle)
        dy = cy - r * math.sin(angle)
        self.create_oval(dx-8, dy-8, dx+8, dy+8,
                          fill=self._color, outline=C["white"], width=2)
        # inner fill
        self.create_oval(cx-72, cy-72, cx+72, cy+72,
                          fill=C["card"], outline=C["bg2"], width=2)
        # time text
        self.create_text(cx, cy-14, text=self._label,
                          font=("Courier", 32, "bold"), fill=C["text"])
        self.create_text(cx, cy+22, text=self._mode_lbl,
                          font=("Courier", 11), fill=C["sub"])


# main app
class PomodoroApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("neko timer ~")
        self.geometry("420x630")
        self.resizable(False, False)
        self.configure(bg=C["bg"])
        self._total   = WORK_TIME
        self._left    = WORK_TIME
        self._running = False
        self._job     = None
        self._session = 0
        self._mode    = "work"
        self._build()

    def _build(self):
        # top deco
        deco = tk.Canvas(self, width=420, height=20, bg=C["bg"], highlightthickness=0)
        deco.place(x=0, y=0)
        for i in range(0, 420, 14):
            col = C["accent"] if (i//14)%2==0 else C["accent2"]
            deco.create_rectangle(i, 2, i+12, 16, fill=col, outline="")

        # title
        tk.Label(self, text="neko pomodoro",
                  font=("Courier", 20, "bold"),
                  bg=C["bg"], fg=C["text"]).place(x=0, y=24, width=420)
        tk.Label(self, text="* stay focused !!! <3 *",
                  font=("Courier", 9), bg=C["bg"],
                  fg=C["sub"]).place(x=0, y=54, width=420)

        # mode tabs
        tab_frame = tk.Frame(self, bg=C["bg"])
        tab_frame.place(x=30, y=78, width=360, height=32)
        self.tab_btns = {}
        for label, key in [("focus","work"),("short break","short"),("long break","long")]:
            btn = tk.Button(tab_frame, text=label,
                             font=("Courier", 9, "bold"), relief="flat", cursor="hand2",
                             command=lambda k=key: self._switch_mode(k))
            btn.pack(side="left", expand=True, fill="both", padx=2)
            self.tab_btns[key] = btn
        self._style_tabs()

        # card
        card_outer = tk.Frame(self, bg=C["border"])
        card_outer.place(x=20, y=118, width=380, height=402)
        self.card = tk.Frame(card_outer, bg=C["card"])
        self.card.place(x=2, y=2, width=376, height=398)

        # ring
        self.ring = RingTimer(self.card)
        self.ring.place(x=78, y=10)

        # cat, bigger and centred
        self.cat = CatCanvas(self.card)
        self.cat.place(x=118, y=238)

        # session dots
        self.dot_canvas = tk.Canvas(self.card, width=360, height=28,
                                     bg=C["card"], highlightthickness=0)
        self.dot_canvas.place(x=8, y=362)
        self._draw_dots()

        # buttons
        btn_frame = tk.Frame(self, bg=C["bg"])
        btn_frame.place(x=30, y=530, width=360, height=50)
        self.start_btn = PixelBtn(btn_frame, "  START  ",
                                   command=self._toggle, w=150, h=42, face=C["accent"])
        self.start_btn.pack(side="left", padx=6)
        PixelBtn(btn_frame, "RESET", command=self._reset,
                  w=100, h=42, face=C["accent2"]).pack(side="left", padx=6)
        PixelBtn(btn_frame, "SKIP",  command=self._skip,
                  w=80, h=42, face=C["shadow"]).pack(side="left", padx=6)

        # bottom decor
        btm = tk.Canvas(self, width=420, height=20, bg=C["bg"], highlightthickness=0)
        btm.place(x=0, y=608)
        for i in range(0, 420, 14):
            col = C["accent2"] if (i//14)%2==0 else C["accent"]
            btm.create_rectangle(i, 2, i+12, 16, fill=col, outline="")

        self._refresh_ring()

    def _style_tabs(self):
        colors = {"work": C["accent"], "short": C["green"], "long": C["yellow"]}
        for key, btn in self.tab_btns.items():
            active = key == self._mode
            btn.configure(bg=colors[key] if active else C["bg2"],
                           fg=C["white"] if active else C["sub"])

    def _draw_dots(self):
        self.dot_canvas.delete("all")
        cx = 210
        for i in range(4):
            x = cx - 63 + i * 42
            filled = i < self._session
            self.dot_canvas.create_oval(x-11, 3, x+11, 25,
                                         fill=C["accent"] if filled else C["bg2"],
                                         outline=C["border"], width=2)
            self.dot_canvas.create_text(x, 14,
                                         text="♥" if filled else "·",
                                         font=("Courier", 11, "bold"),
                                         fill=C["white"] if filled else C["accent2"])

    def _mode_info(self):
        if self._mode == "work":
            return WORK_TIME,   C["accent"], "focus time!",  "sitting"
        elif self._mode == "short":
            return SHORT_BREAK, C["sub"],    "short break~", "sleeping"
        else:
            return LONG_BREAK,  C["shadow"], "long break!!", "happy"

    def _refresh_ring(self):
        total, color, lbl, sprite = self._mode_info()
        mins, secs = self._left // 60, self._left % 60
        self.ring.update(self._left / total if total else 0,
                          color, f"{mins:02d}:{secs:02d}", lbl)
        self.cat.set_sprite(sprite)

    def _switch_mode(self, mode):
        self._stop()
        self._mode = mode
        total, *_ = self._mode_info()
        self._total = total
        self._left  = total
        self._style_tabs()
        self.start_btn.update_face(C["accent"] if mode == "work" else C["sub"])
        tint = {"work": C["card"], "short": "#f0fff8", "long": "#fffdf0"}
        bg = tint[mode]
        self.card.configure(bg=bg)
        self.ring.configure(bg=bg)
        self.cat.configure(bg=bg)
        self.dot_canvas.configure(bg=bg)
        self.start_btn._text = "  START  "; self.start_btn._draw(False)
        self._refresh_ring()

    def _toggle(self):
        if self._running:
            self._stop()
            self.start_btn._text = "  START  "
        else:
            self._start()
            self.start_btn._text = "  PAUSE  "
        self.start_btn._draw(False)

    def _start(self):
        self._running = True; self._tick()

    def _stop(self):
        self._running = False
        if self._job: self.after_cancel(self._job); self._job = None

    def _tick(self):
        if not self._running: return
        if self._left <= 0:
            self._running = False; self._on_complete(); return
        self._left -= 1
        self._refresh_ring()
        self._job = self.after(1000, self._tick)

    def _on_complete(self):
        self.start_btn._text = "  START  "; self.start_btn._draw(False)
        if self._mode == "work":
            self._session = min(4, self._session + 1)
            self._draw_dots()
            if self._session >= 4:
                messagebox.showinfo("nyaa!! (=^.^=)",
                    "4 pomodoros done!!\ntime for a long break~ you earned it!")
                self._session = 0; self._draw_dots()
                self._switch_mode("long")
            else:
                messagebox.showinfo("nyaa!! (=^.^=)",
                    f"focus session done! ({self._session}/4)\ntake a short break~ (=^-w-^=)")
                self._switch_mode("short")
        else:
            messagebox.showinfo("nyaa!! (=^.^=)", "break's over!\nback to work~ (=^.^=)")
            self._switch_mode("work")

    def _reset(self):
        self._stop()
        self._left = self._total
        self.start_btn._text = "  START  "; self.start_btn._draw(False)
        self._refresh_ring()

    def _skip(self):
        self._stop(); self._on_complete()


if __name__ == "__main__":
    app = PomodoroApp()
    app.mainloop()
