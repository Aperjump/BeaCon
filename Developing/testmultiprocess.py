
import multiprocessing as mul
class P(mul.Process):
    def __init__(self):
        super(P, self).__init__()
    def run(self):
        print('hello')


if __name__ == "__main__":
    p = P()
    p.start()
    for D in mul.active_children():
        print("child   p.name:" + D.name + "\tp.id" + str(D.pid))
    p.join()