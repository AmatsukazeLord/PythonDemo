import numpy as np
import os

# 人机井字棋
# 程序以AI的角度编写  ‘自己’代表ai  敌方表示人类
# 极小极大搜索只为ai准备

# 初始化部分
COM = 1
MAN = -1
MAX_NUM = 999
man_first = True  # 人先手


# 不可以使用 x = y = num.zeros()
# 因为这样并不会生成 2个矩阵，而是会因为深拷贝只生成1个矩阵
board = np.zeros((3, 3), dtype=np.int_)
temp_board = np.zeros((3, 3), dtype=np.int_)


# 显示棋盘
def show_board():
    _ = os.system("cls")
    print('当前棋盘：')
    for i in board:
        print('|  ', end='')
        for j in i:
            if j == 1:
                print('*', end='  ')
            elif j == -1:
                print('X', end='  ')
            else:
                print(' ', end='  ')
        print('|')


# 判断输赢  1代表ai赢  -1表示人赢  0表示没分出胜负
def is_win():
    for i in range(3):
        if board[i, 0] + board[i, 1] + board[i, 2] == 3:
            return 1
        elif board[i, 0] + board[i, 1] + board[i, 2] == -3:
            return -1

    for i in range(3):
        if board[0, i] + board[1, i] + board[2, i] == 3:
            return 1
        elif board[0, i] + board[1, i] + board[2, i] == -3:
            return -1
    if board[0, 0] + board[1, 1] + board[2, 2] == 3 or board[0, 2] + board[1, 1] + board[2, 0] == 3:
        return 1
    elif board[0, 0] + board[1, 1] + board[2, 2] == -3 or board[0, 2] + board[1, 1] + board[2, 0] == -3:
        return -1
    return 0


# 评估函数
def evaluate_map():
    if is_win() == 1:
        return MAX_NUM
    elif is_win() == -1:
        return -MAX_NUM

    count = 0
    # 空位全填满自己的棋子
    for i in range(3):
        for j in range(3):
            temp_board[i, j] = 1 if board[i, j] == 0 else board[i, j]
    for i in temp_board:
        if sum(i) == 3:
            count += 1
    for i in range(3):
        if board[0, i] + board[1, i] + board[2, i] == 3:
            count += 1
    count += (board[0, 0] + board[1, 1] + board[2, 2]) // 3
    count += (board[0, 2] + board[1, 1] + board[2, 0]) // 3

    enemy = 0
    # 空位全填满敌方的棋子
    for i in range(3):
        for j in range(3):
            temp_board[i, j] = -1 if board[i, j] == 0 else board[i, j]
    for i in temp_board:
        if sum(i) == -3:
            enemy += 1
    for i in range(3):
        if board[0, i] + board[1, i] + board[2, i] == 3:
            enemy += 1
    enemy += (board[0, 0] + board[1, 1] + board[2, 2]) // 3
    enemy += (board[0, 2] + board[1, 1] + board[2, 0]) // 3

    return count - enemy


# 放置棋子
def set_piece(position, player):
    if position and board[position[0], position[1]] == 0:
        board[position[0], position[1]] = player
    else:
        print('下的位置有棋子了')
        return False
    return True


# 拿起棋子
def unset_piece(position):
    if position:
        board[position[0], position[1]] = 0


# 返回棋盘剩余空位
def vacancy():
    c = 0
    for i in range(3):
        for j in range(3):
            if board[i, j] == 0:
                c += 1
    return c


# 极大极小值搜索
def minmax_search(player, depth=2):
    if depth == 0:
        return None
    if vacancy() == 0:
        return False
    best_position = None
    best_value = 0

    if player == COM:
        for i in range(3):
            for j in range(3):
                if board[i, j] == 0:
                    set_piece((i, j), COM)
                    value = evaluate_map()
                    if value >= best_value:
                        best_value = value
                        best_position = (i, j)
                    unset_piece((i, j))
        set_piece(best_position, COM)
        player = MAN if player == COM else COM
        result = minmax_search(player, depth - 1)
        unset_piece(best_position)
        if result and abs(result[0]) > best_value:
            return result[1]
        return best_position

    elif player == MAN:
        for i in range(3):
            for j in range(3):
                if board[i, j] == 0:
                    set_piece((i, j), MAN)
                    value = evaluate_map()
                    if value <= best_value:
                        best_value = value
                        best_position = (i, j)
                    unset_piece((i, j))
        set_piece(best_position, MAN)
        player = MAN if player == COM else COM
        minmax_search(player, depth - 1)
        unset_piece(best_position)

        return best_value, best_position


# ai下棋
def com_play():
    if vacancy() > 0:
        set_piece(minmax_search(COM, 5), COM)
        print('AI的回合')
        show_board()
        return is_win()
    else:
        print('没空位了')
        return -1


# 人操作
def man_play():
    if vacancy() > 0:
        row = int(input('请输入要下棋的位置（0~2行）:'))
        col = int(input('请输入要下棋的位置（0~2列）:'))
        while not set_piece((row, col), MAN):
            row = int(input('请输入要下棋的位置（0~2行）:'))
            col = int(input('请输入要下棋的位置（0~2列）:'))
        show_board()
        return is_win()
    else:
        print('没空位了')
        return -1


if __name__ == '__main__':
    first = input('人是否先手(y/n)：')
    if first == 'y' or first == 'Y':
        show_board()
        while True:
            man = man_play()
            if man == 1:
                print('你赢了')
                break
            elif man == -1:
                print('平局')
                break

            ai = com_play()
            if ai == 1:
                print('ai赢了')
                break
            elif ai == -1:
                print('平局')
                break
    else:
        show_board()
        while True:
            ai = com_play()
            if ai == 1:
                print('ai赢了')
                break
            elif ai == -1:
                print('平局')
                break

            man = man_play()
            if man == 1:
                print('你赢了')
                break
            elif man == -1:
                print('平局')
                break
