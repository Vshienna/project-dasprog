def sequSearch(listarray, n):
    is_found = False
    for i in  listarray:
        if(i == n ):
            is_found = True
            return is_found
    return is_found
testlist = [1, 2, 32, 8, 17, 19, 42, 13, 0]
print(sequSearch(testlist, 13))