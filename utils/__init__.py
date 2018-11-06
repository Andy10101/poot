def printMainTitle(text,leftSize):
    for i in range(int(leftSize)):
        print('-',end='')
    print(text,end='')
    for i in range(int(leftSize)):
        print('-',end='')
    print('')
def printBody(text,leftSize):
    print('|',end='')
    for i in range(leftSize):
        print(' ',end='')
    print(text)
def printEnd(titleText,size):
    realSize=size*2+len(titleText)*2
    for i in range(realSize):
        print('-',end='')
    print('')