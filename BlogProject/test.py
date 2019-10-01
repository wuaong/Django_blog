def max2min(array):
    tmp = []
    for num in array:
        tmp.insert(0,num)

    return tmp
if __name__ == '__main__':
    array =[6,5,4,3,2,1]
    a=max2min(array)
    print(a)