import commonuse
import card
import gamefield


numofcopper = 60
numofsilver = 40
numofgold = 30
numofvict2 = 8
numofvict34 = 12
numofact = 10
numofcurse = 10  #参加者一人当たりの呪いの枚数



class Game():
    def __init__(self, number):
        self.number = number  #参加人数
        self.player = []  #参加プレイヤーはplay.pyで設定する
        self.field = gamefield.Field()  #場を生成
        self.turnplayer = 0
        self.turncount = 1

    def starter(self, supply):
        for i in range(self.number):#各プレイヤーのデッキに銅貨を7枚、屋敷を3枚ずつ配る
        #その後、各々のデッキをシャッフルし、デッキから5枚引いて手札にする
            copper = [card.Copper() for j in range(7)]
            estate = [card.Estate() for j in range(3)]
            self.player[i].add_deck(copper)
            self.player[i].add_deck(estate)
            self.player[i].shuffle()
            self.player[i].draw(5)

        copperrest = numofcopper - self.number * 7
        self.makesupply(copperrest, 2, card.Copper())  #銅貨の山を作る
        self.makesupply(numofsilver, 3, card.Silver())  #銀貨の山を作る
        self.makesupply(numofgold, 4, card.Gold())  #金貨の山を作る

        numofvict = self.howmany_victorycards(self.number)#人数によって勝利点カードの枚数を制御

        self.makesupply(numofvict, 5, card.Estate())  #屋敷の山を作る
        self.makesupply(numofvict, 6, card.Duchy())  #公領の山を作る
        self.makesupply(numofvict, 7, card.Province())  #属州の山を作る

        self.makesupply((self.number-1)*numofcurse, 1, card.Curse())   #呪いの山を作る

        [self.makesupply(numofact, i, j()) for i, j in zip(range(8, 18), supply)]

        print([self.field.supnumber.get(i).name for i in range(1, 18)])

    def howmany_victorycards(self, number):
        if number == 2:
            return numofvict2
        if number == 3 or number == 4:
            return numofvict34

    def makesupply(self, number, placenum, cardclass):  #山札を作る(引数は、枚数、場所、カードを生成するコマンド)
        cards = [cardclass for i in range(number)]
        self.get_supply(placenum).pile.extend(cards)
        self.get_supply(placenum).name = self.get_cardinfo(placenum).ename
        self.get_supply(placenum).cost = self.get_cardinfo(placenum).cost
        typelist = commonuse.CardType.get_typelist()
        for istype in typelist:
            if hasattr(self.get_cardinfo(placenum), istype):
                setattr(self.get_supply(placenum), istype, 1)


    def beginturn(self, playernum):  #numに対応するプレイヤーのターンを開始する
        print("")
        print(self.turncount)
        print("ターン開始")
        turn = iter(Turn(self.player[playernum], self.field))
        self.player[playernum].beginturn(turn)
        self.player[playernum].nextphase() #Start
        self.player[playernum].nextphase() #Action
        self.player[playernum].gameinfo.phase.start()  #Action
        self.player[playernum].gameinfo.phase.start()  #Treasure
        self.player[playernum].gameinfo.phase.start()  #Buy

    def changeturn(self):
        self.turnplayer = (self.turnplayer + 1) % self.number

    def begingame(self):
        gameflag = 1
        while gameflag:
            self.beginturn(self.turnplayer)
            gameflag = self.is_game_set_or_continue()
        self.endgame()

    def is_game_set_or_continue(self):
        if self.field.is_game_set():
            return 0
        self.changeturn()
        self.turncount += 1
        return 1

    def endgame(self):
    #勝利点が同じであるときは、よりターン数が少なかったプレイヤーの勝ち。
        print("ゲーム終了です")
        VP = [self.player[i].victorycount() for i in range(self.number)]
        print(VP)

    def get_cardinfo(self, number):
        return self.field.get_cardinfo(number)

    def get_supply(self, number):
        return self.field.get_supply(number)

    def put_on_trash(self, cards):
        self.field.put_on_trash(cards)

    def add_zeropile(self):
        self.field.add_zeropile()


class Turn():
    def __init__(self, player, field):
        self.player = player
        self.field = field

    def __iter__(self):
        yield StartPhase(self.player)
        yield ActionPhase(self.player)
        yield TreasurePhase(self.player)
        yield BuyPhase(self.player, self.field)
        yield CleanUpPhase(self.player, self.field)


class Phase():
    def __init__(self, player):
        self.player = player

    def playable(self, cards):
        return False

    def start(self):
        pass

    def rightplayed(self, when):
        pass


class StartPhase(Phase):
    def __init__(self, player):
        super().__init__(player)
        self.player.turnstart()


class ActionPhase(Phase):
    def __init__(self, player):
        super().__init__(player)
        print("アクションフェイズです")
        print(len(self.player.cards.deck.list) + len(self.player.cards.hand.list)\
            + len(self.player.cards.dispile.list))

    def start(self):
        while self.player.phase_judged(ActionPhase):
            self.what_do()

    def what_do(self):
        if not self.player.handcheck('action'):
            self.player.phaseend()
            return

        if self.player.isAI == 1 or self.player.isHuman == 1:  #AIまたは人間用
            print([i.jname for i in self.player.cards.hand.list])
            print("どのアクションカードを使用しますか")
            self.player.what_action()#分けられそう

    def playable(self, cards):
        return cards.is_action()

    def rightplayed(self, when):
        if when == 'right':
            self.player.plusactions(-1)  #カードがプレイされたらアクション権を1減らす

class TreasurePhase(Phase):
    def __init__(self, player):
        super().__init__(player)
        print("財宝フェイズです")
        print([i.jname for i in self.player.cards.hand.list])

    def start(self):
        if self.player.isAI == 1:  #AI用
            self.player.play_coins()
            print(self.player.available.coins)
            self.player.phaseend()
            return

        if self.player.isHuman == 1:
            isbreak = 0
            self.treasure_playable_time(isbreak)
            print(self.player.available.coins)
            self.player.phaseend()
            return

        if self.player.isAI == 0:  #プレイヤ用
            pass

    def treasure_playable_time(self, flag):
        while flag != -1:
            print([i.jname for i in self.player.cards.hand.list])
            print("使用する財宝カードの番号を入力してください")
            flag = self.player.what_coin_play()

    def playable(self, cards):
        return cards.is_treasure()


class BuyPhase(Phase):
    def __init__(self, player, field):
        super().__init__(player)
        print("購入フェイズです")
        self.field = field

    def start(self):
        while self.player.phase_judged(BuyPhase):
            self.is_ai_or_human()

    def is_ai_or_human(self):
        if self.player.isAI == 1:  #AI用
            self.is_continue_ai()
            return

        if self.player.isHuman == 1:
            self.is_continue_human()
            return

    def is_continue_ai(self):
        if self.player.is_buys_left():
            self.player.what_buy()
            return
        self.player.phaseend()

    def is_continue_human(self):
        if self.player.is_buys_left():
            print("購入するカードの番号を入力してください")
            self.player.what_buy()
            return
        self.player.phaseend()


class CleanUpPhase(Phase):
    def __init__(self, player, field):
        super().__init__(player)
        print("クリーンアップフェイズです")
        self.cleanup()

    def cleanup(self):
        self.player.cleanup()



