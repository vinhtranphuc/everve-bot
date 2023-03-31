from contextlib import nullcontext
import time
import numpy as np
from clicknium import clicknium as cc, ui, locator
from common import *
from everveFollowTiktok import *
from everveFollowTwitter import *

def main():
    initFollowTiktok()
    print('FOLLOW_TIKTOK: STOPPED')

    initFollowTwitter()
    print('FOLLOW_TWITTER: STOPPED')

main()
