import player

class AIPlayer1(player.Player):#お金プレイ
    def __init__(self, game):
        super().__init__(game)
        self.isAI = 1

    def play_coins(self):
        i = 0
        while i < self.hand_count():
            i = self.when_playable_coin(i)
            i += 1

    def when_playable_coin(self, number):
        if self.playcard(number, 'right'):
            return number - 1
        return number

    def what_buy(self):
        if self.available.coins < 3:
            self.phaseend()
            return
        if self.available.coins < 6:
            self.buycard(3)
            return
        if self.available.coins < 8:
            self.buycard(4)
            return
        self.buycard(7)


class AIPlayer2(player.Player):#鍛冶屋ステロ
    def __init__(self, game):
        super().__init__(game)
        self.isAI = 1
        self.smithycount = 0
        self.smithyindex = -1

    def play_coins(self):
        i = 0
        while i < self.hand_count():
            i = self.when_playable_coin(i)
            i += 1

    def when_playable_coin(self, number):
        if self.playcard(number, 'right'):
            return number - 1
        return number

    def what_action(self):
        i = 0
        flag = 1
        while i < self.hand_count() and flag:
            flag = self.is_action_played(i)
            i += 1

    def is_action_played(self, number):
        if self.playcard(number, 'right'):
            return 0
        return 1

    def what_buy(self):
        if self.smithyindex == -1 and "Smithy" in [x.name for x in self.gameinfo.game.field.actionpile]:
            self.smithyindex = [x.name for x in self.gameinfo.game.field.actionpile].index("Smithy") + 8

        if self.available.coins < 3:
            self.phaseend()
            return
        if self.available.coins == 3:
            self.buycard(3)
            return
        if self.available.coins < 6 and self.smithycount == 0 and self.smithyindex != -1:
            self.smithycount += 1
            self.buycard(self.smithyindex)
            return
        if self.available.coins < 6:
            self.buycard(3)
            return
        if self.available.coins < 8:
            self.buycard(4)
            return
        self.buycard(7)
