import sys

def ReadFile(path):
    try:
        with open(path, 'r', encoding="utf-8") as f:
            return f.readlines()
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

def WriteFileAdder(path, content):
    try:
        with open(path, 'a', encoding="utf-8") as f:
            for line in content:
                f.write(f'{line.strip()}\n')
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: fileadder.py [target path] [content path]")
        sys.exit(1)
    WriteFileAdder(sys.argv[1], ReadFile(sys.argv[2]))
    print(f"Added the content to {sys.argv[1]}")
