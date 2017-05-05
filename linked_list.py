class Element:
    def __init__(self, data):
        self.data = data
        self.next_element = None

    def get_data(self):
        return self.data

    def get_next(self):
        return self.next_element

    def set_next(self, new_next):
        self.next_element = new_next


class LinkedList:   # but looks like a stack )))

    def __init__(self):
        self.head = None

    def insert(self, data):    # push to head
        new_element = Element(data)
        new_element.set_next(self.head)
        self.head = new_element

    def is_empty(self):
        return self.head is None

    def getout(self):   # get out the elelemnt from the list
        current = self.head
        if current:
            self.head = current.get_next()
        return current.get_data()

    def print_list(self):
        current = self.head
        while current:
            print(current.get_data(), end=' ')
            current = current.get_next()
        print('\n')


main_list = LinkedList()
reverse_list = LinkedList()

for i in range(10):
    main_list.insert(i)

main_list.print_list()

while not main_list.is_empty():
    reverse_list.insert(main_list.getout())

reverse_list.print_list()