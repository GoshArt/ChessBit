from django.db import models
import datetime


# Create your models here.
class Test(models.Model):
    name = models.CharField(max_length=255)
    succ = models.CharField(max_length=255)


class Gosha(models.Model):
    name = models.TextField(max_length=255)
    iq = models.CharField(max_length=2)

    def __str__(self):
        return self.name + " " + self.iq


class User(models.Model):
    UserNickname = models.CharField(max_length=20)
    UserEmail = models.EmailField(max_length=100)
    UserPassword = models.CharField(max_length=20)
    UserRating = models.IntegerField(default=800)

    USER = "US"
    BAN = "BN"
    ADMIN = "AD"
    OWNER = "OW"

    USER_STATUSES = [
        (USER, "USER"),
        (BAN, "BAN"),
        (ADMIN, "ADMIN"),
        (OWNER, "OWNER"),
    ]

    UserStatus = models.CharField(max_length=2, choices=USER_STATUSES, default=USER)
    UserAvatar = models.CharField(max_length=100, default="TEST")
    UserRegistrationDate = models.DateTimeField(auto_now_add=True)


class Lobbies(models.Model):
    LobbyIsRated = models.BooleanField(default=False)
    LobbyTimeLimit = models.IntegerField(default=600)
    LobbyCreatorID = models.ForeignKey(User, on_delete=models.CASCADE)


class Matches(models.Model):
    MatchIsRated = models.BooleanField(default=False)
    # WhitePlayerUserID = models.ForeignKey(User, on_delete=models.CASCADE)
    # BlackPlayerUserID = models.ForeignKey(User, on_delete=models.CASCADE)
    PlayersUserID = models.ManyToManyField(User)
    RESULTS = [
        ("B", "BLACK WON"),
        ("W", "WHITE WON"),
        ("D", "DRAW"),
        ("A", "ABORTED")
    ]
    MatchResult = models.CharField(choices=RESULTS, default="A")


class MatchHistory(models.Model):
    WhitePlayerHistoryRating = models.IntegerField()
    BlackPlayerHistoryRating = models.IntegerField()
    MatchCompletionTime = models.DateTimeField(auto_now_add=True)
    # WhitePlayerUserID = models.ForeignKey(User, on_delete=models.CASCADE)
    # BlackPlayerUserID = models.ForeignKey(User, on_delete=models.CASCADE)
    # PlayersUserID = models.ManyToManyField(User)


class MatchHistory_PlayersUserID(models.Model):
    MatchHistoryId = models.ForeignKey(MatchHistory, on_delete=models.CASCADE)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    UserColor = models.CharField(choices=[("B", "BLACK"), ("W", "WHITE")])
