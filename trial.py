# opening and creating new .txt file
with open('logs/test.txt', 'r') as r, open(f'new.txt', 'w') as o:
    for line in r:
        print(line)
        #strip() function
        if line.strip():
            o.write(line)
f = open("new.txt", "r")
print("New text file:\n",f.read())