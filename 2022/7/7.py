from time import perf_counter


class File:
    def __init__(self, name, size) -> None:
        self.name = name
        self.size = size


class Directory:
    def __init__(self, name, Parent = None) -> None:
        self.name = name
        self.parent = Parent
        self.files = []


    def size(self):
        self.s = 0
        for f in self.files:
            if isinstance(f, File):
                self.s += f.size
            else:
                f.size()
                self.s += f.s


def sumDirectories(filesystem):
    if filesystem.s <= 100000:
        count = filesystem.s
    else:
        count = 0

    for f in filesystem.files:
        if isinstance(f, Directory):
            count += sumDirectories(f)

    return count


def smallestDelete(fileSystem, needToDelete):
    if fileSystem.s < needToDelete:
        return None

    smallest = fileSystem.s
    for f in fileSystem.files:
        if isinstance(f, Directory):
            result = smallestDelete(f, needToDelete)
            if result:
                smallest = min(smallest, result)

    return smallest


def main(filename):
    with open(filename, encoding="UTF-8") as f:
        lines = [line.strip('\n') for line in f.readlines()]


    fileSystem = Directory("/")

    listing = False
    for line in lines[1:]:
        if line[0] == "$":
            listing = False

        if "$ ls" in line:
            listing = True
        elif "$ cd .." in line:
            fileSystem = fileSystem.parent
        elif "$ cd" in line:
            for subDir in fileSystem.files:
                if isinstance(subDir, Directory) and subDir.name == line.split(" ")[2]:
                    fileSystem = subDir
                    break
        elif "dir" in line:
            fileSystem.files.append(Directory(line.split(" ")[1], fileSystem))
        else:
            fileSystem.files.append(File(line.split(" ")[1], int(line.split(" ")[0])))

    while fileSystem.parent:
        fileSystem = fileSystem.parent

    fileSystem.size()

    print(f"\nPart 1:\n{sumDirectories(fileSystem)}")

    freeSpace = 70000000 - fileSystem.s
    needToDelete = 30000000 - freeSpace

    print(f"\nPart 2:\n{smallestDelete(fileSystem, needToDelete)}")


if __name__ == "__main__":
    init_time = perf_counter()
    main("input.txt")
    print(f"\nRan in {perf_counter() - init_time} seconds.")