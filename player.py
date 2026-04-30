class Player:
    def __init__(self):
        self.location = "hospital_room"   # 現在地のID
        self.inventory = []               # 所持アイテムID リスト
        self.memory_count = 0             # 回収した記憶断片数（全5個）
        self.flags = set()                # ストーリーフラグ
        self.visited = set()              # 訪問済み場所ID
        self.turn_count = 0               # 経過ターン数
        self.game_over = False
        self.ending = None                # "good" or "bad"
