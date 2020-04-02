import os
import json
from tqdm import tqdm
import json
import pprint
import re
import numpy as np

pp = pprint.PrettyPrinter(indent=4)

main_texts = []
subfolders = [f.path for f in os.scandir() if f.is_dir()]
# subfolders = ["biorxiv_medrxiv"]
# subfolders = ["noncomm_use_subset"]
print(subfolders)

incubation_values = []

for index in range(len(subfolders)):
    # for index in tqdm(range(len(subfolders))):
    folder = subfolders[index]
    print(folder)
    # dobule nested (ex: foldername/foldername)
    folder_path = os.path.join(folder, folder)

    all_files = os.listdir(folder_path)
    # for filename_index in range(len(all_files)):
    for filename_index in tqdm(range(len(all_files))):
        filename = all_files[filename_index]
        name = filename.lower()
        if name.endswith(
            ".json"
        ):  # DO NOT ADD A FORMATTED VERSION, USE FILENAME (not name) for raw
            # print(name)

            with open(os.path.join(folder_path, filename)) as json_file:
                data = json.load(json_file)

                # array of entires
                body_text = data["body_text"]

                for entry in body_text:
                    text = entry["text"]
                    # period space used sop decimales arent counted as new sentences
                    sentences = text.split(". ")
                    for sentence in sentences:
                        # check multiple sentences bc u may mention same noun a lot in paragraph, but not in same sentence
                        if "incubation" in sentence:
                            # print("Incubation sentence found")

                            # print(sentence)

                            # search for a number/decimal followed by "day"
                            reg = r"(?=.[\d.]+)\s+(\S+)(\b(?=.\w*day\w*)\b)"
                            values = re.findall(reg, sentence)
                            for value in values:  # print the element
                                try:

                                    pure = float(value[0])
                                    # check for regex error
                                    if "e" in str(value[0]):

                                        # print("Range value")
                                        # print(value[0])
                                        e_ind = str(value[0]).index("e")
                                        # print(e_ind)

                                        # witha range, there are two vals, so we add both
                                        before = float(value[0][:e_ind])
                                        # print("before: " + str(before))

                                        after = float(value[0][e_ind + 1 :])
                                        # print("after: " + str(after))

                                        # print("\n")

                                        incubation_values.append(before)
                                        incubation_values.append(after)
                                    else:

                                        incubation_values.append(pure)

                                    # print(pure)
                                    # print("\n")

                                except:
                                    """
                                    print("erorr + " + str(value[0]))
                                    print("\n")
                                    """
                                    pass
                                    # get index of e
                                    """
                                    e_ind = str(value[0]).index("e")
                                    print(int(e_ind))
                                    # print(sentence)
                                    if int(e_ind) == 1:
                                        print("index : " + e_ind)
                                        print(value[0])
                                    """
                                    # print("Error occred")

                    # print(text)
                    # print("\n\n")
                    # main_texts.append(text)
                # pp.pprint(body_text)

                # for only 1 file
                # break


# print(main_texts)
print(incubation_values)

mean = np.mean(incubation_values)
mean = round(mean, 4)
print(mean)
