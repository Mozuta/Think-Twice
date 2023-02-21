#基础分数 n为非闯关模式
s_score_n=1e4
#必要的前提变量

#std_step=n*n*5
#基础时间 n，a，b同上
#std_time=(n-2)*(n-2)*60

def honor_list():
    print()
def levelscore(level,step,time):
    if level == 1:
        return score_a(3,step,time,2,2)
    elif level == 2:
        return score_a(3, step, time, 0.8, 2)
    elif level == 3:
        return score_a(3, step, time, 0.8, 0.8)
    elif level == 4:
        return score_a(4, step, time, 2, 2)
    elif level == 5:
        return score_a(4, step, time, 0.8, 2)
    elif level == 6:
        return score_a(4, step, time, 0.8, 0.8)
    elif level == 7:
        return score_a(5, step, time, 2, 2)
    elif level == 8:
        return score_a(5, step, time, 0.8, 2)
    elif level == 9:
        return score_a(5, step, time, 0.8, 0.8)
    elif level == 10:
        return score_a(6, step, time, 0.8, 0.8)





#def adventure_mode():

#分数计算 标准分数，步数，时间
def score(gai,y_step,y_time):
    std_step=gai*gai*5
    std_time = (gai - 2) * (gai - 2) * 60
    fin_score=1e4+(std_step-y_step)*3+(std_time-y_time)*10
    return fin_score

def score_a(gai,y_step,y_time,w_s,w_t):
    std_step=gai*gai*5*w_s
    std_time = (gai - 2) * (gai - 2) * 60*w_t
    fin_score=1e4+(std_step-y_step)*3+(std_time-y_time)*10
    return fin_score

def judge(s,y):
    if y>=s:
        return 1
    else:
        return 0

while(True):
    n = int(input("输入关卡"))
    your_step = int(input("输入你的步数"))
    your_time = int(input("输入你的时间"))  # 秒
    print(levelscore(n, your_step, your_time))

