
import serial
vel = serial.Serial('/dev/ttyUSB0',9600,timeout=0.05)

def nummake(num):
    hnum=hex(num)
    shnum=str(hnum)
    a=shnum[2:]
    b=a.zfill(2)
    return b
    
    
def gofw(num):
    b=nummake(num)
    vel.write('55 55 05 06 01'+b+'00')
        
def goleft(num):
    b=nummake(num)
    vel.write('55 55 05 06 03'+b+'00')
    
def goright(num):
    b=nummake(num)
    vel.write('55 55 05 06 04'+b+'00')
        
def moveleft(num):
    b=nummake(num)
    vel.write('55 55 05 06 05'+b+'00')
        
def moveright(num):
    b=nummake(num)
    vel.write('55 55 05 06 06'+b+'00')
    
if __name__ == '__main__':
    while(1):
        com = input('请输入命令 前进/左转/右转/左移/右移')
        if com == 'go':
            num = input('plase enter the number')
            snum = int(num)
            gofw(snum)
        elif com == 'goleft':
            num = input('plase enter the number')
            snum = int(num)
            goleft(snum)
        elif com == 'goright':
            num = input('plase enter the number')
            snum = int(num)
            goright(snum)
        elif com == 'moveleft':
            num = input('plase enter the number')
            snum = int(num)
            moveleft(snum)
        elif com == 'moveright':
            num = input('plase enter the number')
            snum = int(num)
            gofw(snum)
        else: 
            print('无效命令，，，')
            
    