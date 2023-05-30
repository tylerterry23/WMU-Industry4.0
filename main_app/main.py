from GUI.mod_login import *
from GUI.mod_home import *


def main():
    temp = 1#LoginWindow().output

    if temp == 0:
        MainWindow()

    elif temp == 1:

        # Run Interface and Live Dashboard (Load Time 3-6 seconds)
        DjangoServer(), MainWindow()
        # MainWindow()
    else:
        pass


if __name__ == '__main__':
    main()
