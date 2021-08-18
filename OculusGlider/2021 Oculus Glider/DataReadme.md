# General SG402 - Newport Discussion for Data/Science Data

## Instrumentation
- sbe T/S

## Dataflow

1) OCG -> Basestation (w/ initial basestation parameters)
2) Basestation -> Akutan (cronjob) and Basestation -> thundersnow (launchd) ***do not sync these directories via rsync***
3) To DAC/ERDDAP:
    a) Akutan -> Profile .nc files GliderDAC (after any quick modifications / attribute updates)
    b) Akutan -> Timeseries/UpandDown .nc files ecofoci-field erddap (after any quick modifications / attribute updates)
