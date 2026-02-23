"""
Interactive terminal calendar — navigate months with arrow keys or +/-.
Press 'q' or Escape to quit, 't' to jump back to today.
"""

import calendar
import datetime
import os
import sys

# ── ANSI colour helpers ────────────────────────────────────────────────────────
RESET   = "\033[0m"
BOLD    = "\033[1m"
DIM     = "\033[2m"

FG_WHITE   = "\033[97m"
FG_CYAN    = "\033[96m"
FG_YELLOW  = "\033[93m"
FG_BLACK   = "\033[30m"

BG_BLUE    = "\033[44m"
BG_CYAN    = "\033[46m"

BORDER     = "\033[38;5;240m"   # grey

def _enable_ansi_windows() -> None:
    """Enable ANSI escape codes on Windows 10+."""
    if sys.platform == "win32":
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

def clear() -> None:
    os.system("cls" if sys.platform == "win32" else "clear")

# ── Platform key reader ────────────────────────────────────────────────────────
if sys.platform == "win32":
    import msvcrt

    def _getch() -> str:
        ch = msvcrt.getch()
        if ch in (b"\x00", b"\xe0"):   # special key prefix
            ch2 = msvcrt.getch()
            return {b"K": "LEFT", b"M": "RIGHT", b"H": "UP", b"P": "DOWN"}.get(ch2, "")
        return ch.decode("utf-8", errors="ignore")

else:
    import tty, termios

    def _getch() -> str:
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch == "\x1b":
                ch2 = sys.stdin.read(2)
                return {"[D": "LEFT", "[C": "RIGHT", "[A": "UP", "[B": "DOWN"}.get(ch2, "ESC")
            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)


# ── Calendar renderer ──────────────────────────────────────────────────────────
DAYS_HEADER = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
CAL_WIDTH   = 26   # inner width (border excluded)

def _hline(char: str = "─") -> str:
    return BORDER + "│" + RESET + char * (CAL_WIDTH + 2) + BORDER + "│" + RESET

def _box_top() -> str:
    return BORDER + "╭" + "─" * (CAL_WIDTH + 2) + "╮" + RESET

def _box_bot() -> str:
    return BORDER + "╰" + "─" * (CAL_WIDTH + 2) + "╯" + RESET

def _pad(text: str, width: int, align: str = "center") -> str:
    """Pad *visible* text (strips ANSI for length calculation)."""
    import re
    visible_len = len(re.sub(r"\033\[[0-9;]*m", "", text))
    pad = width - visible_len
    if align == "center":
        left = pad // 2
        return " " * left + text + " " * (pad - left)
    if align == "right":
        return " " * pad + text
    return text + " " * pad  # left


def render_calendar(year: int, month: int, today: datetime.date) -> list[str]:
    """Return a list of lines forming the calendar box."""
    month_name = datetime.date(year, month, 1).strftime("%B %Y")
    cal = calendar.monthcalendar(year, month)

    lines: list[str] = []
    lines.append(_box_top())

    # ── Month / year title ──
    title = BOLD + FG_CYAN + month_name + RESET
    lines.append(BORDER + "│ " + RESET + _pad(title, CAL_WIDTH) + BORDER + " │" + RESET)
    lines.append(BORDER + "│" + "─" * (CAL_WIDTH + 2) + "│" + RESET)

    # ── Day names ──
    header_parts = []
    for i, d in enumerate(DAYS_HEADER):
        color = FG_YELLOW if i >= 5 else BOLD + FG_WHITE
        header_parts.append(color + d + RESET)
    header_line = "  ".join(header_parts)
    lines.append(BORDER + "│ " + RESET + _pad(header_line, CAL_WIDTH) + BORDER + " │" + RESET)
    lines.append(BORDER + "│" + "─" * (CAL_WIDTH + 2) + "│" + RESET)

    # ── Weeks ──
    for week in cal:
        cells = []
        for idx, day in enumerate(week):
            if day == 0:
                cells.append("  ")
            else:
                is_today   = (year == today.year and month == today.month and day == today.day)
                is_weekend = idx >= 5
                if is_today:
                    cell = BG_BLUE + BOLD + FG_WHITE + f"{day:2d}" + RESET
                elif is_weekend:
                    cell = FG_YELLOW + f"{day:2d}" + RESET
                else:
                    cell = FG_WHITE + f"{day:2d}" + RESET
                cells.append(cell)
        row = "  ".join(cells)
        lines.append(BORDER + "│ " + RESET + _pad(row, CAL_WIDTH) + BORDER + " │" + RESET)

    lines.append(_box_bot())
    return lines


def render_ui(year: int, month: int, today: datetime.date) -> None:
    clear()
    cal_lines = render_calendar(year, month, today)

    print()
    for line in cal_lines:
        print("  " + line)

    print()
    hint = (
        DIM + "  ← → / ± " + RESET + "prev·next month   │   "
        + DIM + "[ ]" + RESET + " prev·next year   │   "
        + DIM + "t" + RESET + " today   │   "
        + DIM + "q" + RESET + " quit"
    )
    print(hint)
    print()


# ── Main loop ──────────────────────────────────────────────────────────────────
def main() -> None:
    _enable_ansi_windows()

    today = datetime.date.today()
    year, month = today.year, today.month

    while True:
        render_ui(year, month, today)

        key = _getch()

        if key in ("q", "Q", "\x1b", "\x03"):      # quit
            clear()
            break
        elif key in ("LEFT", "-", "h", "H"):        # previous month
            month -= 1
            if month < 1:
                month = 12
                year -= 1
        elif key in ("RIGHT", "+", "l", "L"):       # next month
            month += 1
            if month > 12:
                month = 1
                year += 1
        elif key in ("UP", "["):                    # previous year
            year -= 1
        elif key in ("DOWN", "]"):                  # next year
            year += 1
        elif key in ("t", "T"):                     # jump to today
            today = datetime.date.today()           # refresh in case day changed
            year, month = today.year, today.month


if __name__ == "__main__":
    main()
