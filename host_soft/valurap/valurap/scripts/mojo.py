#!/usr/bin/env python
# -------------------------------------------------------------------------
# Mojo.py is a bitstream uploader for the mojo v2 board
# author    Matthew O'Gorman <mog@rldn.net>
# copyright 2013 Matthew O'Gorman
# version 2.0
# ### License : This program is free software, distributed under the terms of
#           the GNU General Public License Version 3. See the COPYING file
#           at the top of the source tree.
# -------------------------------------------------------------------------

import time
import sys
import argparse
import serial
import struct


def main():
    version = "Mojo v2.0 is licensed under the GPLv3 copyright 2013 Matthew O'Gorman"

    parser = argparse.ArgumentParser(description='Mojo bitstream loader v2')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('bitstream', metavar='BITSTREAM', nargs='?',
                       help='Bitstream file to upload to the Mojo.')
    group.add_argument('-i', '--install', metavar='BITSTREAM', dest='install', action='store',
                       help='Bitstream file to upload to the Mojo')
    parser.add_argument('-r', '--ram', dest='ram', action='store_const',
                        const=True, default=False,
                        help='Install bitstream file only to ram')
    # not currently supported by the default firmware of the board
    # group.add_argument('-c', '--copy', metavar='BITSTREAM', dest='copy', action='append', nargs='?',
    #                     help='Bitstream file to copy from the Mojo [Default: %(default)s]', default=['mojo.bin'])

    # group.add_argument('-o', '--only_verify', metavar='BITSTREAM', dest='only_verify', action='store',
    #                    help='Read flash of Mojo only to verify against bitstream.')
    # group.add_argument('-r', '--reboot', dest='reboot', action='store_const',
    #                    const=True, default=False,
    #                    help='Reboot mojo board.')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_const',
                        const=True, default=False,
                        help='Enable verbose output to cli.')
    parser.add_argument('-V', '--version', dest='version', action='store_const',
                        const=True, default=False,
                        help='Display version number of mojo.')
    parser.add_argument('-n', '--no-verify', dest='no_verify', action='store_const',
                        const=True, default=False,
                        help='Do not verify the operation to the Mojo.')
    group.add_argument('-e', '--erase', dest='erase', action='store_const',
                       const=True, default=False,
                       help='Erase flash on Mojo.')
    parser.add_argument('-d', '--device', dest='mojo_tty', action='store',
                        default='/dev/mojo',
                        help='Address of the serial port for the mojo [Default: %(default)s]') 

    args = parser.parse_args()

    if args.version:
        print(version)
        sys.exit(0)

    # Serial code
    try:
        ser = serial.Serial(args.mojo_tty, 19200, timeout=10)
    except Exception:
        print('No serial port found named ' + args.mojo_tty)
        sys.exit(1)

    if not args.bitstream and not args.install and not args.erase:
        print(parser.print_help())
        sys.exit(1)
    if args.erase:
        if args.verbose:
            print("Preparing to erase")
        erase_mojo(ser, args.verbose)
        sys.exit(0)
    if args.bitstream:
        install_mojo(ser, args.bitstream, args.verbose, args.no_verify, args.ram)
        sys.exit(0)
    if args.install:
        install_mojo(ser, args.install, args.verbose, args.no_verify, args.ram)
        sys.exit(0)


def install_mojo(ser, bitstream, verbose, no_verify, ram):
    file = open(bitstream, 'rb')
    bits = file.read()
    length = len(bits)
    reboot_mojo(ser, verbose)

    if ram:
        ser.write(b'R')
        ret = ser.read(1)
        if verbose and ret == 'R':
            print('Mojo is ready to recieve bitstream')
        else:
            print('Mojo did not respond correctly! Make sure the port is correct')
            sys.exit(1)

    if not ram and no_verify:
        ser.write(b'F')
        ret = ser.read(1)
        if verbose and ret == b'R':
            print('Mojo is ready to recieve bitstream')
        else:
            print('Mojo did not respond correctly! Make sure the port is correct')
            sys.exit(1)

    if not ram and not no_verify:
        ser.write(b'V')
        ret = ser.read(1)
        if verbose and ret == b'R':
            print('Mojo is ready to recieve bitstream')
        else:
            print('Mojo did not respond correctly! Make sure the port is correct')
            sys.exit(1)

    buffer = struct.unpack("4B", struct.pack("I", length))
    buf = bytearray()
    for i in buffer:
        buf.append(i)
    ser.write(buf)
    ret = ser.read(1)
    if verbose and ret == b'O':
        print('Mojo acknowledged size of bitstream. Writing bitstream')
    else:
        print('Mojo failed to acknowledge size of bitstream. Did not write')
        sys.exit(1)
    ser.write(bits)
    ret = ser.read(1)
    if verbose and ret == b'D':
        print('Mojo has been flashed')
    else:
        print('Mojo failed to flash correctly')
        sys.exit(1)

    if not ram and not no_verify:
        ser.write(b'S')
        if verbose:
            print('Verifying Mojo')
        ret = ser.read(1)
        if ret != b'\xAA':
            print('Flash does not contain valid start byte.')
            sys.exit(1)
        if verbose:
            print('First Byte was valid getting flash size.')
        ret = ser.read(4)
        flash_length = struct.unpack("I", ret)[0] - 5
        if flash_length != length:
            print('Flash is not same size as local bitstream.')
            sys.exit(1)
        if verbose:
            print('Flash and local bitstream match file size.')
        ret = ser.read(length)
        if ret != bits:
            print('Flash and local bitstream do not match.')
            sys.exit(1)
        if verbose:
            print('Flash and local bitstream are a match.')
    if not ram:
        ser.write(b'L')
        ret = ser.read(1)
        if ret != b'D':
            print('Mojo failed to load bitstream')
            sys.exit(1)
        if verbose:
            print('Mojo has been loaded bitsream')
    return


def reboot_mojo(ser, verbose):
    ser.setDTR(True)
    time.sleep(0.005)
    for i in range(0, 5):
        ser.setDTR(False)
        time.sleep(0.005)
        ser.setDTR(True)
        time.sleep(0.005)
    if verbose:
        print('Rebooting Mojo')
    return


def erase_mojo(ser, verbose):
    reboot_mojo(ser, verbose)
    ser.write(b'E')
    ret = ser.read(1)
    if ret != b'D':
        print('Failed to erase Mojo.  Error code: ' + ret)
        sys.exit(1)
    if verbose:
        print('Erased mojo successfully.')
    ser.close()
    return


if __name__ == '__main__':
    main()
