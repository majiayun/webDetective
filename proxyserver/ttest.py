
screen_w = 80
screen_h = 80
every_w = screen_w / 8
every_h = screen_h / 8
every_area = every_w * every_h

x = 14
y = 13
w = 32
h = 29
left = x
right = x+w
up = y
down = y+h

# left_up = []
left_up_row = up // every_h + 1
left_up_col = left // every_w + 1

# left_up.append(left_up_row)
# left_up.append(left_up_col)

# left_down = []
if down % every_h == 0:
    left_down_row = down // every_h
else:
    left_down_row = down // every_h + 1
left_down_col = left // every_w + 1
# left_down.append(left_down_row)
# left_down.append(left_down_col)

# right_up = []
right_up_row = up // every_h + 1
if right % every_w == 0:
    right_up_col = right // every_h
else:
    right_up_col = right // every_h + 1

# right_up.append(right_up_row)
# right_up.append(right_up_col)

# right_down = []
if down % every_h == 0:
    right_down_row = down // every_h
else:
    right_down_row = down // every_h + 1
if right % every_w == 0:
    right_down_col = right // every_h
else:
    right_down_col = right // every_h + 1


# right_down.append(right_down_row)
# right_down.append(right_down_col)

center_divs = []
for i in range(int(left_up_row + 1), int(left_down_row)):
    for j in range(int(left_up_col + 1), int(right_up_col)):
        cur_div = []
        cur_div.append(i)
        cur_div.append(j)
        cur_div.append(every_h*every_w)
        center_divs.append(cur_div)

edge_divs = []
for i in range(int(left_up_row), int(left_down_row + 1)):
    for j in range(int(left_up_col), int(right_up_col + 1)):
        cur_div = []
        cur_div.append(i)
        cur_div.append(j)
        #左上角
        if i == left_up_row and j == left_up_col:
            cur_x = left_up_col * every_w - left
            cur_y = left_up_row * every_h - up
        #左上角与右上角之间
        elif i == left_up_row and j < right_up_col:
            cur_x = every_w
            cur_y = left_up_row * every_h - up
        #右上角
        elif i == left_up_row and j == right_up_col:
            cur_x = right - (right_up_col-1) * every_w
            cur_y = right_up_row * every_h - up
        # 左上角与左下角之间
        elif i > left_up_row and i != left_down_row and j == left_up_col:
            cur_x = left_up_col * every_w - left
            cur_y = every_h
        # 右上角与右下角之间
        elif i > left_up_row and i != left_down_row and j == right_up_col:
            cur_x = right - (right_up_col-1) * every_w
            cur_y = every_h
        # 左下角
        elif i == left_down_row and j == left_down_col:
            cur_x = left_down_col * every_w - left
            cur_y = down - (left_down_row-1) * every_h
        # 左下角与右下角之间
        elif i == left_down_row and j < right_down_col:
            cur_x = every_w
            cur_y = down - (left_down_row-1) * every_h
        # 右下角
        elif i == left_down_row and j == right_down_col:
            cur_x = right - (right_down_col-1) * every_w
            cur_y = down - (left_down_row-1) * every_h

        cur_div.append(cur_x * cur_y)

        if [cur_div[0], cur_div[1]] not in ([i[0], i[1]] for i in center_divs):
            edge_divs.append(cur_div)

print(center_divs)
print(edge_divs)

every_area_value = [[1,1,0.1/28],[1,2,0.1/28],[1,3,0.1/28],[1,4,0.1/28],[1,5,0.1/28],[1,6,0.1/28],[1,7,0.1/28],[1,8,0.1/28],
              [2,1,0.1/28],[2,2,0.2/20],[2,3,0.2/20],[2,4,0.2/20],[2,5,0.2/20],[2,6,0.2/20],[2,7,0.2/20],[2,8,0.1/28],
              [3,1,0.1/28],[3,2,0.2/20],[3,3,0.3/12],[3,4,0.3/12],[3,5,0.3/12],[3,6,0.3/12],[3,7,0.2/20],[3,8,0.1/28],
              [4,1,0.1/28],[4,2,0.2/20],[4,3,0.3/12],[4,4,0.4/4],[4,5,0.4/4],[4,6,0.3/12],[4,7,0.2/20],[4,8,0.1/28],
              [5,1,0.1/28],[5,2,0.2/20],[5,3,0.3/12],[5,4,0.4/4],[5,5,0.4/4],[5,6,0.3/12],[5,7,0.2/20],[5 ,8,0.1/28],
              [6,1,0.1/28],[6,2,0.2/20],[6,3,0.3/12],[6,4,0.3/12],[6,5,0.3/12],[6,6,0.3/12],[6,7,0.2/20],[6,8,0.1/28],
              [7,1,0.1/28],[7,2,0.2/20],[7,3,0.2/20],[7,4,0.2/20],[7,5,0.2/20],[7,6,0.2/20],[7,7,0.2/20],[7,8,0.1/28],
              [8,1,0.1/28],[8,2,0.1/28],[8,3,0.1/28],[8,4,0.1/28],[8,5,0.1/28],[8,6,0.1/28],[8,7,0.1/28],[8,8,0.1/28],
              ]
center_value=0
for center_div in center_divs:
    for item in every_area_value:
        if [center_div[0],center_div[1]] == [item[0],item[1]]:
            center_value+=center_div[2]/every_area*item[2]

edge_value=0
for edge_div in edge_divs:
    for item in every_area_value:
        if [edge_div[0],edge_div[1]] == [item[0],item[1]]:
            edge_value+=edge_div[2]/every_area*item[2]

area_value=center_value+edge_value
print(area_value)
