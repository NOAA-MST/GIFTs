#!/usr/bin/env python
"""Create and open permissions on skyfield's bsp_files cache directory.

Run this manually after installing GIFTs if gifts.swaDecoder's use of
skyfield fails to write ephemeris files due to directory permissions.
"""
import os

import skyfield


def main():
    bsp_directory = os.path.join(skyfield.__path__[0], 'bsp_files')
    if not os.path.exists(bsp_directory):
        os.mkdir(bsp_directory)
    os.chmod(bsp_directory, 0o777)


if __name__ == "__main__":
    main()
