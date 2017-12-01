W51 APEX data
=============

There are a few scripts here useful for retrieving the data and taking averages over them.

`retrieve_dataverse.py` will download all of the FITS images from the dataverse.  You should edit this file to change the output directory.


`avgspectra.py` will create noise-weighted averages of the cubes and plot
spectra of them with some line identifications overlaid.  This is a fairly
simple script, with most of the length dedicated to line frequency
specifications.  This can be modified to take Gaussian-weighted averages
to mimic extragalactic beams, for example.


`retrieve_data.py` retrieves the raw data from the ESO archive; it shouldn't be
needed except to reduce the data.  The data were reduced using
https://github.com/keflavich/sdpy, but the scripts may be lost to a dead hard
drive.
