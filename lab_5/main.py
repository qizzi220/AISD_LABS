class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


# --- Обязательная часть ---

def insert(root, val):
    if root is None:
        return Node(val)

    if val < root.val:
        root.left = insert(root.left, val)
    elif val > root.val:
        root.right = insert(root.right, val)

    return root


def search(root, target):
    if root is None:
        return False

    if root.val == target:
        return True

    # рекурсивно ищем в нужном поддереве
    if target < root.val:
        return search(root.left, target)
    else:
        return search(root.right, target)


def inorder(root):
    # левое - корень - правое
    if root is not None:
        inorder(root.left)
        print(root.val, end=" ")
        inorder(root.right)


# --- Вариант 2 ---

def find_min(root):
    if root is None:
        return None

    # идем в самый левый узел
    curr = root
    while curr.left is not None:
        curr = curr.left

    return curr.val


def find_max(root):
    if root is None:
        return None

    # идем в самый правый узел
    curr = root
    while curr.right is not None:
        curr = curr.right

    return curr.val


# --- Блок для проверки ---

if __name__ == "__main__":
    root = None
    arr = [15, 10, 20, 8, 12, 17, 25]

    for i in arr:
        root = insert(root, i)

    print("Симметричный обход:")
    inorder(root)
    print("\n")

    print("Поиск 12:", search(root, 12))
    print("Поиск 50:", search(root, 50))
    print()

    print("Минимум:", find_min(root))
    print("Максимум:", find_max(root))