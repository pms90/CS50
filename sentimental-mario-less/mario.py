
def mario(height):
    for i in range(height+1)[1:]:
        print(" "*(height-i) + "#"*(i))

aux = False
while aux == False:
    try:
        height = int(input("Height: "))
        if (height <= 8) and (height >= 1):
            aux = True
    except:
        pass



mario(height)

