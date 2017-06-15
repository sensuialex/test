import card
import random
class CardType():
    cardtype = {'action':'isaction', 'treasure':'istreasure', 'victory':'isvictory', 'curse':'iscurse', 'reaction':'isreaction', 'attack':'isattack'}

    @classmethod
    def get_cardtype(cls, ctype):
        return cls.cardtype.get(ctype)

    @classmethod
    def get_typelist(cls):
        return cls.cardtype.values()


class CardsHolder():
    def __init__(self, cards=None):
        if cards is None:
            self.list = []
        else:
            self.list = cards

    def print_cardlist(self):
        print([card.jname for card in self.list])

    def counting(self):
        return len(self.list)

    def shuffle(self):
        random.shuffle(self.list)

    def clear(self):
        self.list.clear()

    def reverse(self):
        self.list.reverse()

    def reversed(self):
        return self.list[::-1]

    def remove(self, element):
        self.list.remove(element)

    def index(self, name):
        cardname_list = [card.ename for card in self.list]
        return cardname_list.index(name)

    def is_empty(self):
        return self.list == []

    def add_cards(self, cards):
        if isinstance(cards, card.Card):
            self.list.append(cards)
            return
        if isinstance(cards, list):
            self.list.extend(cards)
            return
        if isinstance(cards, CardsHolder):
            self.list.extend(cards.list)

    def is_card_in(self, ename):
        return ename in [card.ename for card in self.list]

    def victorycount(self):
        vp = sum([card.vicpts(self.list) for card in self.list if card.is_victory_or_curse()])
        return vp

    def pop_from_top(self, number):
        cards = CardsHolder(self.list[-number:])
        self.list = self.list[:-number]
        return cards.list

    def pop_from_bottom(self, number):
        cards = CardsHolder(self.list[:number])
        self.list = self.list[number:]
        return cards.list

    def pickup(self, number):
        return self.list[number]

    def pop(self, number):
        return self.list.pop(number)

    def is_type_exist(self, ctype):
        typecards = [card for card in self.list if card.is_type(ctype)]
        return typecards != []

    def all_move_to(self, place, reverse=None):
        if reverse == 'r':
            self.reverse()
        place.add_cards(self.list)
        self.clear()
