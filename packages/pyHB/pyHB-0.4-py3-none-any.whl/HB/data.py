from pyrogram.types import InlineKeyboardButton as IKB, InlineKeyboardMarkup as IKM 

START_TEXT = """
HEY {},
__This is a Smoothest & Powerful HackBot Made By [Team Legend](https://t.me/TeamLegendXD)__
"""

START_BUTTON = IKM([
    [
        IKB(" Tg Hack ", callback_data="hack_btn"),
    ],
    [
        IKB("Updates", url="https://t.me/TeamLegendBots"),
        IKB("Support", url="https://t.me/LegendBot_OP"),
    ],
    [
        IKB("About Me", callback_data="about_me"),
        IKB("Owner", url="https://t.me/LegendBot_Owner"),
    ]])


ABOUT_TEXT = """
This is a Powerful & Advanced Telegram HackBot.
Which is used to Hack Telegram Account By Using his Pyrogram & Telethon session.

Pyrogram ~ [Documents](https://docs.org)
Telethon ~ [Documents](https://docs.org)

             Regarding @LegendBot_Owner
"""
HACK_TEXT = """

"A" :~ [Check user own groups and channels]

"B" :~ [Check user all information like phone number, usrname... etc]

"C" :~ [Ban a group {give me StringSession and channel/group username i will ban all members there}]

"D" :~ [Know user last otp {1st use option B take phone number and login there Account then use me i will give you otp}]

"E" :~ [Join A Group/Channel via StringSession]

"F" :~ [Leave A Group/Channel via StringSession]

"G" :~ [Delete A Group/Channel]

"H" :~ [Check user two step is eneable or disable]

"I" :~ [Terminate All current active sessions except Your StringSession]

"J" :~ [Delete Account]

"K" :~ [Promote a member in a group/channel]

"L" ~ [Demote all admins in a group/channel]

"M" ~ [Change Phone number using StringSession]

I will add more features Later 😅
"""


HACK_MODS = IKM([
    [
        IKB("A", callback_data="A"),
        IKB("B", callback_data ="B"),
        IKB("C", callback_data="C"),
        IKB("D", callback_data="D"),
        IKB("E", callback_data="E"),          
    ],
    [
        IKB("F", callback_data="F"),
        IKB("G", callback_data ="G"),
        IKB("H", callback_data="H"),
        IKB("I", callback_data="I"),
        IKB("J", callback_data="J"),
    ],
    [
        IKB("K", callback_data="K"),
        IKB("L", callback_data="L"),   
        IKB("M", callback_data="M"),
    ],
    ],    
    )
