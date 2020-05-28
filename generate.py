#!python

import os
import sys
from datetime import datetime

if __name__ == '__main__': 
    if len(sys.argv) < 2: 
        print('Please specify a Doctrine to generate a post for')
    if len(sys.argv) == 2:
        if sys.argv[1][-1] != '/': sys.argv[1]+='/' #add trailing / to input if it's not already there
        working_dir = sys.argv[1]
        print(working_dir)
        try:
            os.remove(working_dir + 'out.txt')
        except:
            pass

        try:
            with open(working_dir + 'template.txt', 'r') as template:
                template= template.readlines()
        except Exception as e:
            print(e)
        while True:
            for line in range(len(template)):
                if '[TIMESTAMP]' in template[line]:
                    split = template[line].split("[TIMESTAMP]")
                    split.insert(1, datetime.utcnow().strftime('%Y.%m.%d %H:%M:%S'))
                    template[line] = ''.join(split)
                if '[Fit=' in template[line]:
                    fit_file = template[line][5:-2].rstrip() + '.txt'
                    template.pop(line)
                    
                    if len(fit_file.split('/')) < 2:
                        fit_file = working_dir + fit_file
                    print(fit_file)
                    with open(fit_file, 'r') as fit:
                        fit = fit.readlines()
                        fit.append('\n')
                        fit.reverse()
                        for mod in fit:
                            template.insert(line, mod)
                    break
                if line == len(template)-1:
                    with open(working_dir + 'out.txt', 'w') as output:
                        output.writelines(template)
                    print("fits successfully inserted, output in 'out.txt' in specified directory")
                    sys.exit(0)