#!/usr/bin/python3
"""
Split and interactively page a string or a text file
"""

def more(text, pagelines=10):
    lines = text.splitlines()

    while lines:
        display_lines = lines[:pagelines]
        lines = lines[pagelines:]
        for line in display_lines:
            print(line)
        if lines and input('Need more?') not in ['', 'y', 'Y']:
            break

if __name__ == "__main__":
    import sys
    more(open(sys.argv[1]).read())

