sphinxformat
------------
This package is the implementation of the **Sphinx** packet format
described in the `paper`_ *"Sphinx: A compact and Provably Secure Mix
Format"* by `George Danezis`_ and `Ian Goldberg`_. It should be
considered a fork of the `original implementation`_ released by *Ian
Goldberg* on 2011-03-06, the initial commit of this repository. This
package is maintained by *Felipe Dau* and *David R. Andersen*, as
part of Felipe's Senior Design Project.

**Please, consider this package in alpha stage and do not use it in a
production environment.**

Cryptography
------------
Most of the cryptographic operations come from `pycrypto`_. The
following sections will provide more information about the other
tools that were used.

Elliptic Curve Cryptography (curve25519)
''''''''''''''''''''''''''''''''''''''''
The original implementation of Sphinx included `curve25519`_ by Dan
Bernstein, but the maintainers of this repository chose to use
`curve25519-donna`_ instead.

Large Block Cipher (LIONESS)
''''''''''''''''''''''''''''
The *LIONESS* implementation and the *xcounter* CTR mode class are
adapted from *"Experimental implementation of the sphinx
cryptographic mix packet format by George Danezis"*.

Dependencies
------------
Sphinx depends on *pycrypto* and *curve25519-donna*, which can be
easily installed with `pip`_::

    sudo pip install pycrypto curve25519-donna

Testing
-------
The original code includes a test that can be run with::

    ./SphinxClient.py  or  ./SphinxClient.py -ecc

The latter is smaller and faster, and if you used installed
*curve25519-donna*, *ECC* support should be available.

Feedback
--------
Please use the `GitHub issue tracker`_ to leave suggestions, bug
reports, complaints or anything you feel will contribute to Sphinx.

Contributing
------------
Contributions are more than welcome, and as this package is part of
Felipe's Senior Design Project, all the contributors of this
repository (until the project is concluded) will be mentioned on his
paper.

Acknowledgements
----------------
- Thanks to *David R. Andersen* for working on the development of
  this package and for supervising Felipe's Senior Design Project

- Thanks to *George Danezis* and *Ian Goldberg* for designing and
  implementing Sphinx

.. _`curve25519`: http://cr.yp.to/ecdh.html
.. _`curve25519-donna`: https://pypi.python.org/pypi/curve25519-donna
.. _`george danezis`: http://www0.cs.ucl.ac.uk/staff/G.Danezis
.. _`github issue tracker`: https://github.com/felipedau/sphinxformat/issues
.. _`ian goldberg`: https://cs.uwaterloo.ca/~iang
.. _`original implementation`: https://crysp.uwaterloo.ca/software/Sphinx-0.8.tar.gz
.. _`paper`: https://cypherpunks.ca/~iang/pubs/Sphinx_Oakland09.pdf
.. _`pip`: https://pypi.python.org/pypi/pip
.. _`pycrypto`: https://pypi.python.org/pypi/pycrypto
