
from math import inf as infinity    #Imprort inf(giá trị vô cùng) từ thư viện math, đặt tên mới cho inf là infinity
from random import choice           #thêm hàm choice từ thư viện random
import platform                     #thêm thư viện platform, sử dụng để xác định hệ điều hành
import time                         #thêm thư viện thời gian
from os import system               #thêm hàm system từ thư viện os, sử dụng để làm sạch console

HUMAN = -1
COMP = +1
#Hàm đánh giá trạng thái hiện tại của trò chơi, truyền vào đối số state
def evaluate(state):           #state là trạng thái hiện tại của trò chơi, thể hiện cách các ô trên bảng được điền(vd giá trị có thể là 0,-1,1) 
    if wins(state, COMP):      #kiểm tra xem máy tính thắng hay chưa, nếu máy thắng trả về 1    
        score = +1                  
    elif wins(state, HUMAN):    #kiểm tra xem người thắng hay chưa, nếu máy thắng trả về -1  
        score = -1
    else:
        score = 0               #nếu không ai thắng sẽ trả về hòa
    return score                #trả về giá trị hiện tại của trò chơi, score này được sử dụng trong minmax  

def wins(state, player):        #Hàm kiểm tra xem ai đã thắng
    win_state = [
        [state[0][0], state[0][1], state[0][2]],        #chứa tất cả các trường hợp chiến thắng của game
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],    
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False

def game_over(state):       #hàm kiểm tra xem game kết thúc hay chưa
    return wins(state, HUMAN) or wins(state, COMP)

def empty_cells(state):     #Hàm trả về danh sách ô trống trên bảng trò chơi
    cells = []              #khởi tạo danh sách trống mới cells
    for x, row in enumerate(state):         #sử dụng enumerate lặp qua giá trị và chỉ số hàng
        for y, cell in enumerate(row):      #sử dụng enumerate lặp qua giá trị và chỉ số cột
            if cell == 0:                   #nếu chỉ số cell = 0 thì thêm vào tọa độ x,y vào cells
                cells.append([x, y])
    return cells

def valid_move(x, y):       #Hàm kiểm tra xem nước đi có hợp lệ hay không
    if [x, y] in empty_cells(board):
        return True
    else:
        return False

def set_move(x, y, player):     #Hàm được sử dụng để đặt nước đi cho người chơi
    if valid_move(x, y):        #gọi hàm valid_move để kiểm tra nước đi tại tọa độ x, y có hợp lệ hay không
        board[x][y] = player    #gán giá trị người chơi và ô có tọa độ x, y trên bảng board
        return True
    else:
        return False

def minimax(state, depth, player):      #depth là độ sâu tìm kiếm trong thuật toán minmax   
    if player == COMP:
        best = [-1, -1, -infinity]      #best lưu trữ tọa độ x, y và điểm tốt nhất tìm thấy cho nước đi
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or game_over(state):      #kiểm tra xem trò chơi đã kết thúc hay chưa
        score = evaluate(state)
        return [-1, -1, score]              #score sẽ được gán = +1 nếu máy thắng, -1 nếu người chơi thắng, 0 nếu trò chơi chưa kết thúc

    for cell in empty_cells(state):     #trò chơi chưa kết thúc hàm sẽ tìm nước đi tối ưu thông qua vòng lặp
        x, y = cell[0], cell[1]            #lấy giá trị tọa độ từ hàng x và cột y của ô trống đang xem xét
        state[x][y] = player              #gán nước đi đó vào người chơi
        #gọi hàm minmax đệ quy để tối ưu nước đi cho đối thủ(đổi dấu của player thành ngược lại)
        score = minimax(state, depth - 1, -player)   
        #depth - 1 là độ sâu tiếp theo để tìm kiếm, giảm đi 1 để tìm kiếm các nước đi tiếp theo trong trò chơi
        #kết quả tìm kiếm được lưu vào biến score chứa nước đi tốt nhất tìm được
        state[x][y] = 0           #đặt lại giá trị của ô có tọa độ x, y trong bảng state về 0                     
        score[0], score[1] = x, y   #được sử dụng để cập nhật tọa độ (x, y) của nước đi tốt nhất dựa trên tọa độ của nó trong trò chơi. 
                                    #tại mỗi cấp độ của đệ quy, chúng ta lưu trữ tọa độ của nước đi tốt nhất cho trạng thái hiện tại.
        if player == COMP:
            if score[2] > best[2]:      #trong lần lặp đầu tiên score sẽ được khởi tạo với giá trị [score[0], score[1], score[2]], 
            #sau khi thuật toán minmax chạy score[2] sẽ được gán bằng giá trị dựa trên kết quả của hàm evaluate(state)
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value

    return best

def clean():
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')

def render(state, c_choice, h_choice):
    chars = {
        -1: h_choice,
        +1: c_choice,
        0: ' '
    }
    str_line = '---------------'
    print('\n' + str_line)
    for row in state:
        for cell in row:
            symbol = chars[cell]
            print(f'| {symbol} |', end='')
        print('\n' + str_line)
        
def ai_turn(c_choice, h_choice):
    # Tính độ sâu của trò chơi bằng cách đếm số ô trống còn lại trên bảng trò chơi
    depth = len(empty_cells(board))
    
    # Kiểm tra xem trò chơi đã kết thúc chưa
    if depth == 0 or game_over(board):
        return  # Trả về ngay nếu trò chơi đã kết thúc

    clean()  # Xóa màn hình console để hiển thị bước đi tiếp theo
    print(f'Computer turn [{c_choice}]')
    
    # Hiển thị bảng trò chơi trước khi máy tính thực hiện bước đi
    render(board, c_choice, h_choice)

    if depth == 9:
        # Nếu bảng trống, máy tính chọn một ô ngẫu nhiên để đánh
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        # Nếu bảng không trống, máy tính sử dụng thuật toán minimax để tìm nước đi tốt nhất
        move = minimax(board, depth, COMP)
        x, y = move[0], move[1]

    # Thực hiện nước đi tại ô có tọa độ x, y cho máy tính
    set_move(x, y, COMP)
    
    time.sleep(1)


def human_turn(c_choice, h_choice):
    # Tính độ sâu của trò chơi bằng cách đếm số ô trống còn lại trên bảng trò chơi
    depth = len(empty_cells(board))
    
    # Kiểm tra xem trò chơi đã kết thúc chưa
    if depth == 0 or game_over(board):
        return  # Trả về ngay nếu trò chơi đã kết thúc

    move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    clean()  # Xóa màn hình console để hiển thị bước đi tiếp theo
    print(f'Human turn [{h_choice}]')
    
    # Hiển thị bảng trò chơi trước khi người chơi thực hiện nước đi
    render(board, c_choice, h_choice)

    while move < 1 or move > 9:
        try:
            move = int(input('Use numpad (1..9): '))  # Yêu cầu người chơi nhập nước đi từ bàn phím
            coord = moves[move]  # Lấy tọa độ tương ứng với nước đi từ bảng tọa độ moves
            can_move = set_move(coord[0], coord[1], HUMAN)  # Thực hiện nước đi cho người chơi

            if not can_move:
                print('Bad move')  # Nếu nước đi không hợp lệ, thông báo lỗi
                move = -1
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')  # Nếu người chơi nhập không hợp lệ, thông báo lỗi

def main():
    while True:
        global board
        board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        h_choice = ''  # X hoặc O - Lựa chọn của người chơi
        c_choice = ''  # X hoặc O - Lựa chọn của máy
        first = ''  # Nếu người chơi là người đi trước

        # Người chơi chọn X hoặc O để chơi
        while h_choice != 'O' and h_choice != 'X':
            try:
                print('')
                h_choice = input('Choose X or O\nChosen: ').upper()
            except (EOFError, KeyboardInterrupt):
                print('Bye')
                exit()
            except (KeyError, ValueError):
                print('Bad choice')

        # Thiết lập lựa chọn của máy
        if h_choice == 'X':
            c_choice = 'O'
        else:
            c_choice = 'X'

        # Người chơi có thể đi trước
        clean()
        while first != 'Y' and first != 'N':
            try:
                first = input('First to start?[y/n]: ').upper()
            except (EOFError, KeyboardInterrupt):
                print('Bye')
                exit()
            except (KeyError, ValueError):
                print('Bad choice')

        # Vòng lặp chính của trò chơi
        while len(empty_cells(board)) > 0 and not game_over(board):
            if first == 'N':
                ai_turn(c_choice, h_choice)
                first = ''

            human_turn(c_choice, h_choice)
            ai_turn(c_choice, h_choice)

        # Thông báo kết thúc trò chơi
        clean()
        if wins(board, HUMAN):
            print(f'Human turn [{h_choice}]')
            render(board, c_choice, h_choice)
            print('YOU WIN!')
        elif wins(board, COMP):
            print(f'Computer turn [{c_choice}]')
            render(board, c_choice, h_choice)
            print('YOU LOSE!')
        else:
            render(board, c_choice, h_choice)
            print('DRAW!')

        # Hỏi người chơi có muốn chơi lại không
        play_again = input("Do you want to play again? (y/n): ").strip().lower()
        if play_again != 'y':
            break

if __name__ == '__main__':
    main()

