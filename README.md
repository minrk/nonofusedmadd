# No no-fused-madd

OS X 10.9 + System Python + Xcode 5.1 == can't compile anything ([more information on Stack Overflow](http://stackoverflow.com/questions/22313407)).

This script patches `_sysconfigdata.py` to remove the offending flag `-mno-fused-madd`.

It patches a file in `/System`, which is horrible, so probably nobody should ever use it.

To install:

    pip install nonofusedmadd

To undo the patch after installing:

    python -m nonofusedmadd restore

To reapply the patch:

    python -m nonofusedmadd patch

To show the diff

    python -m nonofusedmadd diff
