import random
import card
import commonuse
import general

class Player():
    def __init__(self, game):
        self.cards = PlayerCards() #手札、デッキ、巣手札、プレイエリア
        self.available = AvailablePerTurn() #残り金数、残りアクション権、残り購入権
        self.isAI = 0
        self.isHuman = 0
        self.other_players = []
        self.gameinfo = PlayerGameInfo(game)
    

    def print_hand(self):
        self.cards.print_hand()

    def draw(self, number):
        self.cards.draw(number)

    def playcard(self, number, when = None):#カードは手札からプレイされる。手札の何枚目かをnumberとして与える。正規のタイミング(財宝フェイズに出す財宝、アクションフェイズにアクション権を消費して出すアクションカード)でカードをプレイするとき、whenに'right'を与えることにする
        the_card = self.cards.pickup_from_hand(number)
        if (when is None) or (self.gameinfo.playable(the_card)):
            playedcard = self.cards.play_from_hands(number)
            self.gameinfo.rightplayed(when)
            playedcard.played(self)
            self.is_actionphase_end(when)#処理終了後、アクションフェイズで残りアクション権が0ならばフェイズを自動的に終了する
            return True
        return False

    def is_actionphase_end(self, when):
        if self.gameinfo.phase_judged(general.ActionPhase) \
            and (when is 'right') and (not self.is_action_left()):
            self.phaseend()

    def shuffle(self):
        self.cards.shuffle()

    def gaincard(self, number):
        place = self.gameinfo.get_supply(number)
        if place.is_left(): #山札が切れていない場合のみ獲得できる
            gainedcard = place.pile.pop()
            self.add_dispile(gainedcard)
            gainedcard.gained(self)
            self.zerocheck_pile(place)

    def buycard(self, number):#カードは原則サプライから購入される　山札の番号をnumberとして与える。
        place = self.gameinfo.get_supply(number)
        if not place.is_left():
            return
        if self.available.coins >= place.cost and self.available.is_buys_left():
            self.available.coins -= place.cost #そのカードのコストを購入者の残り金から減算
            self.available.rest_buys -= 1 #購入権を1減らす
            print(self.available.rest_buys)
            self.gaincard(number)
            print(place.name)

    def trashcard(self, target): #廃棄時効果の発動のタイミングは？
        if isinstance(target, card.Card):
            self.put_on_trash(target)
            target.trashed(self)
            return
        if isinstance(target, list):
            [self.trashcard(i) for i in target]

        if isinstance(target, CardsHolder):
            [self.trashcard(i) for i in target.list]


    def put_on_trash(self, cards):
        self.gameinfo.put_on_trash(cards)

    def phaseend(self): #現在のフェーズを終了し、次のフェーズへ移行する
        self.gameinfo.phaseend()

    def nextphase(self):
        self.gameinfo.phaseend()

    def victorycount(self):
        return self.cards.victorycount()

    def handcheck(self, ctype):
        return self.cards.hand_typecheck(ctype)

    def plusactions(self, number):
        self.available.plusactions(number)

    def plusbuys(self, number):
        self.available.plusbuys(number)

    def pluscoins(self, number):
        self.available.pluscoins(number)

    def what_action(self):
        self.phaseend()

    def what_buy(self):
        pass

    def what_gain(self, number):
        pass

    def beginturn(self, turn):
        self.gameinfo.beginturn(turn)

    def is_action_left(self):
        return self.available.is_action_left()

    def put_on_dispile(self, cards):
        self.cards.put_on_dispile(cards)

    def zerocheck_pile(self, place):
        if place.zerocheck():
            self.gameinfo.add_zeropile()

    def phase_judged(self, phase):
        return self.gameinfo.phase_judged(phase)

    def turnstart(self):
        self.available.turnstart()

    def is_buys_left(self):
        return self.available.is_buys_left()

    def cleanup(self):
        self.cards.cleanup_cards()
        self.draw(5)

    def is_deck_empty(self):
        return self.cards.is_deck_empty()

    def is_dispile_empty(self):
        return self.cards.is_dispile_empty()

    def is_hand_empty(self):
        return self.cards.is_hand_empty()

    def reveal_from_deck(self, number):
        return self.cards.reveal_from_deck(number)

    def add_hand(self, cards):
        self.cards.add_hand(cards)

    def add_dispile(self, cards):
        self.cards.add_dispile(cards)

    def add_deck(self, cards):
        self.cards.add_deck(cards)

    def hand_pop(self, number):
        return self.cards.hand_pop(number)

    def playarea_pop(self, cards):
        self.cards.playarea_pop(cards)

    def pickup_from_hand(self, number):
        return self.cards.pickup_from_hand(number)

    def is_card_in_hand(self, ename):
        return self.cards.is_card_in_hand(ename)

    def index_card_in_hand(self, ename):
        return self.cards.index_card_in_hand(ename)

    def use_attack(self):
        pass

    def deck_count(self):
        return self.cards.deck_count()

    def hand_count(self):
        return self.cards.hand_count()


class PlayerCards():
    def __init__(self):
        self.deck = commonuse.CardsHolder() #デッキ 下から上へ
        self.hand = commonuse.CardsHolder() #手札 左から右へ
        self.dispile = commonuse.CardsHolder() #捨て札の山 下から上へ
        self.playarea = commonuse.CardsHolder() #各プレイヤーの場 左から右へ

    def print_hand(self):
        self.hand.print_cardlist()

    def is_deck_empty(self):
        return self.deck.is_empty()

    def is_dispile_empty(self):
        return self.dispile.is_empty()

    def is_hand_empty(self):
        return self.hand.is_empty()

    def shuffle(self):
        self.deck.shuffle()

    def deck_count(self):
        return self.deck.counting()

    def hand_count(self):
        return self.hand.counting()

    def dispile_count(self):
        return self.dispile.counting()

    def is_card_in_hand(self, ename):
        return self.hand.is_card_in(ename)

    def index_card_in_hand(self, ename):
        return self.hand.index(ename)

    def draw(self, number):
        if number == 0:
            return
        if number > self.deck_count() and not self.is_dispile_empty():
        #デッキの枚数が足りず、かつ捨て札があるとき(デッキ足りなくて捨て札もないときに詰みそう)
            number -= self.deck_count()
            self.deck.all_move_to(self.hand, 'r')
            self.dispile_to_deck()
        drawcard = self.pop_from_decktop(number)
        self.add_hand(drawcard[::-1])

    def pop_from_decktop(self, number):
        return self.deck.pop_from_top(number)

    def dispile_to_deck(self):
        self.dispile.all_move_to(self.deck)
        self.shuffle()

    def victorycount(self):
        vp = 0
        self.gather_all_to_deck()
        print(self.deck_count())
        vp = self.deck.victorycount()
        return vp

    def gather_all_to_deck(self):
        self.dispile.all_move_to(self.deck)
        self.hand.all_move_to(self.deck)
        self.playarea.all_move_to(self.deck)

    def hand_typecheck(self, ctype):
        return self.hand.is_type_exist(ctype)

    def play_from_hands(self, number):
        playedcard = self.hand_pop(number)
        self.add_playarea(playedcard)
        return playedcard

    def pickup_from_hand(self, number):
        return self.hand.pickup(number)

    def hand_pop(self, number):
        return self.hand.pop(number)

    def put_on_dispile(self, cards):
        self.dispile.add_cards(cards)

    def add_dispile(self, cards):
        self.dispile.add_cards(cards)

    def add_hand(self, cards):
        self.hand.add_cards(cards)

    def add_deck(self, cards):
        self.deck.add_cards(cards)

    def add_playarea(self, cards):
        self.playarea.add_cards(cards)

    def cleanup_cards(self):
        self.playarea.all_move_to(self.dispile)
        self.hand.all_move_to(self.dispile)

    def reveal_from_deck(self, number):
        revealed_card = commonuse.CardsHolder()
        if number > self.deck_count() and not self.is_dispile_empty(): #デッキの枚数が足りず、かつ捨て札があるとき
            number -= self.deck_count()
            revealed_card.add_cards(self.reveal_from_deck(self.deck_count()))
            self.dispile_to_deck()
        revealed_card.add_cards(self.pop_from_decktop(number))
        return revealed_card.list

    def playarea_pop(self, cards):
        number = self.playarea.index(cards)
        popcard = self.playarea.pop(number)
        return popcard


class AvailablePerTurn():
    def __init__(self):
        self.rest_actions = 1
        self.rest_buys = 1
        self.coins = 0

    def turnstart(self):
        self.__init__()

    def plusactions(self, number):
        self.rest_actions += number

    def plusbuys(self, number):
        self.rest_buys += number

    def pluscoins(self, number):
        self.coins += number

    def is_action_left(self):
        return self.rest_actions > 0

    def is_buys_left(self):
        return self.rest_buys > 0

class PlayerGameInfo():
    def __init__(self, game):
        self.turn = 0
        self.phase = 0
        self.game = game

    def get_cardinfo(self, number):
        return self.game.get_cardinfo(number)

    def phaseend(self):
        self.phase = next(self.turn)

    def beginturn(self, turn):
        self.turn = turn

    def phase_judged(self, phase):
        return isinstance(self.phase, phase)

    def get_supply(self, number):
        return self.game.get_supply(number)

    def rightplayed(self, when):
        self.phase.rightplayed(when)

    def playable(self, cards):
        return self.phase.playable(cards)

    def put_on_trash(self, cards):
        self.game.put_on_trash(cards)

    def get_cardtype(self, ctype):
        return commonuse.CardType.get_cardtype(ctype)

    def add_zeropile(self):
        self.game.add_zeropile()

#任意のプレイヤーは捨て札の一番上のカードをいつでも見ることができる
#プレイヤーはデッキの残り枚数を数えることができる
#廃棄置き場のカードを確認することができる
#サプライに残っているカードの枚数を確認できる
