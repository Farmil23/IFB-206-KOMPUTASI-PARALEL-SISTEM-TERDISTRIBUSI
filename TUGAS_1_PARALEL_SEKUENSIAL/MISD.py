import threading

data = 10

def add():
    global data
    result = data + 5
    print(f"Hasil pertambahan: {result}")

def multiply():
    global data
    result = data * 2
    print(f"Hasil perkalian: {result}")

def subtract():
    global data
    result = data - 3
    print(f"Hasil pengurangan: {result}")

thread1 = threading.Thread(target=add)
thread2 = threading.Thread(target=multiply)
thread3 = threading.Thread(target=subtract)

thread1.start()
thread2.start()
thread3.start()

thread1.join()
thread2.join()
thread3.join()