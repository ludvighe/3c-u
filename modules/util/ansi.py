
# ANSI escape codes and convenience functions
class Ansi:
    # Escape
    ESC = '\033'

    # Terminal commands
    CLEAR = '[2J'

    # Reset formatting
    NC = '[0m'

    # Style
    BOLD = '[1m'
    FAINT = '[2m'
    ITALIC = '[3m'
    UNDERLINE = '[4m'
    BLINK = '[5m'
    NEGATIVE = '[7m'
    CROSSED = '[9m'

    # Foreground color
    FG_BLACK = '[0;30m'
    FG_RED = '[0;31m'
    FG_GREEN = '[0;32m'
    FG_BROWN = '[0;33m'
    FG_BLUE = '[0;34m'
    FG_PURPLE = '[0;35m'
    FG_CYAN = '[0;36m'
    FG_LIGHT_GRAY = '[0;37m'
    FG_DARK_GRAY = '[1;30m'
    FG_BRIGHT_RED = '[1;31m'
    FG_BRIGHT_GREEN = '[1;32m'
    FG_YELLOW = '[1;33m'
    FG_BRIGHT_BLUE = '[1;34m'
    FG_BRIGHT_PURPLE = '[1;35m'
    FG_BRIGHT_CYAN = '[1;36m'
    FG_BRIGHT_WHITE = '[1;37m'

    # Background color
    BG_BLACK = '[40m'
    BG_RED = '[41m'
    BG_GREEN = '[42m'
    BG_YELLOW = '[43m'
    BG_BLUE = '[44m'
    BG_MAGENTA = '[45m'
    BG_CYAN = '[46m'
    BG_WHITE = '[47m'
    BG_GRAY = '[100m'

    BG_BRIGHT_BLACK = '[40;1m'
    BG_BRIGHT_RED = '[41;1m'
    BG_BRIGHT_GREEN = '[42;1m'
    BG_BRIGHT_YELLOW = '[43;1m'
    BG_BRIGHT_BLUE = '[44;1m'
    BG_BRIGHT_MAGENTA = '[45;1m'
    BG_BRIGHT_CYAN = '[46;1m'
    BG_BRIGHT_WHITE = '[47;1m'

    # String formatter
    # call: Ansi.fmt('str', Ansi.FORMATTING)
    def fmt(s: str, fmt: str):
        return Ansi.ESC + fmt + s + Ansi.ESC + Ansi.NC

    # Clear teminal
    def clear():
        return Ansi.ESC + Ansi.CLEAR


# Test to print all available ANSI escape codes
def test_all():
    for item in Ansi.__dict__.items():
        if '__' in item[0] or 'fmt' in item[0] or 'clear' in item[0] or item[0] == 'ESC':
            continue
        print(Ansi.fmt(item[0], item[1]))
