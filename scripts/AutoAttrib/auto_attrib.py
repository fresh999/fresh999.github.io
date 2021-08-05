from markdown.preprocessors import Preprocessor
import numpy as np
import re

def find_fenced_code_blocks(lines):
    ids = []
    for i, line in enumerate(lines):
        pattern = re.compile(r'^\~{3}')
        if pattern.match(line):
            ids.append(i)
    return ids

class AutoAttrib(Preprocessor):
    def run(self, lines):
        new_lines = []
        ids = find_fenced_code_blocks(lines)
        print(ids)
        blocks = [sl.tolist() for sl in np.split(lines, ids)]
        print(blocks)
        return new_lines


if __name__ == '__main__':

    l = ['~~~', 'ushd', 'kisjvb~~~']

    a = AutoAttrib()
    lines = a.run(l)
