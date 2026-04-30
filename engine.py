import time

from player import Player
from utils import typewrite, show_memory_flash, clear_screen, press_enter
from data.locations import LOCATIONS
from data.items import ITEMS
from data.events import EVENTS

DIRECTION_NAMES = {
    "north": "北",
    "south": "南",
    "east": "東",
    "west": "西",
    "up": "上（屋上へ）",
    "down": "下（地下へ）",
}

TITLE = """
╔══════════════════════════════════════════════════════╗
║                                                      ║
║          記  憶  な  き  告  発  者                   ║
║            ～  NEMESIS : 2087  ～                    ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
"""


class GameEngine:
    def __init__(self):
        self.player = Player()

    # ────────────────────────────────────────────
    # メインループ
    # ────────────────────────────────────────────

    def run(self):
        clear_screen()
        print(TITLE)
        typewrite("  西暦2087年。あなたは目覚めた。")
        time.sleep(0.5)
        press_enter()
        clear_screen()
        self._show_location(first_visit=True)

        while not self.player.game_over:
            self.player.turn_count += 1
            self._show_menu()
            choice = self._get_input("  > ", valid=[str(i) for i in range(1, 7)])
            clear_screen()
            self._process_action(choice)

        print()
        typewrite("  プレイありがとうございました。")

    # ────────────────────────────────────────────
    # 表示系
    # ────────────────────────────────────────────

    def _show_location(self, first_visit=False):
        loc = LOCATIONS[self.player.location]
        loc_id = self.player.location

        # 初回訪問フレーバーテキスト
        if first_visit and loc_id not in self.player.visited:
            first_text = loc.get("first_visit", "")
            if first_text:
                print()
                typewrite("  " + first_text.replace("\n", "\n  "))
                time.sleep(0.3)

        self.player.visited.add(loc_id)

        # 場所の説明
        print()
        print(f"  ■ {loc['name']}")
        print("  " + "─" * 46)
        typewrite("  " + loc["description"].replace("\n", "\n  "))

        # 拾えるアイテム
        pickable = [
            i for i in loc.get("items", [])
            if not ITEMS[i].get("fixed") and i not in self.player.inventory
        ]
        # 設置物アイテム
        fixed_items = [i for i in loc.get("items", []) if ITEMS[i].get("fixed")]

        if pickable:
            names = "、".join(ITEMS[i]["name"] for i in pickable)
            print(f"\n  床に {names} が落ちている。")
        if fixed_items:
            names = "、".join(ITEMS[i]["name"] for i in fixed_items)
            print(f"  {names} がある。")

        # 移動可能な方向を表示
        self._show_exits()

        # 場所イベントのチェック（移動時のみ）
        if first_visit:
            for event_id in loc.get("events", []):
                ev = EVENTS.get(event_id, {})
                done_flag = ev.get("done_flag")
                if done_flag and done_flag not in self.player.flags:
                    press_enter()
                    self._trigger_event(event_id)

    def _show_exits(self):
        loc = LOCATIONS[self.player.location]
        connections = loc.get("connections", {})
        locked = loc.get("locked_connections", {})
        if not connections:
            return
        parts = []
        for dir_key, dest in connections.items():
            dir_name = DIRECTION_NAMES.get(dir_key, dir_key)
            dest_name = LOCATIONS[dest]["name"]
            if dir_key in locked and locked[dir_key]["required_flag"] not in self.player.flags:
                parts.append(f"{dir_name}→{dest_name}[施錠]")
            else:
                parts.append(f"{dir_name}→{dest_name}")
        print("  出口: " + " / ".join(parts))

    def _show_menu(self):
        print()
        print("  " + "─" * 46)
        print("  [ 行動を選んでください ]")
        print("  1. 移動する")
        print("  2. アイテムを拾う")
        print("  3. アイテムを調べる")
        print("  4. アイテムを使う")
        print("  5. インベントリを確認する")
        print("  6. 周囲を見回す（説明を再表示）")
        print("  " + "─" * 46)

    # ────────────────────────────────────────────
    # 入力
    # ────────────────────────────────────────────

    def _get_input(self, prompt="  > ", valid=None):
        while True:
            try:
                choice = input(prompt).strip()
            except (EOFError, KeyboardInterrupt):
                print()
                choice = ""
            if valid is None or choice in valid:
                return choice
            print("  無効な入力です。もう一度選んでください。")

    # ────────────────────────────────────────────
    # アクション振り分け
    # ────────────────────────────────────────────

    def _process_action(self, choice):
        dispatch = {
            "1": self._action_move,
            "2": self._action_pickup,
            "3": self._action_inspect,
            "4": self._action_use,
            "5": self._action_inventory,
            "6": lambda: self._show_location(first_visit=False),
        }
        dispatch.get(choice, lambda: None)()

    # ────────────────────────────────────────────
    # 個別アクション
    # ────────────────────────────────────────────

    def _action_move(self):
        loc = LOCATIONS[self.player.location]
        connections = loc.get("connections", {})
        locked = loc.get("locked_connections", {})

        if not connections:
            typewrite("  どこにも行けない。")
            return

        items_list = list(connections.items())
        print("\n  [ どこへ移動しますか？ ]")
        for i, (dir_key, dest) in enumerate(items_list, 1):
            dir_name = DIRECTION_NAMES.get(dir_key, dir_key)
            dest_name = LOCATIONS[dest]["name"]
            if dir_key in locked and locked[dir_key]["required_flag"] not in self.player.flags:
                print(f"  {i}. {dir_name} → {dest_name}  [施錠中]")
            else:
                print(f"  {i}. {dir_name} → {dest_name}")
        cancel = len(items_list) + 1
        print(f"  {cancel}. キャンセル")

        choice = self._get_input("  > ", [str(i) for i in range(1, cancel + 1)])
        idx = int(choice) - 1
        if idx >= len(items_list):
            self._show_location(first_visit=False)
            return

        dir_key, dest = items_list[idx]
        if dir_key in locked and locked[dir_key]["required_flag"] not in self.player.flags:
            typewrite("\n  " + locked[dir_key]["locked_text"])
            return

        self.player.location = dest
        self._show_location(first_visit=True)

    def _action_pickup(self):
        loc = LOCATIONS[self.player.location]
        pickable = [
            i for i in loc.get("items", [])
            if not ITEMS[i].get("fixed") and i not in self.player.inventory
        ]

        if not pickable:
            typewrite("  拾えるアイテムはない。")
            self._show_location(first_visit=False)
            return

        print("\n  [ どれを拾いますか？ ]")
        for i, item_id in enumerate(pickable, 1):
            print(f"  {i}. {ITEMS[item_id]['name']}")
        cancel = len(pickable) + 1
        print(f"  {cancel}. キャンセル")

        choice = self._get_input("  > ", [str(i) for i in range(1, cancel + 1)])
        idx = int(choice) - 1
        if idx >= len(pickable):
            self._show_location(first_visit=False)
            return

        item_id = pickable[idx]
        self.player.inventory.append(item_id)
        typewrite(f"\n  {ITEMS[item_id]['pickup_text']}")
        self._show_location(first_visit=False)

    def _action_inspect(self):
        loc = LOCATIONS[self.player.location]
        fixed_items = [i for i in loc.get("items", []) if ITEMS[i].get("fixed")]
        all_items = self.player.inventory + fixed_items

        if not all_items:
            typewrite("  調べられるものがない。")
            self._show_location(first_visit=False)
            return

        print("\n  [ 何を調べますか？ ]")
        for i, item_id in enumerate(all_items, 1):
            suffix = "  [設置物]" if item_id in fixed_items else ""
            print(f"  {i}. {ITEMS[item_id]['name']}{suffix}")
        cancel = len(all_items) + 1
        print(f"  {cancel}. キャンセル")

        choice = self._get_input("  > ", [str(i) for i in range(1, cancel + 1)])
        idx = int(choice) - 1
        if idx >= len(all_items):
            self._show_location(first_visit=False)
            return

        item_id = all_items[idx]
        print()
        typewrite("  " + ITEMS[item_id]["description"].replace("\n", "\n  "))

        inspect_event = ITEMS[item_id].get("inspect_event")
        if inspect_event:
            ev = EVENTS.get(inspect_event, {})
            unlock_flag = ev.get("unlock_flag")
            # まだ解放されていない記憶イベントなら発火
            if not unlock_flag or unlock_flag not in self.player.flags:
                press_enter()
                self._trigger_event(inspect_event)

        self._show_location(first_visit=False)

    def _action_use(self):
        loc = LOCATIONS[self.player.location]
        inv_usable = [i for i in self.player.inventory if ITEMS[i].get("usable")]
        fixed_usable = [
            i for i in loc.get("items", [])
            if ITEMS[i].get("fixed") and ITEMS[i].get("usable")
        ]
        all_usable = inv_usable + fixed_usable

        if not all_usable:
            typewrite("  使えるアイテムがない。")
            self._show_location(first_visit=False)
            return

        print("\n  [ 何を使いますか？ ]")
        for i, item_id in enumerate(all_usable, 1):
            suffix = "  [設置物]" if item_id in fixed_usable else ""
            print(f"  {i}. {ITEMS[item_id]['name']}{suffix}")
        cancel = len(all_usable) + 1
        print(f"  {cancel}. キャンセル")

        choice = self._get_input("  > ", [str(i) for i in range(1, cancel + 1)])
        idx = int(choice) - 1
        if idx >= len(all_usable):
            self._show_location(first_visit=False)
            return

        item_id = all_usable[idx]
        use_event = ITEMS[item_id].get("use_event")
        if use_event:
            self._trigger_event(use_event)

        if not self.player.game_over:
            self._show_location(first_visit=False)

    def _action_inventory(self):
        if not self.player.inventory:
            typewrite("  インベントリは空だ。")
        else:
            print("\n  [ 所持アイテム ]")
            for item_id in self.player.inventory:
                print(f"  ・{ITEMS[item_id]['name']}")
        total = 5
        print(f"\n  記憶の断片: {self.player.memory_count} / {total}")
        if self.player.memory_count == total:
            print("  ★ すべての記憶を取り戻した。")
        self._show_location(first_visit=False)

    # ────────────────────────────────────────────
    # イベント処理
    # ────────────────────────────────────────────

    def _trigger_event(self, event_id):
        ev = EVENTS.get(event_id)
        if not ev:
            return

        handlers = {
            "memory":        self._handle_memory,
            "encounter":     self._handle_encounter,
            "story":         self._handle_story,
            "ending_check":  self._handle_ending_check,
            "ending":        self._handle_ending,
        }
        handler = handlers.get(ev["type"])
        if handler:
            handler(ev)

    def _handle_memory(self, ev):
        unlock_flag = ev.get("unlock_flag", "")
        if unlock_flag in self.player.flags:
            return  # 既に解放済み

        show_memory_flash(ev["fragment"])
        self.player.flags.add(unlock_flag)
        self.player.memory_count += 1

        print()
        typewrite(f"  ✦ {ev['summary']}")
        typewrite(f"  記憶の断片: {self.player.memory_count} / 5")

        if self.player.memory_count == 5:
            time.sleep(0.4)
            typewrite("  ★ すべての記憶が戻った。真実が見えてきた。")

    def _handle_encounter(self, ev):
        done_flag = ev.get("done_flag")
        if done_flag and done_flag in self.player.flags:
            return  # 既に処理済み

        print()
        typewrite("  " + ev["text"].replace("\n", "\n  "))

        choices = ev["choices"]
        print("\n  [ どうする？ ]")
        for i, c in enumerate(choices, 1):
            req = c.get("required_item")
            if req and req not in self.player.inventory:
                print(f"  {i}. {c['text']}  ※ {ITEMS[req]['name']}が必要")
            else:
                print(f"  {i}. {c['text']}")

        valid = [str(i) for i in range(1, len(choices) + 1)]

        # 必要アイテムがない選択肢を選んだ場合は再入力を促す
        while True:
            choice = self._get_input("  > ", valid)
            idx = int(choice) - 1
            selected = choices[idx]
            req = selected.get("required_item")
            if req and req not in self.player.inventory:
                typewrite(f"  しかし、{ITEMS[req]['name']}を持っていない。")
                continue
            break

        print()
        typewrite("  " + selected["result_text"].replace("\n", "\n  "))
        self.player.flags.add(selected["result_flag"])
        if done_flag:
            self.player.flags.add(done_flag)

        if selected.get("is_bad_ending"):
            press_enter()
            self._trigger_event("bad_ending_caught")

    def _handle_story(self, ev):
        # 場所条件チェック
        req_loc = ev.get("required_location")
        if req_loc and self.player.location != req_loc:
            typewrite("\n  " + ev.get("wrong_location_text", "ここでは使えない。"))
            return

        # フラグ条件チェック
        req_flag = ev.get("required_flag")
        if req_flag and req_flag not in self.player.flags:
            typewrite("\n  " + ev.get("missing_flag_text", "何も起きなかった。"))
            return

        # 既に解放済みのイベントは再実行しない
        unlock_flag = ev.get("unlock_flag")
        if unlock_flag and unlock_flag in self.player.flags:
            typewrite("\n  （すでに使用済みだ）")
            return

        print()
        typewrite("  " + ev["text"].replace("\n", "\n  "))

        if unlock_flag:
            self.player.flags.add(unlock_flag)
        if ev.get("summary"):
            print()
            typewrite(f"  ✦ {ev['summary']}")

    def _handle_ending_check(self, ev=None):
        """衛星通信端末の使用：エンディング分岐"""
        if self.player.location != "rooftop":
            typewrite("  ここでは使えない。")
            return

        if "data_chip" not in self.player.inventory:
            typewrite(
                "\n  端末のスロットが空だ。\n"
                "  送信するデータが必要だ。"
            )
            return

        press_enter()
        self._trigger_event("good_ending")

    def _handle_ending(self, ev):
        print()
        typewrite(ev["text"], delay=0.04)
        self.player.game_over = True
        self.player.ending = ev.get("result", "bad")
        print()
        if ev.get("result") == "good":
            typewrite("  おめでとうございます！グッドエンディングを達成しました。")
        else:
            typewrite("  バッドエンディングです。もう一度挑戦してみてください。")
