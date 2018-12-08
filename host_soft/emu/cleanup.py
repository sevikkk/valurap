import xml.etree.cElementTree as ET
import sys

def main(fn, fn2):
    tree = ET.ElementTree(file=fn)
    root = tree.getroot()
    for cell in root.iter("cell"):
        for child in cell:
            if child.tag == "output":
                cell.remove(child)
    tree = ET.ElementTree(root)
    with open(fn2, "w") as f:
        tree.write(f)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
