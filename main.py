from multiprocessing import Process, Pipe
from os import getpid
from datetime import datetime
from time import sleep


def local_time(counter):
    return ' (LAMPORT_TIME={}, LOCAL_TIME={})'.format(counter,
                                                      datetime.now())


def calc_recv_timestamp(recv_time_stamp: list, counter: list) -> list:
    for i in range(len(counter)):
        counter[i] = max(recv_time_stamp[i], counter[i]) + 1
    return counter


def event(pid: int, counter: list) -> list:
    counter[pid] += 1
    return counter


def send_message(pipe, pid: int, counter: list) -> list:
    counter[pid] += 1
    pipe.send(('Empty shell', counter))
    return counter


def recv_message(pipe, pid: int, counter: list) -> list:
    counter[pid] += 1
    message, timestamp = pipe.recv()
    counter = calc_recv_timestamp(timestamp, counter)
    return counter


def process_one(pipe12):
    pid = 0
    counter = [0] * 3
    counter = event(pid, counter)
    counter = send_message(pipe12, pid, counter)
    counter = event(pid, counter)
    counter = recv_message(pipe12, pid, counter)
    counter = event(pid, counter)
    sleep(5)
    print('Process #1:', counter)


def process_two(pipe21, pipe23):
    pid = 1
    counter = [0] * 3
    counter = recv_message(pipe21, pid, counter)
    counter = send_message(pipe21, pid, counter)
    counter = send_message(pipe23, pid, counter)
    counter = recv_message(pipe23, pid, counter)
    sleep(10)
    print('Process #2:', counter)


def process_three(pipe32):
    pid = 1
    counter = [0] * 3
    counter = recv_message(pipe32, pid, counter)
    counter = send_message(pipe32, pid, counter)
    sleep(15)
    print('Process #3', counter)


if __name__ == '__main__':
    oneandtwo, twoandone = Pipe()
    twoandthree, threeandtwo = Pipe()

    process1 = Process(target=process_one,
                       args=(oneandtwo,))
    process2 = Process(target=process_two,
                       args=(twoandone, twoandthree))
    process3 = Process(target=process_three,
                       args=(threeandtwo,))

    process1.start()
    process2.start()
    process3.start()

    process1.join()
    process2.join()
    process3.join()
