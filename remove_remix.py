#!/usr/bin/env python3

import os
import re

crawl_dir = "/data/user/musics"

lf = os.listdir(crawl_dir)


r1 = '(-\w)*[Rr][Ee][Mm][Ii][Xx](\w)*'
r2 = '(-\w)*[Nn][Oo][Nn][Ss][Tt][Oo][Pp](\w)*'
r3 = '(-\w)*[Dd][Jj](\w)*'
rm = re.compile(r'(%s|%s|%s)' % (r1,r2,r3))

for f in lf:
    if rm.search(f.split(".")[0]):
        print("%80s" % str(f), end=" ")
        os.system("rm \"" + crawl_dir + "/" + f + "\"")
        print("removed")
