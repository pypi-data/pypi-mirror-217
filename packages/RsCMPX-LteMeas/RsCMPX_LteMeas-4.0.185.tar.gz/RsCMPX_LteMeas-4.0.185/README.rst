==================================
 RsCMPX_LteMeas
==================================

.. image:: https://img.shields.io/pypi/v/RsCMPX_LteMeas.svg
   :target: https://pypi.org/project/ RsCMPX_LteMeas/

.. image:: https://readthedocs.org/projects/sphinx/badge/?version=master
   :target: https://RsCMPX_LteMeas.readthedocs.io/

.. image:: https://img.shields.io/pypi/l/RsCMPX_LteMeas.svg
   :target: https://pypi.python.org/pypi/RsCMPX_LteMeas/

.. image:: https://img.shields.io/pypi/pyversions/pybadges.svg
   :target: https://img.shields.io/pypi/pyversions/pybadges.svg

.. image:: https://img.shields.io/pypi/dm/RsCMPX_LteMeas.svg
   :target: https://pypi.python.org/pypi/RsCMPX_LteMeas/

Rohde & Schwarz CMX/CMP LTE Measurement RsCMPX_LteMeas instrument driver.

Basic Hello-World code:

.. code-block:: python

    from RsCMPX_LteMeas import *

    instr = RsCMPX_LteMeas('TCPIP::192.168.2.101::hislip0')
    idn = instr.query('*IDN?')
    print('Hello, I am: ' + idn)

Check out the full documentation on `ReadTheDocs <https://RsCMPX_LteMeas.readthedocs.io/>`_.

Supported instruments: CMX500, CMP180, PVT360

The package is hosted here: https://pypi.org/project/RsCMPX_LteMeas/

Documentation: https://RsCMPX_LteMeas.readthedocs.io/

Examples: https://github.com/Rohde-Schwarz/Examples/


Version history
----------------

	Latest release notes summary: Update to FW 4.0.185

	Version 4.0.185
		- Update to FW 4.0.185

	Version 4.0.140
		- Update of RsCMPX_LteMeas to FW 4.0.140 from the complete FW package 7.10.0

	Version 4.0.60
		- Update of RsCMPX_LteMeas to FW 4.0.60

	Version 4.0.10
		- First released version