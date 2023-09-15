# sde-assign1

node1 = Node('localhost', 12345)
threading.Thread(target=node1.listen).start()

node2 = Node('localhost', 12346)
threading.Thread(target=node2.listen).start()

# To store data in node2 from node1:
response = node1.store('localhost', 12346, 'some_key', 'Hello, P2P World!')

# To retrieve data from node2:
data = node1.retrieve('localhost', 12346, 'some_key')
