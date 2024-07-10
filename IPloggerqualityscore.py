from IpFunc import ConfigN,main,qu
from threading import Thread
def start():
    #while True:
        ConfigN()
        Thread(target=main,daemon=True).start()
        qu()

if __name__ == "__main__":
    start()
    # ConfigN()
    # main(Notify)