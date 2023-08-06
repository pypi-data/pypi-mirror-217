# Testing a flexible command line interface for ipyvasp

import sys


def main():
    args = sys.argv[1:]

    if args[0].startswith("poscar."):
        attr = args[0].split(".")[1]
        from .lattice import POSCAR

        poscar = POSCAR()
        if attr == "get_kpath":
            assert len(args) >= 2, "poscar.get_kpath takes at least one argument"
            poscar.get_kpath(args[1])
