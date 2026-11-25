
# OPTIMAL DATABASE SEARCH STRUCTURE
# Dynamic Programming - Optimal Binary Search Tree

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class OptimalBST:

    def __init__(self, keys, freq):
        self.keys = keys
        self.freq = freq
        self.n = len(keys)

        self.cost = [[0] * self.n for _ in range(self.n)]
        self.root = [[0] * self.n for _ in range(self.n)]

        self.tree = None
        self.minimum_cost = 0

    def construct(self):

        # Base case: Single key
        for i in range(self.n):
            self.cost[i][i] = self.freq[i]
            self.root[i][i] = i

        # Consider subtrees of increasing lengths
        for length in range(2, self.n + 1):

            for i in range(self.n - length + 1):

                j = i + length - 1
                total_freq = sum(self.freq[i:j + 1])

                self.cost[i][j] = float('inf')

                # Try every key as root
                for r in range(i, j + 1):

                    left = self.cost[i][r - 1] if r > i else 0
                    right = self.cost[r + 1][j] if r < j else 0

                    current_cost = left + right + total_freq

                    if current_cost < self.cost[i][j]:
                        self.cost[i][j] = current_cost
                        self.root[i][j] = r

        self.minimum_cost = self.cost[0][self.n - 1]

        # Build the actual tree
        self.tree = self.build_tree(0, self.n - 1)

    def build_tree(self, i, j):

        if i > j:
            return None

        r = self.root[i][j]
        node = Node(self.keys[r])

        node.left = self.build_tree(i, r - 1)
        node.right = self.build_tree(r + 1, j)

        return node

    def display_table(self):

        print("\n========== DP COST TABLE ==========")

        print("     ", end="")
        for key in self.keys:
            print(f"{key:>8}", end="")
        print()

        for i in range(self.n):
            print(f"{self.keys[i]:>5}", end="")

            for j in range(self.n):
                if j < i:
                    print(f"{'-':>8}", end="")
                else:
                    print(f"{self.cost[i][j]:>8}", end="")
            print()

        print("\n========== ROOT TABLE ==========")

        print("     ", end="")
        for key in self.keys:
            print(f"{key:>8}", end="")
        print()

        for i in range(self.n):
            print(f"{self.keys[i]:>5}", end="")

            for j in range(self.n):
                if j < i:
                    print(f"{'-':>8}", end="")
                else:
                    r = self.root[i][j]
                    print(f"{self.keys[r]:>8}", end="")
            print()

    def display_tree(self, node=None, level=0, side="ROOT"):

        if node is None:
            if level == 0:
                node = self.tree
            else:
                return

        if node is None:
            print("Tree is empty.")
            return

        if node.right:
            self.display_tree(node.right, level + 1, "RIGHT")

        print("    " * level + f"|-- {node.key} ({side})")

        if node.left:
            self.display_tree(node.left, level + 1, "LEFT")

    def search(self, key):

        current = self.tree
        comparisons = 0

        while current:
            comparisons += 1

            if key == current.key:
                return True, comparisons

            elif key < current.key:
                current = current.left

            else:
                current = current.right

        return False, comparisons

    def weighted_cost(self):

        total = 0

        def calculate(node, level):

            nonlocal total

            if node is None:
                return

            index = self.keys.index(node.key)
            total += self.freq[index] * level

            calculate(node.left, level + 1)
            calculate(node.right, level + 1)

        calculate(self.tree, 1)
        return total


# Normal BST for comparison

def normal_bst(keys):

    root = None

    for key in keys:

        new_node = Node(key)

        if root is None:
            root = new_node
            continue

        current = root

        while True:

            if key < current.key:

                if current.left is None:
                    current.left = new_node
                    break

                current = current.left

            else:

                if current.right is None:
                    current.right = new_node
                    break

                current = current.right

    return root


def normal_bst_cost(node, keys, freq, level=1):

    if node is None:
        return 0

    index = keys.index(node.key)

    return (freq[index] * level +
            normal_bst_cost(node.left, keys, freq, level + 1) +
            normal_bst_cost(node.right, keys, freq, level + 1))


# Input functions

def manual_input():

    n = int(input("\nEnter number of keys: "))

    if n <= 0:
        raise ValueError("Number of keys must be positive.")

    keys = []
    freq = []

    print("\nEnter keys in sorted order:")

    for i in range(n):
        keys.append(int(input(f"Key {i + 1}: ")))

    if len(set(keys)) != n or keys != sorted(keys):
        raise ValueError("Keys must be unique and sorted.")

    print("\nEnter search frequencies:")

    for i in range(n):
        f = int(input(f"Frequency of {keys[i]}: "))

        if f <= 0:
            raise ValueError("Frequency must be positive.")

        freq.append(f)

    return keys, freq


def sample_input():

    keys = [10, 20, 30, 40, 50]
    freq = [4, 2, 6, 3, 5]

    return keys, freq


# Main program

def main():

    keys = []
    freq = []
    obst = None

    while True:

        print("\n")
        print("=" * 55)
        print("          OPTIMAL DATABASE SEARCH STRUCTURE")
        print("              DYNAMIC PROGRAMMING")
        print("=" * 55)

        print("\n  1. Enter Keys and Frequencies")
        print("  2. Load Sample Dataset")
        print("  3. Construct Optimal Binary Search Tree")
        print("  4. Display DP Table and Search Results")
        print("  5. Exit")

        print("\n" + "-" * 55)

        choice = input("  Enter your choice: ").strip()

        try:

            if choice == '1':

                keys, freq = manual_input()
                obst = None

                print("\nDatabase data entered successfully.")

            elif choice == '2':

                keys, freq = sample_input()
                obst = None

                print("\nSample dataset loaded successfully.")
                print("\nKeys       :", keys)
                print("Frequencies:", freq)

            elif choice == '3':

                if not keys:
                    print("\nPlease enter data or load a sample first.")
                    continue

                obst = OptimalBST(keys, freq)
                obst.construct()

                normal_root = normal_bst(keys)
                normal_cost = normal_bst_cost(
                    normal_root, keys, freq
                )

                total_freq = sum(freq)

                print("\n========== OPTIMAL BST ==========")
                obst.display_tree()

                print("\n========== COST COMPARISON ==========")
                print("Normal BST Cost :", normal_cost)
                print("Optimal BST Cost:", obst.minimum_cost)

                print("\nAverage search cost:")
                print("Normal BST :", round(normal_cost / total_freq, 2))
                print("Optimal BST:", round(obst.minimum_cost / total_freq, 2))

                print("\nRoot Key:", keys[obst.root[0][obst.n - 1]])

            elif choice == '4':

                if obst is None:
                    print("\nPlease construct the Optimal BST first.")
                    continue

                obst.display_table()

                print("\n========== SEARCH ==========")

                key = int(input("Enter key to search: "))

                found, comparisons = obst.search(key)

                if found:
                    print(f"\nKey {key} found successfully.")
                else:
                    print(f"\nKey {key} not found.")

                print("Comparisons required:", comparisons)

                print("\n========== SEARCH ANALYSIS ==========")
                print("Minimum total search cost:", obst.minimum_cost)
                print("Total search frequency:", sum(freq))
                print("Average search cost:",
                      round(obst.minimum_cost / sum(freq), 2))

            elif choice == '5':

                print("\nThank you for using Optimal Database Search!")
                break

            else:
                print("\nInvalid choice. Please try again.")

        except ValueError as error:
            print("\nInput Error:", error)

        except Exception as error:
            print("\nError:", error)


if __name__ == "__main__":
    main()
