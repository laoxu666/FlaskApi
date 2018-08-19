import random
import time


def time_count(fun):

    def f(*args, **kwargs):
        before = time.time()
        fun(*args, **kwargs)
        after = time.time()
        print(after - before)
    return f


def game_control_wrapper(control):
    def game_control(fun):
        def f(*args, **kwargs):

            if random.randrange(100) > control:
                fun(*args, **kwargs)
            else:
                print("撸代码")

        return f
    return game_control


# @time_count
@game_control_wrapper(10)
def play(name, type=0):

    time.sleep(2)
    print("今天玩了几把%s" % name)


if __name__ == '__main__':
    # before = time.time()
    # play()
    # after = time.time()
    #
    # print(after-before)

    play("LOL", type=1)

