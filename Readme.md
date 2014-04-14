Ising2D
=======

##Usage
Run using:

    ./Ising2D.py {lattice size}x{lattice size}-B{magnetic field}

For example:

    ./Ising2D.py 10x10-B0

initializes a 10x10 lattice without an external field (B = 0).

##Command-line flags

 `+r` Only generate a report, don't re-calculate. For example:

    ./Ising2D.py 10x10-B0 +r

`-r` Only calculate, don't generate a report.

    ./Ising2D.py 10x10-B0 -r

Default (no flags): calculate and generate a report.

Requirements
==
Reports are generated using R.
