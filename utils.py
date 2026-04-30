import sys
import time
import os


def typewrite(text, delay=0.025):
    """タイプライター風にテキストを1文字ずつ表示する"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def show_memory_flash(text):
    """記憶フラッシュバック演出"""
    print()
    border = "╔" + "═" * 50 + "╗"
    title  = "║" + "  【 記 憶 フ ラ ッ シ ュ バ ッ ク 】  ".center(50) + "║"
    sep    = "╠" + "═" * 50 + "╣"
    bottom = "╚" + "═" * 50 + "╝"

    print(border)
    print(title)
    print(sep)
    time.sleep(0.4)
    for line in text.split("\n"):
        time.sleep(0.08)
        sys.stdout.write("║  " + line + "\n")
        sys.stdout.flush()
    print(bottom)
    time.sleep(0.8)


def clear_screen():
    """画面をクリアする"""
    os.system("cls" if os.name == "nt" else "clear")


def press_enter():
    """Enterキーで続行するプロンプト"""
    input("\n  [ Enter キーで続ける... ]")
