#!python
#-*-coding:utf-8-*-
#Time-stamp: <Wed Jan 13 21:43:07 JST 2016>
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division

from zipfile import ZipFile
import json
import sys

hat_blocks = ["whenGreenFlag"]
var_blocks = {"setVar:to:": "=", "changeVar:by:": "+="}
rgb_blocks = {"red": "Red", "blue": "Blue", "green": "Green",
              "あか": "Red", "あお": "Blue", "みどり": "Green",
              "赤" : "Red", "青": "Blue", "緑": "Green",
              "レッド": "Red", "ブルー" : "Blue", "グリーン": "Green"}
control_blocks = {"wait:elapsed:from:": "DigiUSB.delay", "DigiUSB.blink": ""}
brace_blocks = {"doForever": "for", "doIf": "if"}

def main():
    with ZipFile("bottle.sbx", "r") as zf:
        with zf.open("project.json", "r") as pf:
            data = json.loads(pf.read().decode('utf-8'))


            # for vc in data['variables']:
            #     print("var {name};".format(**vc))

            main_data = None
            max_script = 0

            # choose longest loop
            for sc in data['scripts']:
                if(len(sc[2]) > max_script):
                    main_data = sc[2]

            for d in analyzeLoop(main_data):
                pass
                # print(d)
                # print("-----")

            # for v in main_data:
            #     # if isinstance(v, list):
            #     print(v[0])

def analyzeLoop(data):
    for d in data:
        command = d[0]
        if command in brace_blocks:
            if command == "doIf":
                command = "{}({} {} {})".format(brace_blocks[command], readVar(d[1][1]), d[1][0], d[1][2])
            elif command == "doForever":
                command = "for(;;)"
            print(command+"{")
            yield command
            yield from analyzeLoop(d[-1])
            print("}")
        else:
            if command in hat_blocks:
                command = command
            elif command in var_blocks:
                command = "{} {} {}".format(rgb_blocks[d[1]], var_blocks[d[0]], d[2])
            elif command in control_blocks:
                if command == "wait:elapsed:from:":
                    command = "{}({})".format(control_blocks[command],d[1]*1000)
                elif command == "DigiUSB.blink":
                    command = "int _r = {}; int _g = {}; int _b = {};".format(readVar(d[1]), readVar(d[2]), readVar(d[3]))
                    command += "\nRed = _r; Green = _g; Blue = _b"
            print(command + ";")
            yield command

def readVar(arg):
    if isinstance(arg, list):
        return rgb_blocks[arg[1]]
    else:
        return arg

if __name__ == '__main__':
    main()

