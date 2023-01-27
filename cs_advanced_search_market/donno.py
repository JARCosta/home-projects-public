from termcolor import colored


def parser():
    input = []
    with open("input.txt", "r") as f:
        file = f.read()
        lines = file.split("\n")
        for link in lines:
            url = link.split("?")

            print("aaaaa", url)
            arguments = url[1]
            input.append(arguments.split("&"))
    return input


input = parser()

for line in input:
    print(colored(line[0], "blue"))
    for item in line[1:]:
        print(colored(item, "black"))

with open("output.txt", "w") as f:
    # Convert the list to a string and write it to the file
    f.write(str(input))