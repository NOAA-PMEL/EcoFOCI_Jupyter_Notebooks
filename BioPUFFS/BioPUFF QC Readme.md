# PUF QC Readme

_Multiple data formats and versions have existed over the years_

- SBD Reconstructed data with various instruments and design characteristics
- ERDDAP hosted TELOS/FLOT format (science or non-science datastream)

All formats above should end in equivalent final product.... may involve renaming variables in datasets though.

All Units have a "Bottom" mode, a "Profile Mode" (this has been less successful due to timing/sampling desires) and a "Surface" mode.  Some have an "Under Ice" mode.

This means, erddap/sample wise, that there is a timeseries dataset, a profile dataset, and one or two trajectory datasets.  These are CF/COARDS naming standards... even though all the data could be listed as "other" or "timeseries" to keep it in a single dataset.

## Prelim Processing

### Steps
- Calc Temperature, Pressure, PAR, Chlor and other parameters (from engineering units)
    - Apply Cal Coef (turb, chlor)
    - apply derivation equations

### Metdata - seperate dataset
- remove known bad data (failed instruments)
- Prelim QC (range check): remove or flag? QUARTOD says flag... can always go back and add these

-> this data should be rehosted as a prelim Science dataset.  Include lat, lon.  

## Discrete Updates
- CTD validations?

## QUARTOD Derived?
- spikes
- horizontal checks

### Final Data Archive Format?
- Although we can add a lot to the final data metadata via erddap, its probably best if the archived final data is in netcdf with extensive metadata (as EcoFOCIpy tends to do)
- Whether code is written or a dataset is exported and rehosted in netcdf is probably best left up to the programmer.

