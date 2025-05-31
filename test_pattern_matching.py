a = 2
d = True
match a:
    case 1:
        pass
    case other if d:
        print('case 1')
        d = True
    case _:
        print('case 2')
        d = False
