#!python

import os
import sys

if __name__ == '__main__': 
    if len(sys.argv) < 2: 
        print('Please specify a directory to generate a post for')
    if len(sys.argv) == 2:
        if sys.argv[1][-1] != '/': sys.argv[1]+='/' #add trailing / to input if it's not already there
        os.chdir(sys.argv[1])
        os.remove('out.txt')
        
        try:
            with open('template.txt', 'r') as template:
                template= template.readlines()
        except Exception as e:
            print(e)
        while True:
            for line in range(len(template)):
                if '[Fit=' in template[line]:
                    fit_file = template[line][5:-2].rstrip()
                    template.pop(line)
                    with open(fit_file+'.txt', 'r') as fit:
                        fit = fit.readlines()
                        fit.append('\n')
                        fit.reverse()
                        for mod in fit:
                            template.insert(line, mod)
                    break
                if line == len(template)-1:
                    with open('out.txt', 'w') as output:
                        output.writelines(template)
                    print("fits successfully inserted, output in 'out.txt' in specified directory")
                    sys.exit(0)