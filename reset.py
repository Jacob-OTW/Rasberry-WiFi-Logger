import csv


def reset(*files):
    for file in files:
        f = open(file, 'w', newline='')
        f.close()


if __name__ == '__main__':
    reset('all.csv', 'off-to-on.csv')
