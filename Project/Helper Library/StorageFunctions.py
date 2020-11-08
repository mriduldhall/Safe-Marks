class StorageFunctions:
    def __init__(self, storagename, data):
        self.storagename = storagename
        self.data = data

    def append(self):
        file = open(self.storagename, "a+")
        file.write(self.data)
        file.close()

    def retrieve(self, position):
        try:
            file = open(self.storagename, "r")
            line_counter = 1
            for line in file:
                data = line.split('§')
                string_check = data[position-1]
                if string_check == self.data:
                    return str(line), int(line_counter)
                line_counter += 1
            return None, None
        except EOFError:
            return None

    def update(self, location):
        file = open(self.storagename, "r+")
        file_content = (file.readlines())
        file_content[location-1] = self.data
        file.truncate(0)
        file.close()
        file = open(self.storagename, "a")
        file.writelines(file_content)
        file.close()

    def list(self, position):
        data_list = []
        file = open(self.storagename, "r")
        for line in file:
            data = line.split('§')
            data_to_add = data[position-1]
            data_list.append(data_to_add)
        return data_list


if __name__ == "__main__":
    # obj = StorageFunctions("test.txt", "a\nb\nc\nd\ne\nf\ng\nh\ni\nj\nk")
    # obj.append()
    # obj2 = StorageFunctions("test.txt", "test\n")
    # line_content, line_number = obj2.retrieve()
    # print(line_content, "is located on line number", line_number)

    obj3 = StorageFunctions("test.txt", "")
    obj3.update(5)
