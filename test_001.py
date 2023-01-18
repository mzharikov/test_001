"""As the task have not specified language, I've tried to use as less language-specific features as possible,
which of course made the code less pretty. Such approach should not be used in production environment for sure"""


# Public Next, Prev and Rand is terrible idea. Those fields should be Private as modification outside of
# specific class methods will almost certainly break the data structure. At least I won't allow to set them at init
class ListNode:
    def __init__(self, data=None):
        self.next: (ListNode | None) = None
        self.prev: (ListNode | None) = None
        self.rand: (ListNode | None) = None
        self.data: str = data


# Public Head, Tail and Count is terrible idea too
class ListRand:
    def __init__(self):
        self.head: (ListNode | None) = None
        self.tail: (ListNode | None) = None
        self.count: int = 0

    def append(self, new_data: str):
        self.count += 1
        new_node = ListNode(data=new_data)
        if self.head is None and self.tail is None:
            self.head = new_node
            self.tail = new_node
            return

        self.tail.next = new_node
        new_node.prev = self.tail
        self.tail = new_node

    def add_random_link_by_index(self, index_from: int, index_to: int):
        # In some cases it will be faster to start from tail, e.g. both indexes are greater than self.count / 2
        current_node = self.head
        node_from: (ListNode | None) = None
        node_to: (ListNode | None) = None

        current_node_index = 0
        while True:
            if current_node_index == index_from:
                node_from = current_node
            if current_node_index == index_to:
                node_to = current_node
            if current_node.next is None:
                break
            current_node = current_node.next
            current_node_index += 1

        if node_from is None or node_to is None:
            raise IndexError("List index out of range")

        node_from.rand = node_to

    def print_list_with_ids(self):
        current_node = self.head
        while True:
            random_link = ''
            if current_node.rand is not None:
                random_link = '-> ' + current_node.rand.data + ' (' + str(id(current_node.rand)) + ')'
            print(current_node.data + ' (' + str(id(current_node)) + ') ' + random_link)
            if current_node.next is None:
                break
            current_node = current_node.next

    def serialize(self, file: str):
        current_node = self.head
        write_buffer = ''
        serialized_nodes_list = []
        nodes_to_indexes = {}

        node_index = 0
        while True:
            nodes_to_indexes[current_node] = node_index
            serialized_nodes_list.append(current_node.data.replace(';', '\;').replace(':', '\:') + ';')
            if current_node.next is None:
                break
            node_index += 1
            current_node = current_node.next

        for node, index in nodes_to_indexes.items():
            if node.rand is not None:
                linked_node_index = nodes_to_indexes.get(node.rand)
                serialized_nodes_list[index] = serialized_nodes_list[index][:-1] + ':' + str(linked_node_index) + ';'

        for element in serialized_nodes_list:
            write_buffer += element

        file = open(file, 'w')
        file.write(write_buffer)
        file.close()

    def deserialize(self, file: str):
        with open(file) as f:
            text = f.read()

        data_buffer = ''
        index_buffer = ''
        node_index = 0
        is_escape = False
        is_parsing_index = False
        link_pair_indexes = {}
        indexes_to_nodes = {}

        for char in text:
            if char == '\\':
                is_escape = True
            elif char == ":" and not is_escape:
                is_parsing_index = True
            elif char == ";" and not is_escape:
                if is_parsing_index:
                    link_pair_indexes[node_index] = int(index_buffer)
                    index_buffer = ''
                    is_parsing_index = False
                self.append(data_buffer)
                indexes_to_nodes[node_index] = self.tail
                node_index += 1
                data_buffer = ''
            else:
                is_escape = False
                if is_parsing_index:
                    index_buffer += char
                else:
                    data_buffer += char

        for node_index_from, node_index_to in link_pair_indexes.items():
            if indexes_to_nodes.get(node_index_from) is not None:
                indexes_to_nodes.get(node_index_from).rand = indexes_to_nodes.get(node_index_to)


input_list = ["An:d", "he;re", "we;:go:", "Lorem", "ipsum", "dolor", "sit", "amet,", "consectetur", "adipiscing"]

first_list = ListRand()

for e in input_list:
    first_list.append(e)

first_list.add_random_link_by_index(0, 2)
first_list.add_random_link_by_index(3, 3)
first_list.add_random_link_by_index(4, 0)
first_list.add_random_link_by_index(6, 4)
first_list.add_random_link_by_index(6, 3)
first_list.add_random_link_by_index(9, 8)
# first_list.add_random_link_by_index(8, 12) # Will cause "index out of range"

first_list.serialize('serialized.txt')

second_list = ListRand()
second_list.deserialize('serialized.txt')

first_list.print_list_with_ids()
print('========')
second_list.print_list_with_ids()
