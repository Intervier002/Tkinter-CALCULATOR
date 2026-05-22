import tkinter as tk
from tkinter import font
import math


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.resizable(False, False)
        self.root.configure(bg="#0f0f0f")

        # State
        self.expression = ""
        self.display_var = tk.StringVar(value="0")
        self.sub_display_var = tk.StringVar(value="")
        self.new_number = True
        self.last_operator = ""
        self.result_shown = False

        self._build_ui()

    # ── UI Construction ──────────────────────────────────────────────

    def _build_ui(self):
        DISPLAY_BG = "#1a1a1a"
        BTN_BG     = "#2a2a2a"
        BTN_DARK   = "#1f1f1f"
        OP_COLOR   = "#ff6b35"
        EQ_COLOR   = "#ff6b35"
        SPEC_COLOR = "#3a3a3a"
        FG_WHITE   = "#f5f5f5"
        FG_GRAY    = "#888888"
        FG_ORANGE  = "#ff6b35"

        # ── Display ──────────────────────────────────────────────────
        display_frame = tk.Frame(self.root, bg=DISPLAY_BG, pady=20, padx=24)
        display_frame.grid(row=0, column=0, columnspan=4, sticky="ew")

        sub_lbl = tk.Label(
            display_frame,
            textvariable=self.sub_display_var,
            bg=DISPLAY_BG, fg=FG_GRAY,
            font=("Courier New", 13),
            anchor="e"
        )
        sub_lbl.pack(fill="x")

        main_lbl = tk.Label(
            display_frame,
            textvariable=self.display_var,
            bg=DISPLAY_BG, fg=FG_WHITE,
            font=("Courier New", 42, "bold"),
            anchor="e"
        )
        main_lbl.pack(fill="x")

        # ── Button Grid ───────────────────────────────────────────────
        btn_frame = tk.Frame(self.root, bg="#0f0f0f", padx=12, pady=12)
        btn_frame.grid(row=1, column=0, columnspan=4)

        # Layout: (label, row, col, colspan, bg, fg, cmd)
        buttons = [
            # Row 1
            ("AC",  0, 0, 1, SPEC_COLOR, FG_ORANGE, self.clear_all),
            ("+/-", 0, 1, 1, SPEC_COLOR, FG_WHITE,  self.toggle_sign),
            ("%",   0, 2, 1, SPEC_COLOR, FG_WHITE,  self.percent),
            ("÷",   0, 3, 1, OP_COLOR,   "#fff",    lambda: self.operator("/")),

            # Row 2
            ("7",  1, 0, 1, BTN_BG, FG_WHITE, lambda: self.digit("7")),
            ("8",  1, 1, 1, BTN_BG, FG_WHITE, lambda: self.digit("8")),
            ("9",  1, 2, 1, BTN_BG, FG_WHITE, lambda: self.digit("9")),
            ("×",  1, 3, 1, OP_COLOR, "#fff", lambda: self.operator("*")),

            # Row 3
            ("4",  2, 0, 1, BTN_BG, FG_WHITE, lambda: self.digit("4")),
            ("5",  2, 1, 1, BTN_BG, FG_WHITE, lambda: self.digit("5")),
            ("6",  2, 2, 1, BTN_BG, FG_WHITE, lambda: self.digit("6")),
            ("−",  2, 3, 1, OP_COLOR, "#fff", lambda: self.operator("-")),

            # Row 4
            ("1",  3, 0, 1, BTN_BG, FG_WHITE, lambda: self.digit("1")),
            ("2",  3, 1, 1, BTN_BG, FG_WHITE, lambda: self.digit("2")),
            ("3",  3, 2, 1, BTN_BG, FG_WHITE, lambda: self.digit("3")),
            ("+",  3, 3, 1, OP_COLOR, "#fff", lambda: self.operator("+")),

            # Row 5
            ("0",  4, 0, 2, BTN_BG, FG_WHITE, lambda: self.digit("0")),
            (".",  4, 2, 1, BTN_BG, FG_WHITE, self.decimal),
            ("=",  4, 3, 1, EQ_COLOR, "#fff", self.equals),
        ]

        PAD = 6

        for (label, row, col, colspan, bg, fg, cmd) in buttons:
            w = 72 * colspan + PAD * (colspan - 1)
            btn = tk.Button(
                btn_frame,
                text=label,
                width=0,
                bg=bg,
                fg=fg,
                activebackground=self._lighten(bg),
                activeforeground=fg,
                relief="flat",
                bd=0,
                font=("Courier New", 18, "bold"),
                cursor="hand2",
                command=cmd
            )
            btn.grid(
                row=row, column=col, columnspan=colspan,
                padx=PAD // 2, pady=PAD // 2,
                ipadx=0, ipady=14,
                sticky="ew"
            )
            # Make zero button wider via column weight
            btn_frame.columnconfigure(col, minsize=72)

        # Keyboard bindings
        self.root.bind("<Key>", self._on_key)

    # ── Helpers ───────────────────────────────────────────────────────

    def _lighten(self, hex_color):
        """Return a slightly lighter shade of a hex color."""
        try:
            h = hex_color.lstrip("#")
            r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
            r = min(255, r + 30)
            g = min(255, g + 30)
            b = min(255, b + 30)
            return f"#{r:02x}{g:02x}{b:02x}"
        except Exception:
            return hex_color

    def _format(self, value: float) -> str:
        """Format a float for display (strip trailing zeros)."""
        if value == int(value) and not math.isinf(value):
            result = str(int(value))
        else:
            result = f"{value:.10g}"
        # Truncate if too long
        if len(result) > 12:
            result = f"{value:.6g}"
        return result

    def _set_display(self, text):
        self.display_var.set(text)

    # ── Button Actions ────────────────────────────────────────────────

    def digit(self, d: str):
        current = self.display_var.get()
        if self.result_shown or self.new_number:
            self._set_display(d)
            self.new_number = False
            self.result_shown = False
        else:
            if current == "0" and d != ".":
                self._set_display(d)
            else:
                if len(current) < 12:
                    self._set_display(current + d)

    def decimal(self):
        if self.result_shown or self.new_number:
            self._set_display("0.")
            self.new_number = False
            self.result_shown = False
            return
        current = self.display_var.get()
        if "." not in current:
            self._set_display(current + ".")

    def operator(self, op: str):
        current = self.display_var.get()
        op_sym = {"*": "×", "/": "÷", "+": "+", "-": "−"}[op]

        if self.expression and not self.new_number and not self.result_shown:
            # Chain: evaluate what we have first
            try:
                result = eval(self.expression + current)
                self.expression = str(result) + op
                self.sub_display_var.set(self._format(result) + f" {op_sym}")
                self._set_display(self._format(result))
            except Exception:
                self._set_display("Error")
                self.expression = ""
                return
        else:
            self.expression = current + op
            self.sub_display_var.set(current + f" {op_sym}")

        self.last_operator = op
        self.new_number = True
        self.result_shown = False

    def equals(self):
        current = self.display_var.get()
        if not self.expression:
            return
        full_expr = self.expression + current
        self.sub_display_var.set(
            self.expression.replace("*", "×").replace("/", "÷") + current + " ="
        )
        try:
            result = eval(full_expr)
            if math.isinf(result) or math.isnan(result):
                self._set_display("Error")
            else:
                self._set_display(self._format(result))
        except ZeroDivisionError:
            self._set_display("÷ 0 Error")
        except Exception:
            self._set_display("Error")
        self.expression = ""
        self.new_number = True
        self.result_shown = True

    def clear_all(self):
        self.expression = ""
        self.last_operator = ""
        self.new_number = True
        self.result_shown = False
        self._set_display("0")
        self.sub_display_var.set("")

    def toggle_sign(self):
        current = self.display_var.get()
        try:
            val = float(current)
            val = -val
            self._set_display(self._format(val))
        except Exception:
            pass

    def percent(self):
        current = self.display_var.get()
        try:
            val = float(current) / 100
            self._set_display(self._format(val))
        except Exception:
            pass

    # ── Keyboard Support ──────────────────────────────────────────────

    def _on_key(self, event):
        key = event.keysym
        char = event.char
        if char in "0123456789":
            self.digit(char)
        elif char == ".":
            self.decimal()
        elif char in ("+", "-", "*", "/"):
            self.operator(char)
        elif key in ("Return", "KP_Enter"):
            self.equals()
        elif key == "BackSpace":
            self._backspace()
        elif key == "Escape":
            self.clear_all()
        elif char == "%":
            self.percent()

    def _backspace(self):
        current = self.display_var.get()
        if self.result_shown or len(current) <= 1:
            self._set_display("0")
            self.new_number = True
            self.result_shown = False
        else:
            self._set_display(current[:-1])


# ── Entry Point ───────────────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("340x560")
    app = Calculator(root)
    root.mainloop()