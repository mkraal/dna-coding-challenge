from pathlib import Path
from random import randint
from faker import Faker
from timeit import default_timer as timer


def generate_tests():
    fake = Faker()
    lines = []
    line_count = 1000000
    start = timer()
    for i in range(line_count):
        max_range = randint(10, 1000)
        line = fake.text(max_range).replace("\n", "")
        lines.append(f"{line}\n")
        if i % 100000 == 0 and i > 90000:
            end = timer()
            print(f"{i}/{line_count} - {end - start}s")

    file_path = Path(f"data/test_en_words_{line_count}_long_2.txt")
    with file_path.open("w") as f:
        f.writelines(lines)


generate_tests()
