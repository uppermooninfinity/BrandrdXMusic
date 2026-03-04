"""
╔══════════════════════════════════════════════════════════════╗
║         🃏 UNO GAME — BrandrdXMusic Plugin                   ║
║   Place in: BrandrdXMusic/plugins/tools/uno.py               ║
║   Prefixes: / and !                                           ║
╚══════════════════════════════════════════════════════════════╝

Commands:
  /uno  or  !uno       — Create a lobby in the group
  /unojoin  !unojoin   — Join the lobby
  /unostart !unostart  — Start (host only, min 2 players)
  /unostop  !unostop   — Force stop (host / admin)

Gameplay:
  • Bot sends actual card STICKERS into the chat
  • Tap "🃏 My Cards" → bot DMs you your hand as stickers
  • Tap the sticker of the card you want to play (via PM buttons)
  • Tap "🎴 Draw" if you can't / won't play
"""

import asyncio
import random
from typing import Dict, List, Optional

from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)

# ── import your bot app ──────────────────────────────────────
from BrandrdXMusic import app

# ════════════════════════════════════════════════════════════
#  STICKER FILE_IDs  (Official Telegram UNO sticker pack)
#  Pack: @unogame  — all 54 unique cards + card back
# ════════════════════════════════════════════════════════════

# Each key  →  "COLOR_VALUE"  e.g. "red_5", "blue_skip", "wild", "wild4"
CARD_STICKERS: Dict[str, str] = {
    # ── RED ──────────────────────────────────────────────────
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
    # ── BLUE ─────────────────────────────────────────────────
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
    # ── GREEN ────────────────────────────────────────────────
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
    # ── YELLOW ───────────────────────────────────────────────
    "yellow_0":   "CAACAgUAAxkBAAIBU2cV5-On_a8yI4MBnuWBSYDfXQACLgADW3kgB3PZR65vH1D5NgQ",
    "yellow_1":   "CAACAgUAAxkBAAIBVWcV5-Tt1Cr6G79lX-Z-aBnwFgACLwADW3kgBwnhbD5YabGZNgQ",
    "yellow_2":   "CAACAgUAAxkBAAIBV2cV5-U9Hry5UUfBrOJeHa0MFQACMAADW3kgBzNJIVf5VV9KNgQ",
    "yellow_3":   "CAACAgUAAxkBAAIBWWcV5-a1wMFKqaJkzPKPTXV5VQACMQADW3kgBzcSRa1AuNhNNgQ",
    "yellow_4":   "CAACAgUAAxkBAAIBW2cV5-fTr3_CYpImTCE8Jl_IZQACMQADW3kgB7pGZfBM-J5bNgQ",
    "yellow_5":   "CAACAgUAAxkBAAIBXWcV5-iFqvALr_v2Nj_-f3XU7AACNAADW3kgBzETHwnMtPPfNgQ",
    "yellow_6":   "CAACAgUAAxkBAAIBX2cV5-mzJWFVJXLbL5VuLH_LugACNQADW3kgByabq9W0C74eNgQ",
    "yellow_7":   "CAACAgUAAxkBAAIBYWcV5-qJE3KPM_hcaHMb45X7UQACNGADW3kgB5d5FJYQNkUjNgQ",
    "yellow_8":   "CAACAgUAAxkBAAIBY2cV5-utXSo6nQfKvOIEf8PjWwACNwADW3kgBzB5UGdNf3EBNgQ",
    "yellow_9":   "CAACAgUAAxkBAAIBZWcV5-yRBV9RRMS1nwH-83r0tAAcOAADW3kgByCxFfHNOb1KNgQ",
    "yellow_skip":"CAACAgUAAxkBAAIBZ2cV5-2PIPbhJKSMiQjJe9Ih5AACOQADw3kgByv7Hy2JRByMNgQ",
    "yellow_rev": "CAACAgUAAxkBAAIBaWcV5-4gvhfnpXHnGCVvkR-LLwACOgADW3kgByS_iBGKisPHNgQ",
    "yellow_d2":  "CAACAgUAAxkBAAIBa2cV5-8DX-kcAAF_VWRlKwnZFDQAAjsAA1t5IAeXuRuFPpb4UTYÉ",
    # ── WILDS ────────────────────────────────────────────────
    "wild":       "CAACAgUAAxkBAAIBbWcV5_CcQ9G2fIMUZGlJU-E7OQACPAADW3kgBxMR0kBNPi8pNgQ",
    "wild4":      "CAACAgUAAxkBAAIBb2cV5_GgpNNQ3T3AHl28Gy9oTwACPQADW3kgBzlNKHMj_XF-NgQ",
    # ── CARD BACK (shown for draw pile) ──────────────────────
    "back":       "CAACAgUAAxkBAAIBcWcV5_Kkck2hFV9IG8RXH3k8UAACQQADW3kgByGpFBmOvU3rNgQ",
}

# ════════════════════════════════════════════════════════════
#  CARD MODEL
# ════════════════════════════════════════════════════════════

COLORS      = ["red", "blue", "green", "yellow"]
COLOR_EMOJI = {"red": "🔴", "blue": "🔵", "green": "🟢", "yellow": "🟡", "": "🌈"}
NUMBERS     = [str(i) for i in range(10)]
ACTIONS     = ["skip", "rev", "d2"]
WILDS       = ["wild", "wild4"]


class Card:
    def __init__(self, color: str, value: str):
        self.color = color   # "red" / "blue" / "green" / "yellow" / "" (wild)
        self.value = value   # "0".."9" / "skip" / "rev" / "d2" / "wild" / "wild4"

    @property
    def key(self) -> str:
        """Lookup key for CARD_STICKERS dict."""
        if self.value in WILDS:
            return self.value
        return f"{self.color}_{self.value}"

    @property
    def sticker(self) -> str:
        return CARD_STICKERS.get(self.key, CARD_STICKERS["back"])

    @property
    def label(self) -> str:
        ce = COLOR_EMOJI.get(self.color, "")
        v = {
            "skip": "Skip ⛔", "rev": "Reverse 🔄",
            "d2": "+2 ✌️", "wild": "Wild 🌈", "wild4": "+4 Wild 🌈"
        }.get(self.value, self.value)
        return f"{ce} {v}".strip()

    def is_wild(self) -> bool:
        return self.value in WILDS

    def playable_on(self, top: "Card") -> bool:
        if self.is_wild():
            return True
        return self.color == top.color or self.value == top.value

    def __repr__(self):
        return self.label


# ════════════════════════════════════════════════════════════
#  DECK BUILDER
# ════════════════════════════════════════════════════════════

def build_deck() -> List[Card]:
    deck = []
    for c in COLORS:
        deck.append(Card(c, "0"))
        for v in NUMBERS[1:] + ACTIONS:
            deck.append(Card(c, v))
            deck.append(Card(c, v))
    for _ in range(4):
        deck.append(Card("", "wild"))
        deck.append(Card("", "wild4"))
    random.shuffle(deck)
    return deck


# ════════════════════════════════════════════════════════════
#  GAME STATE
# ════════════════════════════════════════════════════════════

class UnoGame:
    def __init__(self, chat_id: int, host_id: int, host_name: str):
        self.chat_id    = chat_id
        self.host_id    = host_id
        self.players:      List[int]       = []
        self.names:        Dict[int, str]  = {}
        self.hands:        Dict[int, List[Card]] = {}
        self.deck:         List[Card]      = []
        self.discard:      List[Card]      = []
        self.index:        int             = 0
        self.direction:    int             = 1    # 1 CW / -1 CCW
        self.started:      bool            = False
        self.pending_draw: int             = 0
        # track PM message ids so we can update them
        self.hand_msg_ids: Dict[int, int]  = {}

        self._add(host_id, host_name)

    def _add(self, uid: int, name: str):
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

    def draw(self, uid: int, n: int):
        for _ in range(n):
            if not self.deck:
                self.deck, self.discard = self.discard[:-1], [self.discard[-1]]
                random.shuffle(self.deck)
            if self.deck:
                self.hands[uid].append(self.deck.pop())

    def play(self, uid: int, idx: int, color: str = "") -> dict:
        card = self.hands[uid][idx]
        if card.is_wild():
            if not color:
                return {"ok": False, "msg": "Pick a color first!"}
            card.color = color
        self.hands[uid].pop(idx)
        self.discard.append(card)
        result = {"ok": True, "card": card, "winner": None, "skip": False}
        if not self.hands[uid]:
            result["winner"] = uid
            return result
        if card.value == "skip":
            result["skip"] = True
        elif card.value == "rev":
            self.direction *= -1
            if len(self.players) == 2:
                result["skip"] = True
        elif card.value == "d2":
            self.pending_draw += 2
            result["skip"] = True
        elif card.value == "wild4":
            self.pending_draw += 4
            result["skip"] = True
        return result


# ════════════════════════════════════════════════════════════
#  ACTIVE GAMES
# ════════════════════════════════════════════════════════════

games: Dict[int, UnoGame] = {}

# ════════════════════════════════════════════════════════════
#  KEYBOARD BUILDERS
# ════════════════════════════════════════════════════════════

def join_kb(chat_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("✋ Join",      callback_data=f"uj_{chat_id}"),
        InlineKeyboardButton("▶️ Start Now", callback_data=f"us_{chat_id}"),
    ]])

def color_kb(chat_id: int, uid: int, idx: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("🔴 Red",    callback_data=f"uc_{chat_id}_{uid}_{idx}_red"),
        InlineKeyboardButton("🔵 Blue",   callback_data=f"uc_{chat_id}_{uid}_{idx}_blue"),
    ],[
        InlineKeyboardButton("🟢 Green",  callback_data=f"uc_{chat_id}_{uid}_{idx}_green"),
        InlineKeyboardButton("🟡 Yellow", callback_data=f"uc_{chat_id}_{uid}_{idx}_yellow"),
    ]])

def hand_kb(g: UnoGame, uid: int) -> InlineKeyboardMarkup:
    """
    Each card in hand becomes ONE button showing its emoji label.
    Playable = ✅  Non-playable = ❌
    Two cards per row so stickers sent above them are visually paired.
    """
    hand = g.hands[uid]
    top  = g.top
    rows = []
    row  = []
    for i, card in enumerate(hand):
        can = card.playable_on(top)
        lbl = f"{'✅' if can else '❌'} {card.label}"
        row.append(InlineKeyboardButton(lbl, callback_data=f"up_{g.chat_id}_{uid}_{i}"))
        if len(row) == 2:
            rows.append(row); row = []
    if row:
        rows.append(row)
    rows.append([
        InlineKeyboardButton("🎴 Draw Card",  callback_data=f"ud_{g.chat_id}_{uid}"),
        InlineKeyboardButton("🔄 Refresh",    callback_data=f"ur_{g.chat_id}_{uid}"),
    ])
    return InlineKeyboardMarkup(rows)

def turn_kb(g: UnoGame) -> InlineKeyboardMarkup:
    uid = g.current
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("🃏 View & Play My Cards",
                             callback_data=f"uv_{g.chat_id}_{uid}"),
    ]])

# ════════════════════════════════════════════════════════════
#  HELPERS
# ════════════════════════════════════════════════════════════

def scoreboard(g: UnoGame) -> str:
    lines = []
    for pid in g.players:
        crown = "👑 " if pid == g.host_id else ""
        n = len(g.hands.get(pid, []))
        arrow = " ◀ TURN" if g.started and pid == g.current else ""
        lines.append(f"{crown}{g.names[pid]}  —  {n if g.started else '—'} cards{arrow}")
    return "\n".join(lines)

async def send_hand(client: Client, g: UnoGame, uid: int):
    """DM the player their hand as sticker images + a button row to play."""
    hand = g.hands[uid]
    top  = g.top
    try:
        # Send each card as a sticker
        for i, card in enumerate(hand):
            can = card.playable_on(top)
            caption = f"{'✅ Playable' if can else '❌ Not playable'}  —  {card.label}"
            await client.send_sticker(uid, card.sticker)
            # small delay so they arrive in order
            await asyncio.sleep(0.15)

        # Then one message with all the play buttons
        msg = await client.send_message(
            uid,
            f"🎴 **Top card:** {g.top.label}\n"
            f"You have **{len(hand)}** cards.\n\n"
            "Tap ✅ card to play it, or 🎴 Draw:",
            reply_markup=hand_kb(g, uid),
        )
        g.hand_msg_ids[uid] = msg.id
    except Exception:
        # User hasn't started the bot in PM
        pass

async def notify_turn(client: Client, g: UnoGame):
    uid   = g.current
    name  = g.names[uid]
    pend  = f"\n⚠️ +{g.pending_draw} incoming — stack or accept!" if g.pending_draw else ""
    await client.send_message(
        g.chat_id,
        f"🎯 **{name}'s turn!**\n"
        f"🎴 Top: **{g.top.label}**{pend}\n\n"
        f"{scoreboard(g)}",
        reply_markup=turn_kb(g),
    )

# ════════════════════════════════════════════════════════════
#  MULTI-PREFIX FILTER  ( / and ! )
# ════════════════════════════════════════════════════════════

def cmd(*commands):
    """Accept both /cmd and !cmd in groups."""
    pattern = "^[/!](" + "|".join(commands) + r")(\s|$)"
    return filters.regex(pattern) & filters.group

# ════════════════════════════════════════════════════════════
#  COMMANDS
# ════════════════════════════════════════════════════════════

@app.on_message(cmd("uno"))
async def _cmd_uno(client: Client, msg: Message):
    cid  = msg.chat.id
    user = msg.from_user
    if not user:
        return

    if cid in games:
        g = games[cid]
        if g.started:
            return await msg.reply("⚠️ A game is running. Use /unostop to end it.")
        if user.id in g.players:
            return await msg.reply("You're already in the lobby!")
        g._add(user.id, user.first_name)
        return await msg.reply(
            f"✋ **{user.first_name}** joined!\n\n**Lobby:**\n{scoreboard(g)}",
            reply_markup=join_kb(cid),
        )

    g = UnoGame(cid, user.id, user.first_name)
    games[cid] = g
    await msg.reply(
        f"🃏 **UNO Lobby Created!**\n\n"
        f"👑 Host: **{user.first_name}**\n\n"
        f"**Players:**\n{scoreboard(g)}\n\n"
        "Tap **✋ Join** to enter, **▶️ Start Now** to begin (min 2).",
        reply_markup=join_kb(cid),
    )


@app.on_message(cmd("unojoin"))
async def _cmd_join(client: Client, msg: Message):
    cid  = msg.chat.id
    user = msg.from_user
    if not user:
        return
    if cid not in games:
        return await msg.reply("No active lobby! Use /uno to create one.")
    g = games[cid]
    if g.started:
        return await msg.reply("Game already started.")
    if user.id in g.players:
        return await msg.reply("You're already in!")
    g._add(user.id, user.first_name)
    await msg.reply(
        f"✋ **{user.first_name}** joined!\n\n**Lobby:**\n{scoreboard(g)}",
        reply_markup=join_kb(cid),
    )


@app.on_message(cmd("unostart"))
async def _cmd_start(client: Client, msg: Message):
    cid  = msg.chat.id
    user = msg.from_user
    if cid not in games:
        return await msg.reply("No lobby found. Use /uno first.")
    g = games[cid]
    if g.started:
        return await msg.reply("Already running!")
    if user.id != g.host_id:
        return await msg.reply("Only the host can start.")
    if len(g.players) < 2:
        return await msg.reply("Need at least 2 players!")
    await _begin(client, cid)


@app.on_message(cmd("unostop"))
async def _cmd_stop(client: Client, msg: Message):
    cid  = msg.chat.id
    user = msg.from_user
    if cid not in games:
        return await msg.reply("No active game here.")
    g = games[cid]
    try:
        member = await client.get_chat_member(cid, user.id)
        is_admin = member.status.value in ("administrator", "creator")
    except Exception:
        is_admin = False
    if user.id != g.host_id and not is_admin:
        return await msg.reply("Only the host or an admin can stop the game.")
    del games[cid]
    await msg.reply("🛑 UNO game stopped.")


# ════════════════════════════════════════════════════════════
#  GAME BEGIN
# ════════════════════════════════════════════════════════════

async def _begin(client: Client, chat_id: int):
    g = games[chat_id]
    g.deal()
    g.started = True

    # Send the top card sticker to the group
    await client.send_sticker(chat_id, g.top.sticker)
    await client.send_message(
        chat_id,
        f"🃏 **UNO Starts!**\n\n"
        f"7 cards dealt to each player.\n"
        f"🎴 First card: **{g.top.label}**\n\n"
        f"{scoreboard(g)}\n\n"
        "Tap **🃏 View & Play My Cards** to open your hand in PM!",
        reply_markup=turn_kb(g),
    )


# ════════════════════════════════════════════════════════════
#  CALLBACKS
# ════════════════════════════════════════════════════════════

# ── Join lobby ──────────────────────────────────────────────
@app.on_callback_query(filters.regex(r"^uj_"))
async def _cb_join(client: Client, q: CallbackQuery):
    cid  = int(q.data.split("_")[1])
    user = q.from_user
    if cid not in games:
        return await q.answer("Lobby expired!", show_alert=True)
    g = games[cid]
    if g.started:
        return await q.answer("Game already started!", show_alert=True)
    if user.id in g.players:
        return await q.answer("You're already in!", show_alert=True)
    g._add(user.id, user.first_name)
    await q.answer(f"✅ Joined!")
    await q.message.edit_text(
        f"🃏 **UNO Lobby**\n\n**Players ({len(g.players)}):**\n{scoreboard(g)}\n\n"
        "Tap **✋ Join** or **▶️ Start Now**!",
        reply_markup=join_kb(cid),
    )


# ── Force start ─────────────────────────────────────────────
@app.on_callback_query(filters.regex(r"^us_"))
async def _cb_start(client: Client, q: CallbackQuery):
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
    await q.message.delete()
    await _begin(client, cid)


# ── View hand (sends stickers in PM) ───────────────────────
@app.on_callback_query(filters.regex(r"^uv_"))
async def _cb_view(client: Client, q: CallbackQuery):
    _, _, cid_s, uid_s = q.data.split("_")
    cid = int(cid_s); turn_uid = int(uid_s)
    user = q.from_user
    if cid not in games:
        return await q.answer("Game ended!", show_alert=True)
    g = games[cid]
    if user.id not in g.players:
        return await q.answer("You're not in this game!", show_alert=True)
    if user.id != g.current:
        # Let them peek their hand but warn
        await q.answer("Not your turn — showing your cards anyway!", show_alert=False)
    else:
        await q.answer("Sending your cards in PM! 📬")
    await send_hand(client, g, user.id)


# ── Refresh hand buttons ────────────────────────────────────
@app.on_callback_query(filters.regex(r"^ur_"))
async def _cb_refresh(client: Client, q: CallbackQuery):
    parts = q.data.split("_")
    cid = int(parts[1]); uid = int(parts[2])
    if q.from_user.id != uid:
        return await q.answer("Not your hand!", show_alert=True)
    if cid not in games:
        return await q.answer("Game over!", show_alert=True)
    g = games[cid]
    await q.message.edit_reply_markup(hand_kb(g, uid))
    await q.answer("Refreshed ✅")


# ── Play a card ─────────────────────────────────────────────
@app.on_callback_query(filters.regex(r"^up_"))
async def _cb_play(client: Client, q: CallbackQuery):
    parts = q.data.split("_")
    cid = int(parts[1]); uid = int(parts[2]); idx = int(parts[3])
    user = q.from_user
    if user.id != uid:
        return await q.answer("Not your cards!", show_alert=True)
    if cid not in games:
        return await q.answer("Game ended!", show_alert=True)
    g = games[cid]
    if user.id != g.current:
        return await q.answer("It's not your turn!", show_alert=True)

    hand = g.hands[uid]
    if idx >= len(hand):
        return await q.answer("Card no longer exists, tap Refresh.", show_alert=True)

    card = hand[idx]
    top  = g.top

    if g.pending_draw and card.value not in ("d2", "wild4"):
        return await q.answer(
            f"You must stack a +2/+4 or accept {g.pending_draw} cards!", show_alert=True
        )

    if not card.playable_on(top):
        return await q.answer("❌ Can't play that on the current card!", show_alert=True)

    if card.is_wild():
        # Ask for color in PM
        try:
            await client.send_message(
                uid,
                f"🌈 You played **{card.label}**\nChoose a color:",
                reply_markup=color_kb(cid, uid, idx),
            )
            await q.answer("Choose a color in PM!")
        except Exception:
            await q.message.reply(
                f"🌈 Choose a color for **{card.label}**:",
                reply_markup=color_kb(cid, uid, idx),
            )
            await q.answer("Choose a color!")
        return

    await _execute(client, q, g, user, idx)


# ── Color chosen ────────────────────────────────────────────
@app.on_callback_query(filters.regex(r"^uc_"))
async def _cb_color(client: Client, q: CallbackQuery):
    # uc_{cid}_{uid}_{idx}_{color}
    parts = q.data.split("_")
    cid   = int(parts[1]); uid = int(parts[2])
    idx   = int(parts[3]); color = parts[4]
    user  = q.from_user
    if user.id != uid:
        return await q.answer("Not yours!", show_alert=True)
    if cid not in games:
        return await q.answer("Game ended!", show_alert=True)
    g = games[cid]
    if user.id != g.current:
        return await q.answer("Not your turn!", show_alert=True)
    hand = g.hands[uid]
    if idx >= len(hand):
        return await q.answer("Invalid card.", show_alert=True)
    hand[idx].color = color
    await q.message.delete()
    await _execute(client, q, g, user, idx, color=color)


# ── Draw card ───────────────────────────────────────────────
@app.on_callback_query(filters.regex(r"^ud_"))
async def _cb_draw(client: Client, q: CallbackQuery):
    parts = q.data.split("_")
    cid = int(parts[1]); uid = int(parts[2])
    user = q.from_user
    if user.id != uid:
        return await q.answer("Not your turn!", show_alert=True)
    if cid not in games:
        return await q.answer("Game ended!", show_alert=True)
    g = games[cid]
    if user.id != g.current:
        return await q.answer("Not your turn!", show_alert=True)

    if g.pending_draw:
        n = g.pending_draw; g.pending_draw = 0
        g.draw(uid, n)
        await q.answer(f"Drew {n} cards 😬")
        await client.send_message(
            g.chat_id,
            f"😬 **{g.names[uid]}** draws **{n}** cards and is skipped!\n\n{scoreboard(g)}"
        )
        g.advance()
    else:
        g.draw(uid, 1)
        drawn = g.hands[uid][-1]
        can   = drawn.playable_on(g.top)
        # Send the drawn card as sticker in PM
        try:
            await client.send_sticker(uid, drawn.sticker)
        except Exception:
            pass
        await q.answer(f"Drew: {drawn.label} {'✅' if can else '❌'}")
        await client.send_message(
            g.chat_id,
            f"🎴 **{g.names[uid]}** draws a card.\n"
            f"{'✅ Can play it!' if can else '⏭ Cannot play — turn passes.'}\n\n{scoreboard(g)}"
        )
        if not can:
            g.advance()

    # Refresh PM hand
    try:
        await q.message.edit_reply_markup(hand_kb(g, uid))
    except Exception:
        pass
    await notify_turn(client, g)


# ════════════════════════════════════════════════════════════
#  EXECUTE PLAY  (shared by play & color callbacks)
# ════════════════════════════════════════════════════════════

async def _execute(
    client: Client,
    q: CallbackQuery,
    g: UnoGame,
    user,
    idx: int,
    color: str = "",
):
    result = g.play(user.id, idx, color)
    if not result["ok"]:
        return await q.answer(result["msg"], show_alert=True)

    card = result["card"]

    # ── Send the played card sticker to the GROUP ──────────
    await client.send_sticker(g.chat_id, card.sticker)

    left     = len(g.hands[user.id])
    uno_txt  = "  🔔 **UNO!!**" if left == 1 else ""
    play_txt = f"🎴 **{g.names[user.id]}** played **{card.label}**{uno_txt}\nCards left: **{left}**"

    # ── Winner ─────────────────────────────────────────────
    if result["winner"]:
        if g.chat_id in games:
            del games[g.chat_id]
        await client.send_message(
            g.chat_id,
            f"{play_txt}\n\n🏆 **{g.names[user.id]} wins the game!** 🎉🎊\n\nUse /uno to play again!"
        )
        try:
            await q.message.delete()
        except Exception:
            pass
        return

    await q.answer(f"✅ Played {card.label}!")

    # ── Handle skip / pending draw for next player ─────────
    if result["skip"]:
        g.advance()  # move to next player first
        if g.pending_draw:
            next_uid  = g.current
            next_name = g.names[next_uid]
            g.draw(next_uid, g.pending_draw)
            drew = g.pending_draw; g.pending_draw = 0
            await client.send_message(
                g.chat_id,
                f"{play_txt}\n\n😬 **{next_name}** draws **{drew}** cards and is skipped!\n\n{scoreboard(g)}"
            )
            g.advance()
        else:
            await client.send_message(
                g.chat_id,
                f"{play_txt}\n\n⛔ Next player is skipped!\n\n{scoreboard(g)}"
            )
    else:
        g.advance()
        await client.send_message(g.chat_id, f"{play_txt}\n\n{scoreboard(g)}")

    # Close the PM card menu
    try:
        await q.message.delete()
    except Exception:
        pass

    await notify_turn(client, g)
