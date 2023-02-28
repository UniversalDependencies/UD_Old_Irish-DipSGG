import os
from conllu import parse

cur_dir = os.getcwd()
main_dir = cur_dir[0:cur_dir.find("not-to-release") - 1]
os.chdir(main_dir)


def check_release(file_name):
    """Checks a file set for release to ensure all sentence numbers are in the correct order,
       Renumbers them appropriately if they are not, and creates a new file."""

    with open(file_name, mode="r", encoding="utf-8") as file:
        check_file = file.read()

    parsed_file = parse(check_file)
    checked_file = []

    for sent_index, sentence in enumerate(parsed_file):
        sent_num = int(sentence.metadata.get("sent_id"))
        if sent_index + 1 != sent_num:
            sentence.metadata["sent_id"] = f"{sent_index + 1}"
        checked_file.append(sentence.serialize())

    checked_file = "".join(checked_file)

    if check_file != checked_file:
        with open(f"{file_name}_old", mode="w", encoding="utf-8") as file:
            file.write(check_file)
        with open(file_name, mode="w", encoding="utf-8") as file:
            file.write(checked_file)
        return f"Differences found, file updated and old file renamed: {file_name}_old."
    else:
        return "No differences found, file ready for upload."


if __name__ == "__main__":

    print(check_release("sga_dipsgg-ud-test.conllu"))
