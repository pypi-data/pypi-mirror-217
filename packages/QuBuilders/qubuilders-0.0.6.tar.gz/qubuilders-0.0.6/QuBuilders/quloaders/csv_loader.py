"""this code file is able to read the
questions from a csv  file and then return
the questions as a quseq object.
the csv file must have the following format otherwise it is not readable by this
reader.

the header of csv should be like this:
question_title; answers; choices; hints; descriptions
... and here each element.
note:delimiter of csv file must be ;"""


import csv
from QuBuilders import NchTan as NT


def read_file_c(file_object, name: str, descr: str):
    """the file_object is your file that you opened using
    open. name is the name for your question seq and descr is the
    descriptions for your question seq"""

    data = csv.reader(file_object, delimiter=';')
    next(data)
    obj = NT.QuSeq(name, descr)

    for question in data:
        qu = NT.QuestionDataSaver(question[0], eval(question[1]),
                                  eval(question[2]), question[3],
                                  question[4])
        obj += qu
    file_object.close()
    return obj



