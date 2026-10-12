import time

Time = int(input("Enter Time: "))

for x in reversed(range(Time)):
    seconds = int(x) % 60
    minutes = int(x/60)%60
    hours = int(x/3600)%24
    print(f"{hours:02}:{minutes:02}:{seconds:02}")
    time.sleep(1)

print("Times Up!!!")