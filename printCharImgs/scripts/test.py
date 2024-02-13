import subprocess
# subprocess.run("ffpython ff_test.py")
# subprocess.run("python ff_test.py")
# subprocess.Popen(["./ff_test.py", "arg1"])
#subprocess.run("python ff_test.py arg")

from multiprocessing import Process
from ff_test import run1
class qwer:
    def run2(self):
        # print(2)
        # if __name__ == "__main__":
        #     print(1)
        #     p = Process(target=run1, args=("bob",))
        #     p.start()
        #     p.join()
        print(1)
        p = Process(target=run1, args=("bob",))
        p.start()
        p.join()
