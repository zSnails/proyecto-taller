class LinkedList:
    def __init__(self):
        self.head = None
        self.length = 0

    def __len__(self):
        return self.length

    def append(self, data) -> None:
        if not self.head:
            self.head = data
            self.length += 1
            return

        current = self.head
        while current.next:
            current = current.next
        current.next = data
        self.length += 1

    def __getitem__(self, index):
        if not index:
            return self.head

        curr = self.head
        while index:
            curr = curr.next
            index -= 1
        return curr

    def __iter__(self) -> "Node":
        curr = self.head
        while curr:
            yield curr
            curr = curr.next

    def __str__(self):
        str = "["

        curr = self.head
        while curr.next:
            str += f"{curr}, "
            curr = curr.next
        str += f"{curr}]"

        return str


class Data:
    def __init__(self, num):
        self.value = num
        self.next = None

    def __str__(self):
        return f"Data({self.value})"


lista = LinkedList()
lista.append(Data(1))
lista.append(Data(23))
lista.append(Data(28))
lista.append(Data(27))

print(lista[2].value)


for elemento in lista:
    print(elemento.value)

print(lista)
print(len(lista))
