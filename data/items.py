# アイテムデータ
# fixed: True のアイテムは持ち歩けない（設置物）
# usable: True のアイテムは「使う」コマンドで操作できる
# inspect_event: 「調べる」時に発生するイベントID
# use_event: 「使う」時に発生するイベントID

ITEMS = {
    "wristband": {
        "name": "患者リストバンド",
        "description": (
            "白いプラスチック製のリストバンド。\n"
            "バーコードと管理番号が印刷されている。\n"
            "その下に、かすかに手書きの文字が見える。\n"
            "『K-77 / 記憶消去プロトコル適用済』"
        ),
        "pickup_text": "リストバンドを拾い上げた。",
        "fixed": False,
        "usable": False,
        "inspect_event": "memory_1",
        "use_event": None,
    },
    "syringe": {
        "name": "注射器（空）",
        "description": (
            "透明な液体が残っていた形跡のある使用済み注射器。\n"
            "ラベルには『NEX-R / 神経遮断剤』と印刷されている。\n"
            "――この薬を誰かに打たれた感覚が、かすかに蘇る。"
        ),
        "pickup_text": "注射器を慎重に拾い上げた。",
        "fixed": False,
        "usable": False,
        "inspect_event": "memory_2",
        "use_event": None,
    },
    "memo": {
        "name": "暗号メモ",
        "description": (
            "濡れて滲んだ紙切れ。数字と文字が書き殴られている。\n"
            "『47-ALPHA / 衛星回線 / NEMESIS』\n"
            "――NEMESISという文字を見た瞬間、脳の奥で何かが震えた。"
        ),
        "pickup_text": "メモを拾った。",
        "fixed": False,
        "usable": False,
        "inspect_event": "memory_3",
        "use_event": None,
    },
    "burner_phone": {
        "name": "使い捨て端末",
        "description": (
            "安価な使い捨てスマートフォン。バッテリー残量は僅か。\n"
            "ロック画面にパスワード入力欄がある。\n"
            "――正しいコードを入力すれば、何かにアクセスできるかもしれない。"
        ),
        "pickup_text": "使い捨て端末を拾った。",
        "fixed": False,
        "usable": True,
        "inspect_event": None,
        "use_event": "use_burner_phone",
    },
    "ic_card": {
        "name": "ICカード",
        "description": (
            "地下鉄の定期券型ICカード。名前欄は空白。\n"
            "裏面に小さく『区画7-C 全域通行許可』と刻印されている。"
        ),
        "pickup_text": "ICカードを拾った。",
        "fixed": False,
        "usable": True,
        "inspect_event": None,
        "use_event": "use_ic_card",
    },
    "recorder": {
        "name": "記録装置",
        "description": (
            "手のひらサイズの録音・録画デバイス。外装は傷だらけ。\n"
            "再生ボタンを押すと、かすかに音声が流れ始める。\n"
            "『……NEXUSによる市民監視データは既に1億件を超えた。\n"
            "　政府はこれを知っている。いや――命令したのは政府だ……』\n"
            "ノイズの後、音声は途切れた。"
        ),
        "pickup_text": "記録装置を回収した。",
        "fixed": False,
        "usable": False,
        "inspect_event": "memory_4",
        "use_event": None,
    },
    "data_chip": {
        "name": "証拠データチップ",
        "description": (
            "爪ほどの大きさの記録チップ。\n"
            "――これを見た瞬間、確信した。\n"
            "このチップにすべてが入っている。\n"
            "NEXUSの監視網、政府との秘密契約書、1億人分の個人データ。\n"
            "あなたが命を懸けて隠した、最後の証拠だ。"
        ),
        "pickup_text": "証拠データチップを手に取った。手が震える。",
        "fixed": False,
        "usable": False,
        "inspect_event": "memory_5",
        "use_event": None,
    },
    "satellite_terminal": {
        "name": "衛星通信端末",
        "description": (
            "改造された衛星通信端末。通常の検閲回線を迂回し、\n"
            "直接グローバルネットワークにデータを送信できる。\n"
            "チップスロットが一つ、青く光っている。"
        ),
        "pickup_text": None,  # 持ち歩けない
        "fixed": True,
        "usable": True,
        "inspect_event": None,
        "use_event": "use_satellite_terminal",
    },
}
