import sys
import io

# Windows 環境で UTF-8 出力を強制する
if sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from engine import GameEngine


def main():
    game = GameEngine()
    game.run()


if __name__ == "__main__":
    main()
