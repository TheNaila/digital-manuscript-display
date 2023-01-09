import re


def create_dict(entry):
    has_title = False
    has_accession_num = False
    new_dictionary = {}
    # creates dict object
    for line in entry:
        line = line.strip()  # cutting off white-spaces from the ends
        splt_txt = line.split(':')  # ? what if no collon
        if splt_txt[0] != " " and splt_txt[0] != "":  # if empty line, skip
            if splt_txt[0].lower() == "title":
                has_title = True
            if splt_txt[0].lower() == "accession number":
                has_accession_num = True
            for count, item in enumerate(splt_txt):
                splt_txt[count] = item.strip()
        else:
            continue
        try:
            new_dictionary[splt_txt[0]] = splt_txt[1]
        except Exception as e:
            print("Please verify that all text is in the form 'Title: Text'")

    try:
        assert has_title, "Entry is missing Title"
    except Exception as e:
        print(e)
    try:
        assert has_accession_num, "Entry is missing Accession Number"
    except Exception as e:
        print(e)
        # don't allow submit button if assertions are false
    return new_dictionary


def main(text_file):
    import json

    file = open(text_file, 'r', encoding='utf-8')  # should specify the encoding type and the mode
    document_lines = file.readlines()  # each time you call the function it calls a new line

    # iterates through the documents line by line and creates a new entry in the entry dictionary
    current_entry = []
    entry_dictionary = []
    count = 0

    for line in document_lines:
        new_entry = re.search('^Maker', line)
        count = count + 1
        if re.match("^\s*$", line):
            continue
        elif new_entry is not None and len(current_entry) != 0:
            entry_dictionary.append(create_dict(current_entry))
            current_entry = []
            current_entry.append(line)
        elif count == len(document_lines):
            current_entry.append(line)
            entry_dictionary.append(create_dict(current_entry))
        else:
            current_entry.append(line)

    json = json.dumps(entry_dictionary, indent=4)
    # Writing to sample.json
    with open("test2.json", "w") as outfile:
        outfile.write(json)
    return "test2.json"
