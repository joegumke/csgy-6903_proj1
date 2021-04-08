#! /usr/bin/python

# Main Processing Function for NYU Trailblazers hillclimbing CODE

import argparse
import encryptor as encrypt 
import decryptor as decrypt


def main():
    parser = argparse.ArgumentParser()
    #parser.add_argument(
    #"ciphertext",
    #help="Ciphertext to analyze",
    #action="store"
    #)

    parser.add_argument(
    "-t",
    nargs="?",
    help="length of key  Variable from 0-24",
    action="store",
    dest="varT",
    type=int,
    choices=range(0,23)
    )

    parser.add_argument(
    "-v",
    nargs="?",
    help="Number of Words. Variable from 0-1,000",
    action="store",
    dest="varV",
    type=int,
    choices=range(0,500)
    )

    parser.add_argument(
    "-l",
    nargs="?",
    help="Length of Messages. Variable from 0-1,000",
    action="store",
    dest="varL",
    type=int,
    choices=range(0,500)
    )
    args = parser.parse_args()

    #Define variable names
    #ciphertext = args.ciphertext
    varT = args.varT

    encrypt.randomWordSelect(varT)

    #decrypt.decrypt(ciphertext)
    #encrypt.encrypt()

if __name__ == "__main__":
    main()


