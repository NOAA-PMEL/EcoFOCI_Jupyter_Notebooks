# SWOT Data Prepping and Processing

Data Requirements are spelled out in the working document.
- Three independent datastreams
    + GPS (NMEA GPPGA string)
    + PRAWE (engineering) - not included in L1 data
    + PRAWC (science)
    + Load - not included in L1 data
    + Met/Baro 
    
Currently these get parsed into three seperate RUDICS -> ERDDAP processes.  
- process NMEA string 
- process and convert Science values (units conversions and add salinity)

Would be best if this data can all be synthesized dynamically and housed in an erddap system (so that only new subsets are pulled)
- build xml for each dataset using deployment config file, output as ACDD/CF NetCDF File
- limitations to erddap compared to what NASA wants if one file is desired.  Alternatively we can have three subsets of data.

Instruments/Datastreams:
- GPS
- BARO
- PRAW / CTD 
- Platform (N201?)

Variable Metadata
INSTR_INFO

------
Any time gridding/mapping? Not for L1, each datastream can be independent (Prawler Sci/Engr, Float/GPS/Load)
Format (NetCDF)

-----
Done by JPL:
- QC Flags
- Product Synthesis

Need to vet data periodically and submit data peridically (https? sftp? rsync? open erddap instance?)