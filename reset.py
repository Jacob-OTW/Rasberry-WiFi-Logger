def reset(file, content):
    with open(file, 'w', newline='') as file:
        file.write(content)
        file.close()


if __name__ == '__main__':
    reset('all.csv', "status,latency,date\n")
    reset('off-to-on.csv', "status,date\n")
