# BrandrdXMusic/plugins/tools/uno.py
# ──────────────────────────────────────────────────────────────
#  🃏  UNO GAME  —  Pyrogram v2+  |  BrandrdXMusic plugin
#  Commands (/ and ! prefix both work):
#    /uno        — create lobby
#    /unojoin    — join lobby
#    /unostart   — start game (host only, min 2 players)
#    /unostop    — stop game  (host / admin)
# ──────────────────────────────────────────────────────────────

import asyncio
import random
from typing import Dict, List

from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)

from BrandrdXMusic import app

# ══════════════════════════════════════════════════════════════
#  STICKER FILE_IDs  (Official Telegram UNO sticker pack)
# ══════════════════════════════════════════════════════════════
CARD_STICKERS: Dict[str, str] = {
    # RED
    "red_0":      "CAACAgUAAxkBAAIBBWcV5xyNPzNDm6mLBkjeJSXMexBFAAIGAANWHiAH7PfHGjFOaYI2BA",
    "red_1":      "CAACAgUAAxkBAAIBB2cV5x1dDf0KJ0XPd2YHfg7JAQACBQADW3kgBySPAw4HFsYoNgQ",
    "red_2":      "CAACAgUAAxkBAAIBCWcV5x6z8PkXEeJY5pJDxX8r5wACBwADW3kgBzRQUYT8xzHFNgQ",
    "red_3":      "CAACAgUAAxkBAAIBC2cV5x-W2wuKYwlM5kaaLPD77gACCAADW3kgB9MdHxGCJKMvNgQ",
    "red_4":      "CAACAgUAAxkBAAIBDWcV5yBK5I9I8BjbZ4C2rTj7agACCQADW3kgBwnHLM8kPJLVNgQ",
    "red_5":      "CAACAgUAAxkBAAIBD2cV5yGPDj_E9Xf2a5TXIlH5VgACCgADW3kgByNm4NWz82A3NgQ",
    "red_6":      "CAACAgUAAxkBAAIBEWcV5yL5BqXBaJFlxiKjGEZJcQACCwADW3kgB2OA5D77JkFbNgQ",
    "red_7":      "CAACAgUAAxkBAAIBE2cV5yOz0sY9M_XnZ3b8uuVWywACDAADW3kgByTq02KJJ3FKNgQ",
    "red_8":      "CAACAgUAAxkBAAIBFWcV5ySRu3EpO7qslMoFrqlsaQACDQADW3kgBylFMoM8fLNKNgQ",
    "red_9":      "CAACAgUAAxkBAAIBF2cV5yVwH6k6A3FiWZE6u1mtzwACDgADW3kgB7qiAAFLZ2-BJzYE",
    "red_skip":   "CAACAgUAAxkBAAIBGWcV5yb98oD_ZNExGfyEPT_BTAACEOADW3kgB_BqLW3MwVl_NgQ",
    "red_rev":    "CAACAgUAAxkBAAIBG2cV5yeHjwLWkPSHkS5uoT6PxwACEQADW3kgB_kT0g0LLtWfNgQ",
    "red_d2":     "CAACAgUAAxkBAAIBHWcV5yhWS-Tma7Vm-1mBJ4-FdAACEgADW3kgB21ZfDmCuWNGNgQ",
    # BLUE
    "blue_0":     "CAACAgUAAxkBAAIBH2cV5ympGv7sYHd_KjPoYKGp1QACEwADW3kgBzJlsrP4IaxYNgQ",
    "blue_1":     "CAACAgUAAxkBAAIBIWcV5yoTxVMMrPRbgH7WNLF2ZAACFAADW3kgBzNJEqIFPsMZNgQ",
    "blue_2":     "CAACAgUAAxkBAAIBI2cV5ytTfaLSDvXB3R3OmD7WFQACFQADW3kgBwvMDaLGc-kXNgQ",
    "blue_3":     "CAACAgUAAxkBAAIBJWcV5yx5RoCvH6N_p4eM2wPbLwACFgADW3kgB5jJFz9q49RLNgQ",
    "blue_4":     "CAACAgUAAxkBAAIBJ2cV5y3AyH0c_hy7yy9lS1J2PQACGAADW3kgB4JEcBlhgJc7NgQ",
    "blue_5":     "CAACAgUAAxkBAAIBKWcV5y5fBJtIPrj4yE_hgPZKRQACGQADW3kgByeS8-R7IxaBNgQ",
    "blue_6":     "CAACAgUAAxkBAAIBK2cV5y_1hD8PnW7vl3VIDpjEJQACGgADW3kgB0cNRvqf9n5qNgQ",
    "blue_7":     "CAACAgUAAxkBAAIBLWcV5zBP7jx0P_XRhD85Iu1AGQACHAADW3kgB-wY06dJn4RUNgQ",
    "blue_8":     "CAACAgUAAxkBAAIBL2cV5zGn2cV2Ieh-0G7kJcMrggACHQADW3kgByRpZHaWJB59NgQ",
    "blue_9":     "CAACAgUAAxkBAAIBMWcV5zJb9qX5jhLLH2Bfi9GpQQACHgADW3kgBxk3UXN6_GglNgQ",
    "blue_skip":  "CAACAgUAAxkBAAIBM2cV5zMzY_e2NlFuPqvBz0H4hQACHwADW3kgB6M_iRBTMHBNNgQ",
    "blue_rev":   "CAACAgUAAxkBAAIBNWcV5zRbbV3pkpqoHfuqRcEEqQACIAADW3kgBxeZ4XOIJm-YNgQ",
    "blue_d2":    "CAACAgUAAxkBAAIBN2cV5zW1Y2lJixdZZyW_yBXtpAACIQADW3kgB97GVmMxfwHXNgQ",
    # GREEN
    "green_0":    "CAACAgUAAxkBAAIBOWcV5zaEKY0lS3uXb1vEo8cqSQACIgADW3kgBzaS_S7FTJWjNgQ",
    "green_1":    "CAACAgUAAxkBAAIBO2cV5zdUr4g5F0hW35bhsDNshAACIwADW3kgB6LYAAFz8DRvkjYE",
    "green_2":    "CAACAgUAAxkBAAIBPWcV5zhJfOFYMtLHCp6YHtSSzAACJAADW3kgBwJJ7d8BijCJNgQ",
    "green_3":    "CAACAgUAAxkBAAIBP2cV5zlLb1kGfpnnHV5dFl6-TwACJQADW3kgBxJfZy9q07l5NgQ",
    "green_4":    "CAACAgUAAxkBAAIBQWcV5zr5cpVDuJfzn1K4u3l8nAACJgADW3kgBxMRZ4EBFumxNgQ",
    "green_5":    "CAACAgUAAxkBAAIBQ2cV5zt5rGKLhLaR_y7beBTArgACJwADW3kgB-E-OfzIuiDINgQ",
    "green_6":    "CAACAgUAAxkBAAIBRWcV5zyMwWsLfHNq3vPJQHK5JQACKAAAW3kgB5KHD0JRm6OhNgQ",
    "green_7":    "CAACAgUAAxkBAAIBR2cV5z2LvNXV4rOLJN5W-Wz3FQACKQADw3kgByFChYdYM8GJNgQ",
    "green_8":    "CAACAgUAAxkBAAIBSWcV5z6mwOPeIVKFk3vAXuL3OQACKQADW3kgByAWsX0W17xlNgQ",
    "green_9":    "CAACAgUAAxkBAAIBS2cV5z_d-VKPL2I-A_MkXPCYHQACKgADW3kgB5Wx4DJTkLx2NgQ",
    "green_skip": "CAACAgUAAxkBAAIBTWcV5-COdOaIgdilzuv6bFNZmAACKwADW3kgB_rL7jMZD04dNgQ",
    "green_rev":  "CAACAgUAAxkBAAIBT2cV5-GG-PsIjl2C4_bFO9c4eAACLAADW3kgBzM6Q_9HqFibNgQ",
    "green_d2":   "CAACAgUAAxkBAAIBUWcV5-Kc3OBN3fhKYPaWJ8g3GQACLQADW3kgB0pJ44hnvPFdNgQ",
    # YELLOW
    "yellow_0":   "CAACAgUAAxkBAAIBU2cV5-On_a8yI4MBnuWBSYDfXQACLgADW3kgB3PZR65vH1D5NgQ",
    "yellow_1":   "CAACAgUAAxkBAAIBVWcV5-Tt1Cr6G79lX-Z-aBnwFgACLwADW3kgBwnhbD5YabGZNgQ",
    "yellow_2":   "CAACAgUAAxkBAAIBV2cV5-U9Hry5UUfBrOJeHa0MFQACMAADW3kgBzNJIVf5VV9KNgQ",
    "yellow_3":   "CAACAgUAAxkBAAIBWWcV5-a1wMFKqaJkzPKPTXV5VQACMQADW3kgBzcSRa1AuNhNNgQ",
    "yellow_4":   "CAACAgUAAxkBAAIBW2cV5-fTr3_CYpImTCE8Jl_IZQACMQADW3kgB7pGZfBM-J5bNgQ",
    "yellow_5":   "CAACAgUAAxkBAAIBXWcV5-iFqvALr_v2Nj_-f3XU7AACNAADW3kgBzETHwnMtPPfNgQ",
    "yellow_6":   "CAACAgUAAxkBAAIBX2cV5-mzJWFVJXLbL5VuLH_LugACNQADW3kgByabq9W0C74eNgQ",
    "yellow_7":   "CAACAgUAAxkBAAIBYWcV5-qJE3KPM_hcaHMb45X7UQACMGADW3kgB5d5FJYQNkUjNgQ",
    "yellow_8":   "CAACAgUAAxkBAAIBY2cV5-utXSo6nQfKvOIEf8PjWwACNwADW3kgBzB5UGdNf3EBNgQ",
    "yellow_9":   "CAACAgUAAxkBAAIBZWcV5-yRBV9RRMS1nwH-83r0tAAcOAADW3kgByCxFfHNOb1KNgQ",
    "yellow_skip":"CAACAgUAAxkBAAIBZ2cV5-2PIPbhJKSMiQjJe9Ih5AACOQADw3kgByv7Hy2JRByMNgQ",
    "yellow_rev": "CAACAgUAAxkBAAIBaWcV5-4gvhfnpXHnGCVvkR-LLwACOgADW3kgByS_iBGKisPHNgQ",
    "yellow_d2":  "CAACAgUAAxkBAAIBa2cV5-8DX-kcAAF_VWRlKwnZFDQAAjsAA1t5IAeXuRuFPpb4UTY",
    # WILDS
    "wild":       "CAACAgUAAxkBAAIBbWcV5_CcQ9G2fIMUZGlJU-E7OQACPAADW3kgBxMR0kBNPi8pNgQ",
    "wild4":      "CAACAgUAAxkBAAIBb2cV5_GgpNNQ3T3AHl28Gy9oTwACPQADW3kgBzlNKHMj_XF-NgQ",
    # CARD BACK
    "back":       "CAACAgUAAxkBAAIBcWcV5_Kkck2hFV9IG8RXH3k8UAACQQADW3kgByGpFBmOvU3rNgQ",
}

# ══════════════════════════════════════════════════════════════
#  CARD + DECK
# ══════════════════════════════════════════════════════════════
COLORS      = ["red", "blue", "green", "yellow"]
COLOR_EMOJI = {"red": "🔴", "blue": "🔵", "green": "🟢", "yellow": "🟡", "": "🌈"}
NUMBERS     = [str(i) for i in range(10)]
ACTIONS     = ["skip", "rev", "d2"]
WILDS       = ["wild", "wild4"]
LABEL_MAP   = {
    "skip": "Skip ⛔", "rev": "Reverse 🔄",
    "d2": "+2", "wild": "Wild 🌈", "wild4": "+4 Wild 🌈"
}


class Card:
    def __init__(self, color: str, value: str):
        self.color = color
        self.value = value

    @property
    def key(self):
        return self.value if self.value in WILDS else f"{self.color}_{self.value}"

    @property
    def sticker(self):
        return CARD_STICKERS.get(self.key, CARD_STICKERS["back"])

    @property
    def label(self):
        e = COLOR_EMOJI.get(self.color, "")
        v = LABEL_MAP.get(self.value, self.value)
        return f"{e} {v}".strip()

    def is_wild(self):
        return self.value in WILDS

    def playable_on(self, top: "Card"):
        if self.is_wild():
            return True
        return self.color == top.color or self.value == top.value


def build_deck() -> List[Card]:
    deck = []
    for c in COLORS:
        deck.append(Card(c, "0"))
        for v in NUMBERS[1:] + ACTIONS:
            deck += [Card(c, v), Card(c, v)]
    for _ in range(4):
        deck += [Card("", "wild"), Card("", "wild4")]
    random.shuffle(deck)
    return deck


# ══════════════════════════════════════════════════════════════
#  GAME STATE
# ══════════════════════════════════════════════════════════════
class UnoGame:
    def __init__(self, chat_id: int, host_id: int, host_name: str):
        self.chat_id       = chat_id
        self.host_id       = host_id
        self.players:      List[int]             = []
        self.names:        Dict[int, str]        = {}
        self.hands:        Dict[int, List[Card]] = {}
        self.deck:         List[Card]            = []
        self.discard:      List[Card]            = []
        self.index:        int                   = 0
        self.direction:    int                   = 1
        self.started:      bool                  = False
        self.pending_draw: int                   = 0
        self._join(host_id, host_name)

    def _join(self, uid: int, name: str):
        if uid not in self.players:
            self.players.append(uid)
            self.names[uid] = name

    def deal(self):
        self.deck = build_deck()
        for p in self.players:
            self.hands[p] = [self.deck.pop() for _ in range(7)]
        while True:
            top = self.deck.pop()
            if not top.is_wild() and top.value in NUMBERS:
                self.discard = [top]
                break
            self.deck.insert(0, top)

    @property
    def top(self) -> Card:
        return self.discard[-1]

    @property
    def current(self) -> int:
        return self.players[self.index]

    def advance(self, skip=False):
        steps = 2 if skip else 1
        self.index = (self.index + self.direction * steps) % len(self.players)

    def draw_cards(self, uid: int, n: int):
        for _ in range(n):
            if not self.deck:
                self.deck    = self.discard[:-1]
                self.discard = [self.discard[-1]]
                random.shuffle(self.deck)
            if self.deck:
                self.hands[uid].append(self.deck.pop())

    def play_card(self, uid: int, idx: int, color: str = "") -> dict:
        card = self.hands[uid][idx]
        if card.is_wild():
            if not color:
                return {"ok": False, "msg": "Pick a color first!"}
            card.color = color
        self.hands[uid].pop(idx)
        self.discard.append(card)
        res = {"ok": True, "card": card, "winner": None, "skip": False}
        if not self.hands[uid]:
            res["winner"] = uid
            return res
        if card.value == "skip":
            res["skip"] = True
        elif card.value == "rev":
            self.direction *= -1
            if len(self.players) == 2:
                res["skip"] = True
        elif card.value == "d2":
            self.pending_draw += 2
            res["skip"] = True
        elif card.value == "wild4":
            self.pending_draw += 4
            res["skip"] = True
        return res


# ══════════════════════════════════════════════════════════════
#  ACTIVE GAMES  { chat_id: UnoGame }
# ══════════════════════════════════════════════════════════════
games: Dict[int, UnoGame] = {}


# ══════════════════════════════════════════════════════════════
#  KEYBOARDS
# ══════════════════════════════════════════════════════════════
def join_kb(cid: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("✋ Join Game",  callback_data=f"unojoin_{cid}"),
        InlineKeyboardButton("▶️ Start Now", callback_data=f"unostart_{cid}"),
    ]])


def turn_kb(g: UnoGame) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(
            "🃏 View & Play My Cards",
            callback_data=f"unoview_{g.chat_id}_{g.current}"
        )
    ]])


def hand_kb(g: UnoGame, uid: int) -> InlineKeyboardMarkup:
    hand = g.hands[uid]
    top  = g.top
    rows = []
    row  = []
    for i, card in enumerate(hand):
        can = card.playable_on(top)
        lbl = f"{'✅' if can else '❌'} {card.label}"
        row.append(InlineKeyboardButton(lbl, callback_data=f"unoplay_{g.chat_id}_{uid}_{i}"))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([
        InlineKeyboardButton("🎴 Draw Card", callback_data=f"unodraw_{g.chat_id}_{uid}"),
        InlineKeyboardButton("🔄 Refresh",   callback_data=f"unopeek_{g.chat_id}_{uid}"),
    ])
    return InlineKeyboardMarkup(rows)


def color_kb(cid: int, uid: int, idx: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("🔴 Red",    callback_data=f"unocolor_{cid}_{uid}_{idx}_red"),
        InlineKeyboardButton("🔵 Blue",   callback_data=f"unocolor_{cid}_{uid}_{idx}_blue"),
    ],[
        InlineKeyboardButton("🟢 Green",  callback_data=f"unocolor_{cid}_{uid}_{idx}_green"),
        InlineKeyboardButton("🟡 Yellow", callback_data=f"unocolor_{cid}_{uid}_{idx}_yellow"),
    ]])


# ══════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════
def scoreboard(g: UnoGame) -> str:
    lines = []
    for pid in g.players:
        crown = "👑 " if pid == g.host_id else "👤 "
        n     = len(g.hands.get(pid, []))
        arrow = "  ◀️ TURN" if g.started and pid == g.current else ""
        info  = f"{n} card{'s' if n != 1 else ''}" if g.started else "waiting"
        lines.append(f"{crown}{g.names[pid]}  —  {info}{arrow}")
    return "\n".join(lines)


async def send_hand_pm(client: Client, g: UnoGame, uid: int):
    """DM all cards as stickers + one control message with play buttons."""
    hand = g.hands[uid]
    top  = g.top
    try:
        await client.send_message(
            uid,
            f"🃏 **Your Hand** — {len(hand)} cards\n"
            f"🎴 Top card: **{top.label}**\n\n"
            "Your cards incoming 👇  (✅ = playable)"
        )
        for card in hand:
            await client.send_sticker(uid, card.sticker)
            await asyncio.sleep(0.1)
        await client.send_message(
            uid,
            "Tap the card you want to play:",
            reply_markup=hand_kb(g, uid),
        )
    except Exception:
        pass  # user hasn't started the bot in PM


async def notify_turn(client: Client, g: UnoGame):
    uid  = g.current
    name = g.names[uid]
    pend = f"\n⚠️ **+{g.pending_draw}** cards incoming — stack or accept!" if g.pending_draw else ""
    await client.send_sticker(g.chat_id, g.top.sticker)
    await client.send_message(
        g.chat_id,
        f"🎯 **{name}'s turn!**{pend}\n\n{scoreboard(g)}",
        reply_markup=turn_kb(g),
    )


# ══════════════════════════════════════════════════════════════
#  COMMANDS  ← THE ROOT FIX: prefixes=["/", "!"]
# ══════════════════════════════════════════════════════════════

@app.on_message(filters.command("uno", prefixes=["/", "!"]) & filters.group)
async def cmd_uno(client: Client, message: Message):
    cid  = message.chat.id
    user = message.from_user
    if not user:
        return

    if cid in games:
        g = games[cid]
        if g.started:
            return await message.reply("⚠️ A game is already running! Use /unostop to end it.")
        if user.id in g.players:
            return await message.reply("You're already in the lobby!")
        g._join(user.id, user.first_name)
        return await message.reply(
            f"✋ **{user.first_name}** joined!\n\n**Players ({len(g.players)}):**\n{scoreboard(g)}",
            reply_markup=join_kb(cid),
        )

    g = UnoGame(cid, user.id, user.first_name)
    games[cid] = g
    await message.reply(
        f"🃏 **UNO Lobby Created!**\n\n"
        f"👑 Host: **{user.first_name}**\n\n"
        f"**Players:**\n{scoreboard(g)}\n\n"
        "Tap **✋ Join Game** to enter.\n"
        "Tap **▶️ Start Now** when everyone's in _(min 2 players)_.",
        reply_markup=join_kb(cid),
    )


@app.on_message(filters.command("unojoin", prefixes=["/", "!"]) & filters.group)
async def cmd_unojoin(client: Client, message: Message):
    cid  = message.chat.id
    user = message.from_user
    if not user:
        return
    if cid not in games:
        return await message.reply("No active lobby! Use /uno to create one.")
    g = games[cid]
    if g.started:
        return await message.reply("Game already started, wait for the next round!")
    if user.id in g.players:
        return await message.reply("You're already in!")
    g._join(user.id, user.first_name)
    await message.reply(
        f"✋ **{user.first_name}** joined!\n\n**Players ({len(g.players)}):**\n{scoreboard(g)}",
        reply_markup=join_kb(cid),
    )


@app.on_message(filters.command("unostart", prefixes=["/", "!"]) & filters.group)
async def cmd_unostart(client: Client, message: Message):
    cid  = message.chat.id
    user = message.from_user
    if cid not in games:
        return await message.reply("No lobby! Use /uno first.")
    g = games[cid]
    if g.started:
        return await message.reply("Game is already running!")
    if user.id != g.host_id:
        return await message.reply("Only the host can start the game!")
    if len(g.players) < 2:
        return await message.reply("Need at least 2 players!")
    await begin_game(client, cid)


@app.on_message(filters.command("unostop", prefixes=["/", "!"]) & filters.group)
async def cmd_unostop(client: Client, message: Message):
    cid  = message.chat.id
    user = message.from_user
    if cid not in games:
        return await message.reply("No active UNO game here.")
    g = games[cid]
    try:
        member   = await client.get_chat_member(cid, user.id)
        is_admin = member.status.value in ("administrator", "creator")
    except Exception:
        is_admin = False
    if user.id != g.host_id and not is_admin:
        return await message.reply("Only the host or an admin can stop the game!")
    del games[cid]
    await message.reply("🛑 UNO game has been stopped.")


# ══════════════════════════════════════════════════════════════
#  BEGIN GAME
# ══════════════════════════════════════════════════════════════
async def begin_game(client: Client, chat_id: int):
    g = games[chat_id]
    g.deal()
    g.started = True
    await client.send_sticker(chat_id, g.top.sticker)
    await client.send_message(
        chat_id,
        f"🃏 **UNO Game Started!**\n\n"
        f"7 cards dealt to each player.\n"
        f"🎴 Starting card: **{g.top.label}**\n\n"
        f"{scoreboard(g)}\n\n"
        "Tap **🃏 View & Play My Cards** to see your hand in DM!\n"
        "_(Start the bot in PM first if you haven't already)_",
        reply_markup=turn_kb(g),
    )


# ══════════════════════════════════════════════════════════════
#  CALLBACKS
# ══════════════════════════════════════════════════════════════

@app.on_callback_query(filters.regex(r"^unojoin_(-?\d+)$"))
async def cb_join(client: Client, q: CallbackQuery):
    cid  = int(q.data.split("_")[1])
    user = q.from_user
    if cid not in games:
        return await q.answer("Lobby expired!", show_alert=True)
    g = games[cid]
    if g.started:
        return await q.answer("Game already started!", show_alert=True)
    if user.id in g.players:
        return await q.answer("You're already in!", show_alert=True)
    g._join(user.id, user.first_name)
    await q.answer("✅ You joined the game!")
    await q.message.edit_text(
        f"🃏 **UNO Lobby**\n\n"
        f"**Players ({len(g.players)}):**\n{scoreboard(g)}\n\n"
        "Tap **✋ Join Game** or **▶️ Start Now**!",
        reply_markup=join_kb(cid),
    )


@app.on_callback_query(filters.regex(r"^unostart_(-?\d+)$"))
async def cb_forcestart(client: Client, q: CallbackQuery):
    cid  = int(q.data.split("_")[1])
    user = q.from_user
    if cid not in games:
        return await q.answer("No lobby!", show_alert=True)
    g = games[cid]
    if g.started:
        return await q.answer("Already started!", show_alert=True)
    if user.id != g.host_id:
        return await q.answer("Only the host can start!", show_alert=True)
    if len(g.players) < 2:
        return await q.answer("Need at least 2 players!", show_alert=True)
    try:
        await q.message.delete()
    except Exception:
        pass
    await begin_game(client, cid)


@app.on_callback_query(filters.regex(r"^unoview_(-?\d+)_(\d+)$"))
async def cb_view(client: Client, q: CallbackQuery):
    parts = q.data.split("_")
    cid   = int(parts[1])
    user  = q.from_user
    if cid not in games:
        return await q.answer("Game ended!", show_alert=True)
    g = games[cid]
    if user.id not in g.players:
        return await q.answer("You're not in this game!", show_alert=True)
    if user.id != g.current:
        await q.answer("Not your turn — showing cards anyway!", show_alert=False)
    else:
        await q.answer("Sending cards to your PM 📬")
    await send_hand_pm(client, g, user.id)


@app.on_callback_query(filters.regex(r"^unopeek_(-?\d+)_(\d+)$"))
async def cb_peek(client: Client, q: CallbackQuery):
    parts = q.data.split("_")
    cid   = int(parts[1])
    uid   = int(parts[2])
    if q.from_user.id != uid:
        return await q.answer("Not your hand!", show_alert=True)
    if cid not in games:
        return await q.answer("Game ended!", show_alert=True)
    g = games[cid]
    try:
        await q.message.edit_reply_markup(hand_kb(g, uid))
    except Exception:
        pass
    await q.answer("Refreshed ✅")


@app.on_callback_query(filters.regex(r"^unoplay_(-?\d+)_(\d+)_(\d+)$"))
async def cb_play(client: Client, q: CallbackQuery):
    parts = q.data.split("_")
    cid   = int(parts[1])
    uid   = int(parts[2])
    idx   = int(parts[3])
    user  = q.from_user
    if user.id != uid:
        return await q.answer("These aren't your cards!", show_alert=True)
    if cid not in games:
        return await q.answer("Game ended!", show_alert=True)
    g = games[cid]
    if user.id != g.current:
        return await q.answer("It's not your turn!", show_alert=True)
    hand = g.hands[uid]
    if idx >= len(hand):
        return await q.answer("Card gone — tap 🔄 Refresh!", show_alert=True)
    card = hand[idx]
    if g.pending_draw and card.value not in ("d2", "wild4"):
        return await q.answer(
            f"Must stack a +2/+4 or accept {g.pending_draw} cards!", show_alert=True
        )
    if not card.playable_on(g.top):
        return await q.answer("❌ That card can't be played right now!", show_alert=True)
    if card.is_wild():
        try:
            await client.send_message(
                uid,
                f"🌈 You played **{card.label}**\nChoose a color:",
                reply_markup=color_kb(cid, uid, idx),
            )
            await q.answer("Pick a color in your PM!")
        except Exception:
            await q.message.reply(
                f"🌈 **{user.first_name}**, choose a color for **{card.label}**:",
                reply_markup=color_kb(cid, uid, idx),
            )
            await q.answer("Pick a color!")
        return
    await do_play(client, q, g, user, idx)


@app.on_callback_query(filters.regex(r"^unocolor_(-?\d+)_(\d+)_(\d+)_(\w+)$"))
async def cb_color(client: Client, q: CallbackQuery):
    parts = q.data.split("_")
    cid   = int(parts[1])
    uid   = int(parts[2])
    idx   = int(parts[3])
    color = parts[4]
    user  = q.from_user
    if user.id != uid:
        return await q.answer("Not your card!", show_alert=True)
    if cid not in games:
        return await q.answer("Game ended!", show_alert=True)
    g = games[cid]
    if user.id != g.current:
        return await q.answer("Not your turn!", show_alert=True)
    hand = g.hands[uid]
    if idx >= len(hand):
        return await q.answer("Invalid card!", show_alert=True)
    hand[idx].color = color
    try:
        await q.message.delete()
    except Exception:
        pass
    await do_play(client, q, g, user, idx, color=color)


@app.on_callback_query(filters.regex(r"^unodraw_(-?\d+)_(\d+)$"))
async def cb_draw(client: Client, q: CallbackQuery):
    parts = q.data.split("_")
    cid   = int(parts[1])
    uid   = int(parts[2])
    user  = q.from_user
    if user.id != uid:
        return await q.answer("Not your turn!", show_alert=True)
    if cid not in games:
        return await q.answer("Game ended!", show_alert=True)
    g = games[cid]
    if user.id != g.current:
        return await q.answer("Not your turn!", show_alert=True)

    if g.pending_draw:
        n = g.pending_draw
        g.pending_draw = 0
        g.draw_cards(uid, n)
        await q.answer(f"Drew {n} cards 😬")
        await client.send_message(
            g.chat_id,
            f"😬 **{g.names[uid]}** accepts and draws **{n}** cards — turn skipped!\n\n{scoreboard(g)}"
        )
        g.advance()
    else:
        g.draw_cards(uid, 1)
        drawn = g.hands[uid][-1]
        can   = drawn.playable_on(g.top)
        try:
            await client.send_sticker(uid, drawn.sticker)
        except Exception:
            pass
        await q.answer(f"Drew: {drawn.label} {'✅' if can else '❌'}")
        await client.send_message(
            g.chat_id,
            f"🎴 **{g.names[uid]}** draws a card.\n"
            f"{'✅ Can play it!' if can else '⏭️ Cannot play it — turn passes.'}\n\n{scoreboard(g)}"
        )
        if not can:
            g.advance()

    try:
        await q.message.edit_reply_markup(hand_kb(g, uid))
    except Exception:
        pass
    await notify_turn(client, g)


# ══════════════════════════════════════════════════════════════
#  SHARED PLAY EXECUTOR
# ══════════════════════════════════════════════════════════════
async def do_play(
    client: Client, q: CallbackQuery,
    g: UnoGame, user, idx: int, color: str = ""
):
    res = g.play_card(user.id, idx, color)
    if not res["ok"]:
        return await q.answer(res["msg"], show_alert=True)

    card     = res["card"]
    left     = len(g.hands[user.id])
    uno_bang = "  🔔 **UNO!!**" if left == 1 else ""
    play_txt = (
        f"🎴 **{g.names[user.id]}** played **{card.label}**{uno_bang}\n"
        f"└ {left} card{'s' if left != 1 else ''} remaining"
    )

    # Send played card sticker to the GROUP for everyone to see
    await client.send_sticker(g.chat_id, card.sticker)

    if res["winner"]:
        games.pop(g.chat_id, None)
        await client.send_message(
            g.chat_id,
            f"{play_txt}\n\n🏆 **{g.names[user.id]} wins the UNO game!** 🎉🎊\n\nUse /uno to play again!"
        )
        try:
            await q.message.delete()
        except Exception:
            pass
        return

    await q.answer(f"✅ Played {card.label}!")

    if res["skip"]:
        g.advance()
        if g.pending_draw:
            nxt  = g.current
            nxtn = g.names[nxt]
            g.draw_cards(nxt, g.pending_draw)
            drew           = g.pending_draw
            g.pending_draw = 0
            await client.send_message(
                g.chat_id,
                f"{play_txt}\n\n😬 **{nxtn}** draws **{drew}** cards and is skipped!\n\n{scoreboard(g)}"
            )
            g.advance()
        else:
            await client.send_message(
                g.chat_id,
                f"{play_txt}\n\n⛔ Next player is **skipped**!\n\n{scoreboard(g)}"
            )
    else:
        g.advance()
        await client.send_message(g.chat_id, f"{play_txt}\n\n{scoreboard(g)}")

    try:
        await q.message.delete()
    except Exception:
        pass

    await notify_turn(client, g)
