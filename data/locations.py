# 場所データ
# connections: 移動可能な方向と目的地ID
# locked_connections: 条件付きで開く通路
# items: その場所に存在するアイテムID
# events: 訪問時に発生するイベントID

LOCATIONS = {
    "hospital_room": {
        "name": "廃病院の一室",
        "description": (
            "薄汚れたベッドが一台。天井からは蛍光灯がちらついている。\n"
            "窓の外は灰色の空。壁には「区画7-C 隔離室」と貼り紙がある。\n"
            "あなたは床に倒れていた――ここがどこで、いつかも分からない。"
        ),
        "first_visit": (
            "目が覚める。\n"
            "全身が重い。頭の中は空っぽだ。\n"
            "名前も、顔も、過去も――何も思い出せない。\n"
            "ただ一つだけ確かなことがある。\n"
            "ここから出なければならない。"
        ),
        "connections": {
            "north": "dark_alley",
        },
        "locked_connections": {},
        "items": ["wristband", "syringe"],
        "events": [],
    },
    "dark_alley": {
        "name": "薄暗い路地",
        "description": (
            "廃病院の裏口を抜けると、狭い路地が広がる。\n"
            "頭上にはホログラム広告が明滅し、路面には油膜の浮く水たまり。\n"
            "2087年の都市は、腐りかけた未来の匂いがした。"
        ),
        "first_visit": (
            "外の空気が肺に刺さる。\n"
            "高層ビルが空を埋め尽くし、どこかからサイレンの音が聞こえる。\n"
            "急がなければ――そんな確信だけが、本能として残っていた。"
        ),
        "connections": {
            "south": "hospital_room",
            "east": "subway_station",
        },
        "locked_connections": {},
        "items": ["memo", "burner_phone", "ic_card"],
        "events": [],
    },
    "subway_station": {
        "name": "地下鉄駅【区画7-C】",
        "description": (
            "薄暗いホームに監視カメラが無数に並ぶ。赤い点滅光がゆっくりと左右に動く。\n"
            "改札には生体認証スキャナー。人影はまばらだが、どこかに視線を感じる。"
        ),
        "first_visit": (
            "駅に入った瞬間、全身の毛が逆立つ。\n"
            "スーツ姿の男がこちらをじっと見ている。\n"
            "――エージェントだ。直感がそう告げた。"
        ),
        "connections": {
            "west": "dark_alley",
            "south": "factory_basement",
        },
        "locked_connections": {
            "south": {
                "required_flag": "factory_unlocked",
                "locked_text": "地下へ続く通路の扉は電子ロックがかかっている。通行許可証が必要だ。",
            }
        },
        "items": [],
        "events": ["agent_encounter"],
    },
    "factory_basement": {
        "name": "廃工場の地下室",
        "description": (
            "錆びついた機材が並ぶ地下室。空気は淀んでいる。\n"
            "壁を走るケーブルの束。かつてここで何かが行われていた痕跡がある。\n"
            "奥の隅に古い記録機器が置かれている。"
        ),
        "first_visit": (
            "地下へ続く階段を降りると、記憶の断片が頭をよぎる。\n"
            "――ここに来たことがある。そんな気がした。"
        ),
        "connections": {
            "north": "subway_station",
            "up": "rooftop",
        },
        "locked_connections": {
            "up": {
                "required_flag": "rooftop_unlocked",
                "locked_text": "屋上への非常階段は電子ロックがかかっている。アクセスコードが必要だ。",
            }
        },
        "items": ["recorder", "data_chip"],
        "events": [],
    },
    "rooftop": {
        "name": "高層ビルの屋上",
        "description": (
            "都市の夜景が360度広がる。風が強い。\n"
            "中央に衛星通信端末が設置されている。小型だが、特殊な改造が施されている。\n"
            "チップスロットが青く光っている。――これを使えば、すべてを世界に知らせることができる。"
        ),
        "first_visit": (
            "屋上に出た瞬間、記憶が一気に流れ込んできた。\n"
            "あなたはここに来るために戦ってきた。\n"
            "終わりが、近い。"
        ),
        "connections": {
            "down": "factory_basement",
        },
        "locked_connections": {},
        "items": ["satellite_terminal"],
        "events": [],
    },
}
