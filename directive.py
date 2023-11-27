# creating a program that uses for and while loops to print in the terminal name fav food and fav movies

mystuff = ["stuff", "more stuff"]

# i is local variable that is an element in the list; runs as many times as there are the things in the list
for i in mystuff:
    print(i)

# a condition is true and while keeps going as long as it is true

x = 0
while True:
    if x > len(mystuff)-1:
        break
    print(mystuff[x])
    x += 1
    