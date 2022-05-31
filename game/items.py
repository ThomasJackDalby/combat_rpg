class Item:
    def __init__(self, name):
        self.name = name

def load_items(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
    
    items = []
    for line in lines:
        data = line.split(" ")
        item = Item(data[0])
        items.append(item)
    return items

if __name__ == "__main__":
    items = load_items("items.txt")
    
    from tabulate import tabulate
    print(tabulate(([item.name] for item in items), headers=["Name"]))