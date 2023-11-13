class GAME_RES:
    BLACK_VICTORY = "black_victory"
    WHITE_VICTORY = "white_victory"
    ACTIVE = "active"
    ABORTED = "aborted"
    GAME_RESULT_CHOISES = (
        (BLACK_VICTORY, "BlackVictory"),
        (WHITE_VICTORY, "WhiteVictory"),
        (ACTIVE, "Active"),
        (ABORTED, "Aborted"),
    )


class USER_ROLES:
    BOT = "bot"
    USER = "user"
    ADMIN = "admin"
    BANNED = "banned"
    USER_ROLE_CHOISES = (
        (BOT, "Bot"),
        (USER, "User"),
        (ADMIN, "Admin"),
        (BANNED, "Banned"),
    )
