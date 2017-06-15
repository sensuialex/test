kindoftreasure = 3  #財宝カードの種類
kindofvictoryc = 3  #基本勝利点カードの種類
kindofaction = 10  #王国カードの種類

class Field():
    zeropile = 0  #0枚になったサプライの個数
    def __init__(self):
        self.trash = [] #廃棄置き場(単独)
        self.cursepile = Pile()  #呪い置き場(単独)
        self.treasurepile = [Pile() for i in range(kindoftreasure)]  #財宝置き場
        self.victorypile = [Pile() for i in range(kindofvictoryc)]  #勝利点カード置き場
        self.actionpile = [Pile() for i in range(kindofaction)]  #王国カード置き場

        self.supnumber = {1:self.cursepile}
        suptrenum = {(i+2):self.treasurepile[i] for i in range(3)}
        supvicnum = {(i+5):self.victorypile[i] for i in range(3)}
        supactnum = {(i+8):self.actionpile[i] for i in range(10)}
        self.supnumber.update(suptrenum)
        self.supnumber.update(supvicnum)
        self.supnumber.update(supactnum)  #サプライの場に番号を対応付けた

    def is_game_set(self):
        if Field.zeropile >= 3 or self.get_supply(7).zerocheck():
            return True
        return False

    def get_cardinfo(self, number):
        return self.supnumber.get(number).pile[0]

    def get_supply(self, number):
        return self.supnumber.get(number)

    def put_on_trash(self, cards):
        self.trash.append(cards)

    def add_zeropile(self):
        Field.zeropile += 1


class Pile():  #サプライのカードの山
    def __init__(self):
        self.pile = []  #カードの山 下から上へ
        self.name = ""  #山札に置かれているカードの名前
        self.cost = -1  #山札に置かれているカードのコスト

    def zerocheck(self): #山をチェックし、それが残り0枚ならzeropileをインクリメントする
        if len(self.pile) == 0:
            return 1
        return 0

    def is_left(self):
        length = len(self.pile)
        return length > 0
