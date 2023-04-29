import time


def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args)
        end_time = time.time()
        print(f'Time: {end_time - start_time:.10f}')
        return result

    return wrapper


@timer
def search(lst_, low_, high_, x_):
    count = 0
    for i in range(low_, high_):
        count += 1
        if lst_[i] == x_:
            return i, count
        else:
            return -1

@timer
def binary_search(lst_, low_, high_, x_):
    count = 0
    while low_ <= high_:
        count += 1
        mid = (low_ + high_) // 2
        if lst_[mid] == x_:
            return mid, count
        elif lst_[mid] > x_:
            high_ = mid - 1
        else:
            low_ = mid + 1
    else:
        return -1


lst = [i for i in range(1, 10000000)]
x = 34
result = binary_search(lst, 0, len(lst) - 1, x)
if result != -1:
    print(f' Число {x} найдено в списке по индексу {result[0]}. Кол-во попыток: {result[1]}')
else:
    print('Число не найдено')
