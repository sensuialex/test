#coding:UTF-8
import play

game = play.game_setup(2,1)

player_winpts = [0 for i in range(game.number)]

for m in range(10): #対戦回数
    game = play.game_setup(2,1)
    game.begingame()

    nowmax = 0     #最高点
    playnum = [i for i in range(game.number)]
    scores = [game.player[i].victorycount() for i in range(game.number)]

    for (i,n) in zip(playnum,scores):
        if nowmax <= n:
            nowmax = n
            winnerIndex = i
    player_winpts[winnerIndex] += 1


print("トータル結果")
print(player_winpts)
 #aaaaa
