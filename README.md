# No no-fused-madd

OS X 10.9 + System Python + Xcode 5.1 = can't compile anything ([more information on Stack Overflow](http://stackoverflow.com/questions/22313407)).

This script patches `_sysconfigdata.py` to remove the offending flag `-mno-fused-madd`.

It patches a file in `/System`, **which is horrible, so probably nobody should ever use it**.

To install:

    sudo pip install nonofusedmadd

To undo the patch after installing:

    sudo python -m nonofusedmadd restore

To reapply the patch:

    sudo python -m nonofusedmadd patch

To show the diff

    python -m nonofusedmadd diff


Note that since this is for patching System Python, `sudo` is probably required.
There is no `--user` install that makes sense.

You can also just download the script without installing it, and do all the same actions with

    sudo python nonofusemadd.py

instead of `python -m nonofusemadd`.
