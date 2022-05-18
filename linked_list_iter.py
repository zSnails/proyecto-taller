class User:
    def __init__(self, name):
        self.name = name
        self.next = None

    def append(self, user):
        curr = self
        while curr.next:
            curr = curr.next

        curr.next = user

    def __iter__(self):
        curr = self
        while curr:
            yield curr
            curr = curr.next
        # return ListIterator(self)


def ListIterator(head):
    while head:
        yield head
        head = head.next


users = User("Aaron")
users.append(User("Samuel"))
users.append(User("Niggers"))

for user in users:
    print(user)
