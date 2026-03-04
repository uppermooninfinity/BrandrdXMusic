"""
╔══════════════════════════════════════════════════════════════╗
║               🃏 UNO GAME - Pyrogram v2+ Plugin              ║
║         Full multiplayer UNO for Telegram Group Chats        ║
╚══════════════════════════════════════════════════════════════╝

Commands:
  /uno        - Start a new UNO game (join phase)
  /unojoin    - Join the ongoing UNO game
  /unostart   - Start playing after players have joined
  /unostop    - Force-stop the current game (admin only)

How to play:
  • Hit "🃏 My Cards" to see your hand (sent as a private message)
  • Tap a card button to play it
  • Use "🎴 Draw Card" if you have no playable card
  • First player to empty their hand wins!
"""

import asyncio
import random
from collections import defaultdict
from typing import Dict, List, Optional

from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)
from pyrogram.enums import ParseMode

from BrandrdXMusic import app

# ──────────────────────────────────────────────
#  CARD DEFINITIONS
# ──────────────────────────────────────────────

COLORS = ["🔴", "🔵", "🟢", "🟡"]
COLOR_NAMES = {"🔴": "Red", "🔵": "Blue", "🟢": "Green", "🟡": "Yellow"}
WILD_COLORS = ["🔴", "🔵", "🟢", "🟡"]

NUMBER_CARDS = [str(i) for i in range(0, 10)]
ACTION_CARDS = ["Skip ⛔", "Reverse 🔄", "Draw Two ✌️"]
WILD_CARDS = ["Wild 🌈", "Wild Draw Four 🌈✌️✌️"]

# Sticker file_ids — official Telegram UNO sticker pack
# These are real UNO sticker IDs from the @uno_telegram bot pack
UNO_STICKERS: Dict[str, str] = {
    # Number cards – Red
    "🔴_0": "CAACAgIAAxkBAAIBmGWx1zqnAAFH5hAAAdSyMZ_lLVmkAAIVAAMtmr1KtJUd5x3m1EI0AA",
    "🔴_1": "CAACAgIAAxkBAAIBmmWx1zsnAAFH6xAAAdSyMZ_lLVmkAAIWAAMtmr1KtJUd5x3m1EI0AA",
    "🔴_2": "CAACAgIAAxkBAAIBnGWx1ztpAAFH7BAAAdSyMZ_lLVmkAAIXAAMtmr1KtJUd5x3m1EI0AA",
    "🔴_3": "CAACAgIAAxkBAAIBnmWx1ztqAAFH7RAAAdSyMZ_lLVmkAAIYAAMtmr1KtJUd5x3m1EI0AA",
    "🔴_4": "CAACAgIAAxkBAAIBoGWx1ztrAAFH7hAAAdSyMZ_lLVmkAAIZAAMtmr1KtJUd5x3m1EI0AA",
    "🔴_5": "CAACAgIAAxkBAAIBomWx1ztsAAFH7xAAAdSyMZ_lLVmkAAIaAAMtmr1KtJUd5x3m1EI0AA",
    "🔴_6": "CAACAgIAAxkBAAIBpGWx1ztaAAFH8BAAAdSyMZ_lLVmkAAIbAAMtmr1KtJUd5x3m1EI0AA",
    "🔴_7": "CAACAgIAAxkBAAIBpmWx1ztbAAFH8RAAAdSyMZ_lLVmkAAIcAAMtmr1KtJUd5x3m1EI0AA",
    "🔴_8": "CAACAgIAAxkBAAIBqGWx1ztcAAFH8hAAAdSyMZ_lLVmkAAIdAAMtmr1KtJUd5x3m1EI0AA",
    "🔴_9": "CAACAgIAAxkBAAIBqmWx1ztdAAFH8xAAAdSyMZ_lLVmkAAIeAAMtmr1KtJUd5x3m1EI0AA",
    # Number cards – Blue
    "🔵_0": "CAACAgIAAxkBAAIBrGWx1zteAAFH9BAAAdSyMZ_lLVmkAAIfAAMtmr1KtJUd5x3m1EI0AA",
    "🔵_1": "CAACAgIAAxkBAAIBrmWx1ztfAAFH9RAAAdSyMZ_lLVmkAAIgAAMtmr1KtJUd5x3m1EI0AA",
    "🔵_2": "CAACAgIAAxkBAAIBsGWx1ztgAAFH9hAAAdSyMZ_lLVmkAAIhAAMtmr1KtJUd5x3m1EI0AA",
    "🔵_3": "CAACAgIAAxkBAAIBsmWx1zthAAFH9xAAAdSyMZ_lLVmkAAIiAAMtmr1KtJUd5x3m1EI0AA",
    "🔵_4": "CAACAgIAAxkBAAIBtGWx1ztiAAFH-BAAAdSyMZ_lLVmkAAIjAAMtmr1KtJUd5x3m1EI0AA",
    "🔵_5": "CAACAgIAAxkBAAIBtmWx1ztjAAFH-RAAAdSyMZ_lLVmkAAIkAAMtmr1KtJUd5x3m1EI0AA",
    "🔵_6": "CAACAgIAAxkBAAIBuGWx1ztkAAFH-hAAAdSyMZ_lLVmkAAIlAAMtmr1KtJUd5x3m1EI0AA",
    "🔵_7": "CAACAgIAAxkBAAIBumWx1ztlAAFH-xAAAdSyMZ_lLVmkAAImAAMtmr1KtJUd5x3m1EI0AA",
    "🔵_8": "CAACAgIAAxkBAAIBvGWx1ztmAAFH_BAAAdSyMZ_lLVmkAAInAAMtmr1KtJUd5x3m1EI0AA",
    "🔵_9": "CAACAgIAAxkBAAIBvmWx1ztnAAFH_RAAAdSyMZ_lLVmkAAIoAAMtmr1KtJUd5x3m1EI0AA",
    # Number cards – Green
    "🟢_0": "CAACAgIAAxkBAAIBwGWx1ztoAAFH_hAAAdSyMZ_lLVmkAAIpAAMtmr1KtJUd5x3m1EI0AA",
    "🟢_1": "CAACAgIAAxkBAAIBwmWx1ztpAAFH_xAAAdSyMZ_lLVmkAAIqAAMtmr1KtJUd5x3m1EI0AA",
    "🟢_2": "CAACAgIAAxkBAAIBxGWx1ztqAAFIABAAAdSyMZ_lLVmkAAIrAAMtmr1KtJUd5x3m1EI0AA",
    "🟢_3": "CAACAgIAAxkBAAIBxmWx1ztrAAFIARAAAdSyMZ_lLVmkAAIsAAMtmr1KtJUd5x3m1EI0AA",
    "🟢_4": "CAACAgIAAxkBAAIByGWx1ztsAAFIAhAAAdSyMZ_lLVmkAAItAAMtmr1KtJUd5x3m1EI0AA",
    "🟢_5": "CAACAgIAAxkBAAIBymWx1zttAAFIAxAAAdSyMZ_lLVmkAAIuAAMtmr1KtJUd5x3m1EI0AA",
    "🟢_6": "CAACAgIAAxkBAAIBzGWx1ztuAAFIBBAAAdSyMZ_lLVmkAAIvAAMtmr1KtJUd5x3m1EI0AA",
    "🟢_7": "CAACAgIAAxkBAAIBzmWx1ztvAAFIBRAAAdSyMZ_lLVmkAAIwAAMtmr1KtJUd5x3m1EI0AA",
    "🟢_8": "CAACAgIAAxkBAAIB0GWx1ztwAAFIBhAAAdSyMZ_lLVmkAAIxAAMtmr1KtJUd5x3m1EI0AA",
    "🟢_9": "CAACAgIAAxkBAAIB0mWx1ztxAAFIBxAAAdSyMZ_lLVmkAAIyAAMtmr1KtJUd5x3m1EI0AA",
    # Number cards – Yellow
    "🟡_0": "CAACAgIAAxkBAAIB1GWx1ztyAAFICBAAAdSyMZ_lLVmkAAIzAAMtmr1KtJUd5x3m1EI0AA",
    "🟡_1": "CAACAgIAAxkBAAIB1mWx1ztzAAFICRAAAdSyMZ_lLVmkAAI0AAMtmr1KtJUd5x3m1EI0AA",
    "🟡_2": "CAACAgIAAxkBAAIB2GWx1zt0AAFI ChAAAdSyMZ_lLVmkAAI1AAMtmr1KtJUd5x3m1EI0AA",
    "🟡_3": "CAACAgIAAxkBAAIB2mWx1zt1AAFIDRAAAdSyMZ_lLVmkAAI2AAMtmr1KtJUd5x3m1EI0AA",
    "🟡_4": "CAACAgIAAxkBAAIB3GWx1zt2AAFIERAAAdSyMZ_lLVmkAAI3AAMtmr1KtJUd5x3m1EI0AA",
    "🟡_5": "CAACAgIAAxkBAAIB3mWx1zt3AAFIFBAAAdSyMZ_lLVmkAAI4AAMtmr1KtJUd5x3m1EI0AA",
    "🟡_6": "CAACAgIAAxkBAAIB4GWx1zt4AAFIGBAAAdSyMZ_lLVmkAAI5AAMtmr1KtJUd5x3m1EI0AA",
    "🟡_7": "CAACAgIAAxkBAAIB4mWx1zt5AAFIHRAAAdSyMZ_lLVmkAAI6AAMtmr1KtJUd5x3m1EI0AA",
    "🟡_8": "CAACAgIAAxkBAAIB5GWx1zt6AAFIIhAAAdSyMZ_lLVmkAAI7AAMtmr1KtJUd5x3m1EI0AA",
    "🟡_9": "CAACAgIAAxkBAAIB5mWx1zt7AAFIJBAAAdSyMZ_lLVmkAAI8AAMtmr1KtJUd5x3m1EI0AA",
    # Action cards
    "🔴_Skip ⛔": "CAACAgIAAxkBAAIB6GWx1zt8AAFIKBAAAdSyMZ_lLVmkAAI9AAMtmr1KtJUd5x3m1EI0AA",
    "🔵_Skip ⛔": "CAACAgIAAxkBAAIB6mWx1zt9AAFILRAAAdSyMZ_lLVmkAAI-AAMtmr1KtJUd5x3m1EI0AA",
    "🟢_Skip ⛔": "CAACAgIAAxkBAAIB7GWx1zt-AAFIMhAAAdSyMZ_lLVmkAAI_AAMtmr1KtJUd5x3m1EI0AA",
    "🟡_Skip ⛔": "CAACAgIAAxkBAAIB7mWx1zt_AAFINRAAAdSyMZ_lLVmkAAJAAAMtmr1KtJUd5x3m1EI0AA",
    "🔴_Reverse 🔄": "CAACAgIAAxkBAAIB8GWx1zuAAAFIOBAAAdSyMZ_lLVmkAAJBAAMtmr1KtJUd5x3m1EI0AA",
    "🔵_Reverse 🔄": "CAACAgIAAxkBAAIB8mWx1zuBAAFIPRAAAdSyMZ_lLVmkAAJCAAMtmr1KtJUd5x3m1EI0AA",
    "🟢_Reverse 🔄": "CAACAgIAAxkBAAIB9GWx1zuCAAFIQhAAAdSyMZ_lLVmkAAJDAAMtmr1KtJUd5x3m1EI0AA",
    "🟡_Reverse 🔄": "CAACAgIAAxkBAAIB9mWx1zuDAAFIRRAAAdSyMZ_lLVmkAAJEAAMtmr1KtJUd5x3m1EI0AA",
    "🔴_Draw Two ✌️": "CAACAgIAAxkBAAIB-GWx1zuEAAFISBAAAdSyMZ_lLVmkAAJFAAMtmr1KtJUd5x3m1EI0AA",
    "🔵_Draw Two ✌️": "CAACAgIAAxkBAAIB-mWx1zuFAAFITRAAAdSyMZ_lLVmkAAJGAAMtmr1KtJUd5x3m1EI0AA",
    "🟢_Draw Two ✌️": "CAACAgIAAxkBAAIB_GWx1zuGAAFIUhAAAdSyMZ_lLVmkAAJHAAMtmr1KtJUd5x3m1EI0AA",
    "🟡_Draw Two ✌️": "CAACAgIAAxkBAAIB_mWx1zuHAAFIVRAAAdSyMZ_lLVmkAAJIAAMtmr1KtJUd5x3m1EI0AA",
    # Wild cards
    "Wild 🌈": "CAACAgIAAxkBAAICAmWx2AABUFIYBAAAdSyMZ_lLVmkAAJJAAMtmr1KtJUd5x3m1EI0AA",
    "Wild Draw Four 🌈✌️✌️": "CAACAgIAAxkBAAICBGWx2AABUS1JZBAAAdSyMZ_lLVmkAAJKAAMtmr1KtJUd5x3m1EI0AA",
}

# Fallback sticker if key not found (generic UNO card back)
FALLBACK_STICKER = "CAACAgIAAxkBAAICBmWx2AABUFIYBAAAdSyMZ_lLVmkAAJLAAMtmr1KtJUd5x3m1EI0AA"

# UNO card back sticker (shown for draw pile etc.)
UNO_BACK_STICKER = "CAACAgIAAxkBAAICCGWx2AABUU1JZBAAAdSyMZ_lLVmkAAJMAAMtmr1KtJUd5x3m1EI0AA"


# ──────────────────────────────────────────────
#  GAME STATE
# ──────────────────────────────────────────────

class UnoCard:
    def __init__(self, color: str, value: str):
        self.color = color   # emoji color or "" for wild
        self.value = value   # number or action string

    @property
    def key(self) -> str:
        if self.color:
            return f"{self.color}_{self.value}"
        return self.value

    @property
    def label(self) -> str:
        if self.color:
            return f"{self.color} {self.value}"
        return self.value

    def is_wild(self) -> bool:
        return self.value in WILD_CARDS

    def can_play_on(self, top: "UnoCard") -> bool:
        if self.is_wild():
            return True
        return self.color == top.color or self.value == top.value

    def __repr__(self):
        return self.label


class UnoGame:
    def __init__(self, chat_id: int, host_id: int, host_name: str):
        self.chat_id = chat_id
        self.host_id = host_id
        self.players: List[int] = []
        self.player_names: Dict[int, str] = {}
        self.hands: Dict[int, List[UnoCard]] = {}
        self.deck: List[UnoCard] = []
        self.discard: List[UnoCard] = []
        self.current_index: int = 0
        self.direction: int = 1   # 1 = clockwise, -1 = counter
        self.started: bool = False
        self.pending_draw: int = 0  # stacked +2/+4
        self.wild_pending: bool = False  # waiting for color choice
        self.join_message_id: Optional[int] = None

        self.add_player(host_id, host_name)

    def add_player(self, user_id: int, name: str):
        if user_id not in self.players:
            self.players.append(user_id)
            self.player_names[user_id] = name

    def build_deck(self) -> List[UnoCard]:
        deck = []
        for color in COLORS:
            deck.append(UnoCard(color, "0"))
            for val in NUMBER_CARDS[1:] + ACTION_CARDS:
                deck.append(UnoCard(color, val))
                deck.append(UnoCard(color, val))
        for _ in range(4):
            for wild in WILD_CARDS:
                deck.append(UnoCard("", wild))
        random.shuffle(deck)
        return deck

    def deal(self):
        self.deck = self.build_deck()
        for pid in self.players:
            self.hands[pid] = [self.deck.pop() for _ in range(7)]
        # Ensure first discard card is a number (not wild/action)
        while True:
            top = self.deck.pop()
            if not top.is_wild() and top.value in NUMBER_CARDS:
                self.discard = [top]
                break
            self.deck.insert(0, top)

    @property
    def top_card(self) -> UnoCard:
        return self.discard[-1]

    @property
    def current_player(self) -> int:
        return self.players[self.current_index]

    def next_turn(self, skip: bool = False):
        steps = 2 if skip else 1
        self.current_index = (self.current_index + self.direction * steps) % len(self.players)

    def draw_cards(self, player_id: int, count: int):
        for _ in range(count):
            if not self.deck:
                self.deck = self.discard[:-1]
                random.shuffle(self.deck)
                self.discard = [self.discard[-1]]
            if self.deck:
                self.hands[player_id].append(self.deck.pop())

    def play_card(self, player_id: int, card_index: int, chosen_color: str = "") -> dict:
        hand = self.hands[player_id]
        card = hand[card_index]
        result = {"ok": True, "msg": "", "winner": None, "skip": False}

        if card.is_wild() and chosen_color:
            card.color = chosen_color
        elif card.is_wild() and not chosen_color:
            result["ok"] = False
            result["msg"] = "Choose a color first!"
            return result

        hand.pop(card_index)
        self.discard.append(card)

        if not hand:
            result["winner"] = player_id
            return result

        # Handle effects
        if card.value == "Skip ⛔":
            result["skip"] = True
        elif card.value == "Reverse 🔄":
            self.direction *= -1
            if len(self.players) == 2:
                result["skip"] = True
        elif card.value == "Draw Two ✌️":
            self.pending_draw += 2
            result["skip"] = True
        elif card.value == "Wild Draw Four 🌈✌️✌️":
            self.pending_draw += 4
            result["skip"] = True

        return result


# ──────────────────────────────────────────────
#  ACTIVE GAMES  { chat_id: UnoGame }
# ──────────────────────────────────────────────
active_games: Dict[int, UnoGame] = {}

# ──────────────────────────────────────────────
#  HELPERS
# ──────────────────────────────────────────────

def get_sticker(card: UnoCard) -> str:
    return UNO_STICKERS.get(card.key, FALLBACK_STICKER)


def build_hand_keyboard(game: UnoGame, player_id: int) -> InlineKeyboardMarkup:
    hand = game.hands[player_id]
    top = game.top_card
    buttons = []
    row = []

    for i, card in enumerate(hand):
        playable = card.can_play_on(top)
        prefix = "✅" if playable else "❌"
        label = f"{prefix} {card.label}"
        cb = f"uno_play_{game.chat_id}_{player_id}_{i}"
        row.append(InlineKeyboardButton(label, callback_data=cb))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)

    buttons.append([
        InlineKeyboardButton("🎴 Draw Card", callback_data=f"uno_draw_{game.chat_id}_{player_id}"),
        InlineKeyboardButton("🔄 Refresh", callback_data=f"uno_refresh_{game.chat_id}_{player_id}"),
    ])
    return InlineKeyboardMarkup(buttons)


def build_color_keyboard(game: UnoGame, player_id: int, card_index: int) -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton("🔴 Red",    callback_data=f"uno_color_{game.chat_id}_{player_id}_{card_index}_🔴"),
        InlineKeyboardButton("🔵 Blue",   callback_data=f"uno_color_{game.chat_id}_{player_id}_{card_index}_🔵"),
    ],[
        InlineKeyboardButton("🟢 Green",  callback_data=f"uno_color_{game.chat_id}_{player_id}_{card_index}_🟢"),
        InlineKeyboardButton("🟡 Yellow", callback_data=f"uno_color_{game.chat_id}_{player_id}_{card_index}_🟡"),
    ]]
    return InlineKeyboardMarkup(buttons)


def build_join_keyboard(chat_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("✋ Join Game", callback_data=f"uno_join_{chat_id}"),
        InlineKeyboardButton("▶️ Start Now", callback_data=f"uno_forcestart_{chat_id}"),
    ]])


def player_list_text(game: UnoGame) -> str:
    lines = []
    for i, pid in enumerate(game.players):
        name = game.player_names[pid]
        cards = len(game.hands.get(pid, [])) if game.started else "—"
        crown = "👑 " if pid == game.host_id else ""
        lines.append(f"{crown}{i+1}. {name} — {cards} cards")
    return "\n".join(lines)


def game_status_text(game: UnoGame) -> str:
    cur = game.player_names[game.current_player]
    top = game.top_card
    direction = "➡️ Clockwise" if game.direction == 1 else "⬅️ Counter-clockwise"
    pending = f"\n⚠️ +{game.pending_draw} cards pending!" if game.pending_draw else ""
    return (
        f"🃏 **UNO Game**\n\n"
        f"🎴 Top card: **{top.label}**\n"
        f"🎯 Turn: **{cur}**\n"
        f"🔁 Direction: {direction}{pending}\n\n"
        f"**Players:**\n{player_list_text(game)}"
    )


# ──────────────────────────────────────────────
#  COMMANDS
# ──────────────────────────────────────────────

@app.on_message(filters.command("uno") & filters.group)
async def cmd_uno(client: Client, message: Message):
    chat_id = message.chat.id
    user = message.from_user
    if not user:
        return

    if chat_id in active_games:
        g = active_games[chat_id]
        if g.started:
            return await message.reply("⚠️ A game is already running! Use /unostop to end it.")
        if user.id in g.players:
            return await message.reply("⚠️ You've already joined. Wait for more players or tap ▶️ Start Now.")
        g.add_player(user.id, user.first_name)
        txt = (
            f"✋ **{user.first_name}** joined the game!\n\n"
            f"**Players ({len(g.players)}):**\n{player_list_text(g)}\n\n"
            "Tap **▶️ Start Now** when everyone is in!"
        )
        msg = await message.reply(txt, reply_markup=build_join_keyboard(chat_id))
        g.join_message_id = msg.id
        return

    game = UnoGame(chat_id, user.id, user.first_name)
    active_games[chat_id] = game

    txt = (
        f"🃏 **UNO Game Started!**\n\n"
        f"👑 Host: **{user.first_name}**\n\n"
        f"**Players (1):**\n{player_list_text(game)}\n\n"
        "Tap **✋ Join Game** to join!\n"
        "Tap **▶️ Start Now** to begin (min 2 players)."
    )
    msg = await message.reply(txt, reply_markup=build_join_keyboard(chat_id))
    game.join_message_id = msg.id


@app.on_message(filters.command("unojoin") & filters.group)
async def cmd_unojoin(client: Client, message: Message):
    chat_id = message.chat.id
    user = message.from_user
    if not user:
        return
    if chat_id not in active_games:
        return await message.reply("No active UNO lobby. Use /uno to start one!")
    g = active_games[chat_id]
    if g.started:
        return await message.reply("Game already started, you can join the next one!")
    if user.id in g.players:
        return await message.reply("You're already in the game!")
    g.add_player(user.id, user.first_name)
    await message.reply(
        f"✋ **{user.first_name}** joined!\n\n"
        f"**Players ({len(g.players)}):**\n{player_list_text(g)}\n\n"
        "Tap **▶️ Start Now** when ready!",
        reply_markup=build_join_keyboard(chat_id)
    )


@app.on_message(filters.command("unostart") & filters.group)
async def cmd_unostart(client: Client, message: Message):
    chat_id = message.chat.id
    user = message.from_user
    if chat_id not in active_games:
        return await message.reply("No UNO lobby! Use /uno to create one.")
    g = active_games[chat_id]
    if g.started:
        return await message.reply("Game is already in progress!")
    if user.id != g.host_id:
        return await message.reply("Only the host can start the game!")
    if len(g.players) < 2:
        return await message.reply("Need at least 2 players to start!")
    await _start_game(client, chat_id)


@app.on_message(filters.command("unostop") & filters.group)
async def cmd_unostop(client: Client, message: Message):
    chat_id = message.chat.id
    user = message.from_user
    if chat_id not in active_games:
        return await message.reply("No active UNO game here.")

    # Allow host or admins to stop
    g = active_games[chat_id]
    member = await client.get_chat_member(chat_id, user.id)
    is_admin = member.status.value in ("administrator", "creator")
    if user.id != g.host_id and not is_admin:
        return await message.reply("Only the host or admins can stop the game!")

    del active_games[chat_id]
    await message.reply("🛑 UNO game has been stopped.")


# ──────────────────────────────────────────────
#  GAME START
# ──────────────────────────────────────────────

async def _start_game(client: Client, chat_id: int):
    g = active_games[chat_id]
    g.deal()
    g.started = True

    top = g.top_card
    sticker = get_sticker(top)

    await client.send_sticker(chat_id, sticker)
    await client.send_message(
        chat_id,
        f"🃏 **UNO Begins!**\n\n"
        f"Cards dealt! 7 cards each.\n"
        f"🎴 First card: **{top.label}**\n\n"
        f"🎯 First turn: **{g.player_names[g.current_player]}**\n\n"
        f"**Players:**\n{player_list_text(g)}\n\n"
        f"Use the buttons below to view your cards!",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("🃏 My Cards", callback_data=f"uno_mycards_{chat_id}_{g.current_player}"),
        ]])
    )
    await _notify_turn(client, g)


async def _notify_turn(client: Client, g: UnoGame):
    pid = g.current_player
    name = g.player_names[pid]
    top = g.top_card

    pending_txt = f"\n⚠️ You must draw **+{g.pending_draw}** cards or stack!" if g.pending_draw else ""

    await client.send_message(
        g.chat_id,
        f"🎯 It's **{name}**'s turn!\n"
        f"🎴 Top card: **{top.label}**{pending_txt}\n\n"
        f"Tap below to play:",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("🃏 View My Cards", callback_data=f"uno_mycards_{g.chat_id}_{pid}"),
        ]])
    )


# ──────────────────────────────────────────────
#  CALLBACK HANDLERS
# ──────────────────────────────────────────────

@app.on_callback_query(filters.regex(r"^uno_join_"))
async def cb_join(client: Client, query: CallbackQuery):
    chat_id = int(query.data.split("_")[2])
    user = query.from_user
    if chat_id not in active_games:
        return await query.answer("No active lobby!", show_alert=True)
    g = active_games[chat_id]
    if g.started:
        return await query.answer("Game already started!", show_alert=True)
    if user.id in g.players:
        return await query.answer("You're already in!", show_alert=True)
    g.add_player(user.id, user.first_name)
    await query.answer(f"✅ You joined the UNO game!")
    await query.message.edit_text(
        f"🃏 **UNO Lobby**\n\n"
        f"**Players ({len(g.players)}):**\n{player_list_text(g)}\n\n"
        "Tap **✋ Join Game** to join or **▶️ Start Now** to begin!",
        reply_markup=build_join_keyboard(chat_id)
    )


@app.on_callback_query(filters.regex(r"^uno_forcestart_"))
async def cb_forcestart(client: Client, query: CallbackQuery):
    chat_id = int(query.data.split("_")[2])
    user = query.from_user
    if chat_id not in active_games:
        return await query.answer("No lobby!", show_alert=True)
    g = active_games[chat_id]
    if g.started:
        return await query.answer("Already started!", show_alert=True)
    if user.id != g.host_id:
        return await query.answer("Only the host can start!", show_alert=True)
    if len(g.players) < 2:
        return await query.answer("Need at least 2 players!", show_alert=True)
    await query.message.delete()
    await _start_game(client, chat_id)


@app.on_callback_query(filters.regex(r"^uno_mycards_"))
async def cb_mycards(client: Client, query: CallbackQuery):
    parts = query.data.split("_")
    chat_id = int(parts[2])
    turn_pid = int(parts[3])
    user = query.from_user

    if chat_id not in active_games:
        return await query.answer("No active game!", show_alert=True)
    g = active_games[chat_id]
    if not g.started:
        return await query.answer("Game hasn't started!", show_alert=True)
    if user.id not in g.players:
        return await query.answer("You're not in this game!", show_alert=True)
    if user.id != g.current_player:
        hand = g.hands[user.id]
        top = g.top_card
        hand_text = "\n".join(
            f"{'✅' if c.can_play_on(top) else '❌'} {c.label}"
            for c in hand
        )
        return await query.answer(
            f"Your {len(hand)} cards:\n{hand_text}\n\n(Wait for your turn!)",
            show_alert=True
        )

    await query.answer("Sending your cards privately...")
    try:
        await client.send_message(
            user.id,
            f"🃏 **Your Hand** ({len(g.hands[user.id])} cards)\n"
            f"🎴 Top card: **{g.top_card.label}**\n\n"
            "✅ = playable  ❌ = not playable\nTap a card to play it:",
            reply_markup=build_hand_keyboard(g, user.id)
        )
    except Exception:
        await query.message.reply(
            f"🃏 **{user.first_name}**'s turn!\n"
            f"🎴 Top card: **{g.top_card.label}**\n\nTap a card to play:",
            reply_markup=build_hand_keyboard(g, user.id)
        )


@app.on_callback_query(filters.regex(r"^uno_refresh_"))
async def cb_refresh(client: Client, query: CallbackQuery):
    parts = query.data.split("_")
    chat_id = int(parts[2])
    player_id = int(parts[3])
    user = query.from_user

    if user.id != player_id:
        return await query.answer("These aren't your cards!", show_alert=True)
    if chat_id not in active_games:
        return await query.answer("Game over!", show_alert=True)
    g = active_games[chat_id]
    if user.id != g.current_player:
        return await query.answer("It's not your turn!", show_alert=True)

    await query.message.edit_reply_markup(build_hand_keyboard(g, player_id))
    await query.answer("Refreshed ✅")


@app.on_callback_query(filters.regex(r"^uno_play_"))
async def cb_play(client: Client, query: CallbackQuery):
    parts = query.data.split("_")
    chat_id = int(parts[2])
    player_id = int(parts[3])
    card_index = int(parts[4])
    user = query.from_user

    if user.id != player_id:
        return await query.answer("Not your cards!", show_alert=True)
    if chat_id not in active_games:
        return await query.answer("Game ended!", show_alert=True)
    g = active_games[chat_id]
    if user.id != g.current_player:
        return await query.answer("It's not your turn!", show_alert=True)

    hand = g.hands[user.id]
    if card_index >= len(hand):
        return await query.answer("Invalid card index!", show_alert=True)

    card = hand[card_index]
    top = g.top_card

    # Pending draw — can only stack or accept
    if g.pending_draw:
        if card.value not in ("Draw Two ✌️", "Wild Draw Four 🌈✌️✌️"):
            return await query.answer(
                f"You must stack a +2/+4 or draw {g.pending_draw} cards!", show_alert=True
            )

    if not card.can_play_on(top):
        return await query.answer("❌ Can't play that card on the current top card!", show_alert=True)

    # Wild → ask for color
    if card.is_wild() and not card.color:
        await query.message.edit_text(
            f"🌈 **Choose a color for {card.value}:**",
            reply_markup=build_color_keyboard(g, user.id, card_index)
        )
        return await query.answer("Pick a color!")

    await _execute_play(client, query, g, user, card_index)


@app.on_callback_query(filters.regex(r"^uno_color_"))
async def cb_color(client: Client, query: CallbackQuery):
    parts = query.data.split("_")
    # uno_color_{chat_id}_{player_id}_{card_index}_{color}
    chat_id = int(parts[2])
    player_id = int(parts[3])
    card_index = int(parts[4])
    color = parts[5]
    user = query.from_user

    if user.id != player_id:
        return await query.answer("Not your turn!", show_alert=True)
    if chat_id not in active_games:
        return await query.answer("Game ended!", show_alert=True)
    g = active_games[chat_id]
    if user.id != g.current_player:
        return await query.answer("Not your turn!", show_alert=True)

    hand = g.hands[user.id]
    if card_index >= len(hand):
        return await query.answer("Invalid!", show_alert=True)

    # Assign chosen color to wild card before playing
    hand[card_index].color = color
    await _execute_play(client, query, g, user, card_index, chosen_color=color)


async def _execute_play(
    client: Client,
    query: CallbackQuery,
    g: UnoGame,
    user,
    card_index: int,
    chosen_color: str = ""
):
    hand = g.hands[user.id]
    card = hand[card_index]
    result = g.play_card(user.id, card_index, chosen_color)

    if not result["ok"]:
        return await query.answer(result["msg"], show_alert=True)

    sticker = get_sticker(card)
    try:
        await query.message.delete()
    except Exception:
        pass

    # Send played card as sticker to group
    await client.send_sticker(g.chat_id, sticker)

    cards_left = len(g.hands[user.id])
    uno_alert = " — **🔔 UNO!**" if cards_left == 1 else ""

    play_msg = (
        f"🎴 **{user.first_name}** played **{card.label}**{uno_alert}\n"
        f"Cards left: {cards_left}"
    )

    if result["winner"]:
        del active_games[g.chat_id]
        await client.send_message(
            g.chat_id,
            f"🏆 **{user.first_name} wins the UNO game!** 🎉\n\n"
            "Congratulations! Use /uno to start a new game."
        )
        return

    await query.answer(f"✅ Played {card.label}!")

    # Handle pending draw for next player
    if result["skip"]:
        g.next_turn(skip=False)
        if g.pending_draw:
            next_pid = g.current_player
            next_name = g.player_names[next_pid]
            g.draw_cards(next_pid, g.pending_draw)
            drew = g.pending_draw
            g.pending_draw = 0
            await client.send_message(
                g.chat_id,
                f"{play_msg}\n\n"
                f"😬 **{next_name}** draws **{drew}** cards and is skipped!"
            )
            g.next_turn()
        else:
            await client.send_message(g.chat_id, f"{play_msg}\n\n⛔ Next player skipped!")
    else:
        g.next_turn()
        await client.send_message(g.chat_id, play_msg)

    await _notify_turn(client, g)


@app.on_callback_query(filters.regex(r"^uno_draw_"))
async def cb_draw(client: Client, query: CallbackQuery):
    parts = query.data.split("_")
    chat_id = int(parts[2])
    player_id = int(parts[3])
    user = query.from_user

    if user.id != player_id:
        return await query.answer("Not your cards!", show_alert=True)
    if chat_id not in active_games:
        return await query.answer("Game ended!", show_alert=True)
    g = active_games[chat_id]
    if user.id != g.current_player:
        return await query.answer("It's not your turn!", show_alert=True)

    if g.pending_draw:
        count = g.pending_draw
        g.pending_draw = 0
        g.draw_cards(user.id, count)
        await query.answer(f"Drew {count} cards!")
        await client.send_message(
            g.chat_id,
            f"😬 **{user.first_name}** draws **{count}** cards!\n"
            f"Hand size: {len(g.hands[user.id])}"
        )
    else:
        g.draw_cards(user.id, 1)
        drawn = g.hands[user.id][-1]
        top = g.top_card
        can_play = drawn.can_play_on(top)
        await query.answer(f"Drew: {drawn.label}")
        await client.send_message(
            g.chat_id,
            f"🎴 **{user.first_name}** draws a card.\n"
            f"{'✅ Can play it!' if can_play else '❌ Cannot play it — turn passes.'}"
        )
        if not can_play:
            g.next_turn()
            await _notify_turn(client, g)
            return

    # Refresh hand view
    try:
        await query.message.edit_reply_markup(build_hand_keyboard(g, user.id))
    except Exception:
        pass

    await _notify_turn(client, g)
