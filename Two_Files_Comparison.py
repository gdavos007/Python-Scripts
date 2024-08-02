# This script compares two semi-structured text files line by line.

file1 = 'file1.RPT'
file2 = 'file2.RPT'

# Read the contents of the files
with open(file1, 'r') as f1, open(file2, 'r') as f2:
    lines1 = f1.readlines()
    lines2 = f2.readlines()

# Compare line by line
for i, (line1, line2) in enumerate(zip(lines1, lines2)):
    if line1 != line2:
        print(f"Line {i + 1} differs:")
        print(f"File 1: {line1.strip()}")
        print(f"File 2: {line2.strip()}")

# Check if any file has extra lines
if len(lines1) > len(lines2):
    print("File 1 has extra lines starting from line", len(lines2) + 1)
elif len(lines2) > len(lines1):
    print("File 2 has extra lines starting from line", len(lines1) + 1)
