def manyyield(n, m):
    yield from range(n)

    yield from range(m)

if __name__ == '__main__':
    for j in manyyield(5,10):
        print(j)