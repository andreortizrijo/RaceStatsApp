def test(number):
    a = 0
    while a == 0:
        number += 1
        i = 2
        print(i)
        i += 1
        if i == 3:
            a = 1
    
    print(i)
    return 'Funca'

test(5)