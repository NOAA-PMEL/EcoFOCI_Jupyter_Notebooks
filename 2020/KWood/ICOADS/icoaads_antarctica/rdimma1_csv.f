C=============================================================================C
C International Comprehensive Ocean-Atmosphere Data Set (ICOADS)  20 Sep 2016 C
C Filename:level: rdimma1_csv.f:01A                           Fortran program C
C Purpose: Read ICOADS Subset CSV files                     Author: Zaihua Ji C
C=============================================================================C
C Built based on rwimma1:01D
C Compile: gfortran -o rdimma1_csv rdimma1_csv.f
C Run: rdimma1_csv < subset.csv > subset.txt
C
C Data are read into Character (CVALUE), Integer (IVALUE) and
C Float (FVALUE) arrays. In these arrays, character missing value is set
C to empty string, integer missing values is set to -9999999, and float
C missing value is set = -9999999..
C
C This program also dumps the data in a fixed format output. The field length
C and missing values are defined in the arrays as in the BLOCK DATA BDIMMA.
C------------------------------------------------------------------------------
      PROGRAM RDIMMA1_CSV
      IMPLICIT INTEGER(A-E,G-Z)
C
C      CHARACTER*12 PROGID
C      DATA PROGID/'RDIMMA1_CSV'/
C
      PARAMETER(NUM=219,VNUM=200,FMISS=-9999999.,IMISS=-9999999)
      PARAMETER(STDOUT=6)
      CHARACTER*8 ABBR,AFMTS,OMISS
      DIMENSION VIDX(VNUM), VLEN(VNUM)
      COMMON /IMMA1/ILEN(NUM),ABBR(NUM),FMIN1(NUM),FMAX1(NUM),
     + AFMTS(NUM),OMISS(NUM),FUNITS(NUM),ITYPE(NUM)
C
      CHARACTER*1024, RPT, OUTRPT, CVALUE*20
      COMMON /VDATA/IVALUE(VNUM),FVALUE(VNUM),CVALUE(VNUM)
      DATA CVALUE/VNUM*' '/,IVALUE/VNUM*IMISS/,FVALUE/VNUM*FMISS/
C
      NREC = 0
      VCNT = 0
      OUTLEN = 0
C
C  READ VARIABLE NAMES
      READ(*,'(A)',END=900)RPT
      CALL READVARS(RPT,VIDX,VLEN,VCNT,OUTLEN)
C
C READ REPORT
  100 CONTINUE
      READ(*,'(A)',END=900)RPT
C
C INCREMENT NUMBER OF REPORTS READ
      NREC = NREC + 1
C
C READ IN CHARACTER, INTEGER AND FLOAT VALUES AND BUILD OUTRPT
      CALL READRPT(RPT,VIDX,VLEN,VCNT,OUTRPT)
C
C DUMP OUTRPT
      WRITE(STDOUT, '(A)') OUTRPT(2:OUTLEN)
C
      GOTO 100
C
C END OF FILE
  900 CONTINUE
C      WRITE(STDOUT,*)'REPORTS ',NREC
C
      END
C=============================================================================C
C WARNING:  Code beyond this point should not require any modification.       C
C=============================================================================C
C------------------------------------------------------------------------------
      SUBROUTINE READVARS(RPT,VIDX,VLEN,VCNT,OUTLEN)
C INITIALIZE ARRY VARS AND VIDX
      IMPLICIT INTEGER(A-E,G-Z)
      CHARACTER*(*) RPT
      PARAMETER(NUM=219, VNUM=200)
      DIMENSION VIDX(VNUM),VLEN(VNUM)
C
      CHARACTER*8 ABBR, AFMTS, VID, VNAME, OMISS, LDSPCS
      COMMON /IMMA1/ILEN(NUM),ABBR(NUM),FMIN1(NUM),FMAX1(NUM),
     + AFMTS(NUM),OMISS(NUM),FUNITS(NUM),ITYPE(NUM)
C
      VCNT = 0
      OUTLEN = 0
      RLEN = LENTRM(RPT)
      POS1 = 1
      POS2 = INDEX(RPT, ",") - 1
 9100 CONTINUE
      READ(RPT(POS1:POS2), *) VNAME
      POS = INDEX(VNAME, "-")
      VID = LDSPCS(VNAME(POS+1:))

      I = 0
 9101 CONTINUE
      IF (I .LT. NUM) THEN
         I = I + 1
         IF (ABBR(I) .NE. VID) GOTO 9101
         VCNT = VCNT + 1
         VIDX(VCNT) = I
         VLEN(VCNT) = ILEN(I) + 1
         IF(FUNITS(I) .GT. 0 .AND. FUNITS(I) .LT. 1.0) THEN
            VLEN(VCNT) = VLEN(VCNT) + 1
         ENDIF
         OUTLEN = OUTLEN + VLEN(VCNT)
      ELSE
         PRINT *, "**" // VID // "**"
         STOP 'Unkown Variable Name!'
      ENDIF

      POS1 = POS2 + 2
      IF (POS1 .LT. RLEN) THEN
         POS = INDEX(RPT(POS1:), ",")
         IF (POS .EQ. 0) THEN
            POS2 = RLEN
         ELSE
            POS2 = POS + POS1 - 2
         ENDIF
         GOTO 9100
      ENDIF
      END
C------------------------------------------------------------------------------
      SUBROUTINE READRPT(RPT,VIDX,VLEN,VCNT,OUTRPT)
C INITIALIZE ARRY VARS AND VIDX
      IMPLICIT INTEGER(A-E,G-Z)
      PARAMETER(NUM=219, VNUM=200)
      CHARACTER*(*) RPT, OUTRPT
      DIMENSION VIDX(VNUM),VLEN(VNUM)
      CHARACTER*20 CVALUE
      COMMON /VDATA/IVALUE(VNUM),FVALUE(VNUM),CVALUE(VNUM)
      CHARACTER*8 AFMT,ABBR,AFMTS,OMISS
      COMMON /IMMA1/ILEN(NUM),ABBR(NUM),FMIN1(NUM),FMAX1(NUM),
     + AFMTS(NUM),OMISS(NUM),FUNITS(NUM),ITYPE(NUM)
C
      RLEN = LENTRM(RPT)
      POS1 = 1
      OFF = 1
      OUTRPT = ' '
      DO 9200 N = 1, VCNT
         IF (N .EQ. VCNT) THEN
            POS2 = RLEN
         ELSE
            POS2 = POS1 + INDEX(RPT(POS1:), ",") - 2
         ENDIF
         IDX = VIDX(N)
         AFMT = AFMTS(IDX)
         IF (POS2 .LT. POS1) THEN   ! EMPTY VALUE
            IF (ITYPE(IDX) .EQ. 3) THEN
               WRITE(OUTRPT(OFF:), AFMT) ' '
            ELSE
               OUTRPT(OFF:) = OMISS(IDX)
            ENDIF
         ELSEIF (ITYPE(IDX) .EQ. 1) THEN
            READ(RPT(POS1:POS2), *) IVALUE(N)
            WRITE(OUTRPT(OFF:), AFMT) IVALUE(N)
         ELSEIF (ITYPE(IDX) .EQ. 2) THEN
            READ(RPT(POS1:POS2), *) FVALUE(N)
            WRITE(OUTRPT(OFF:), AFMT) FVALUE(N)
         ELSEIF (ITYPE(IDX) .EQ. 3) THEN
            READ(RPT(POS1:POS2), *) CVALUE(N)
            WRITE(OUTRPT(OFF:), AFMT) CVALUE(N)
         ENDIF
         POS1 = POS2 + 2
         OFF = OFF + VLEN(N)
 9200 CONTINUE
      END
C------------------------------------------------------------------------------
      FUNCTION LENTRM(STR)
C LENGTH OF A STRING MINUS TRAILING BLANKS
      CHARACTER STR*(*)
C
      DO 9300 LENTRM = LEN(STR), 1, -1
        IF (STR(LENTRM:LENTRM).NE.' ') RETURN
 9300 CONTINUE
      END
C------------------------------------------------------------------------------
      CHARACTER*8 FUNCTION LDSPCS(STR)
C ADD LEADING SPACES IF TRIMMED STRING LENGTH IS LESS THEN 5
      CHARACTER STR*(*)
C
      LDSPCS = ' '
      LSTR = LENTRM(STR)
      LPOS = 6 - LSTR
      WRITE(LDSPCS(LPOS:), '(A)') STR(1:LSTR)
      END
C------------------------------------------------------------------------------
      BLOCK DATA BDIMMA
C COMMON BLOCK DATA STATEMENTS
      IMPLICIT INTEGER(A-E,G-Z)
C
C     missing = -9999999
C     ILEN    = field length
C     ABBR    = field abbreviation
C     FMIN1   = field range minimum (first, or only)
C     FMAX1   = field range maximum (first, or only)
C     AFMTS   = field write out format
C     OMISS   = field misssing values
C     FUNITS  = field units
C     ITYPE   = 1: integer
C               2: float
C               3: character
C
      PARAMETER(NUM=219)
      CHARACTER*8 ABBR, AFMTS, OMISS
      COMMON /IMMA1/ILEN(NUM),ABBR(NUM),FMIN1(NUM),FMAX1(NUM),
     + AFMTS(NUM),OMISS(NUM),FUNITS(NUM),ITYPE(NUM)
C
      DATA (ILEN(I),ABBR(I),FMIN1(I),FMAX1(I),AFMTS(I),OMISS(I),
     + FUNITS(I),ITYPE(I),I=1,16)/
     +   4,'   YR', 1600.   , 2024. ,'(i5)',  '-9999',  1.    , 1,
     +   2,'   MO',    1.   ,   12. ,'(i3)',  '-99',    1.    , 1,
     +   2,'   DY',    1.   ,   31. ,'(i3)',  '-99',    1.    , 1,
     +   4,'   HR',    0.00 ,  23.99,'(f6.2)','-99.99', 0.01  , 2,
     +   5,'  LAT',  -90.00 ,  90.00,'(f7.2)','-999.99',0.01  , 2,
     +   6,'  LON',    0.00 , 359.99,'(f8.2)','-9999.99',0.01 , 2,
     +   2,'   IM',    0.   ,   99. ,'(i3)',  '-99',    1.    , 1,
     +   1,' ATTC',    0.   ,   35. ,'(1x,a1)', ' ',    0.    , 3,
     +   1,'   TI',    0.   ,    3. ,'(i2)',  '-9',     1.    , 1,
     +   1,'   LI',    0.   ,    6. ,'(i2)',  '-9',     1.    , 1,
     +   1,'   DS',    0.   ,    9. ,'(i2)',  '-9',     1.    , 1,
     +   1,'   VS',    0.   ,    9. ,'(i2)',  '-9',     1.    , 1,
     +   2,'  NID',    0.   ,   99. ,'(i3)',  '-99',    1.    , 1,
     +   2,'   II',    0.   ,   10. ,'(i3)',  '-99',    1.    , 1,
     +   9,'   ID',   32.   ,  126. ,'(1x,a9)',' ',     0.    , 3,
     +   2,'   C1',   48.   ,   57. ,'(1x,a2)',' ',     0.    , 3/
      DATA (ILEN(I),ABBR(I),FMIN1(I),FMAX1(I),AFMTS(I),OMISS(I),
     + FUNITS(I),ITYPE(I),I=17,48)/
     +   1,'   DI',    0.   ,    6. ,'(i2)',  '-9',     1.    , 1,
     +   3,'    D',    1.   ,  362. ,'(i4)',  '-999',   1.    , 1,
     +   1,'   WI',    0.   ,    8. ,'(i2)',  '-9',     1.    , 1,
     +   3,'    W',    0.0  ,   99.9,'(f5.1)','-99.9',  0.1   , 2,
     +   1,'   VI',    0.   ,    2. ,'(i3)',  '-99',    1.    , 1,
     +   2,'   VV',   90.   ,   99. ,'(i3)',  '-99',    1.    , 1,
     +   2,'   WW',    0.   ,   99. ,'(i3)',  '-99',    1.    , 1,
     +   1,'   W1',    0.   ,    9. ,'(i2)',  '-9',     1.    , 1,
     +   5,'  SLP',  870.0  , 1074.6,'(f7.1)','-9999.9',0.1   , 2,
     +   1,'    A',    0.   ,    8. ,'(i2)',  '-9',     1.    , 1,
     +   3,'  PPP',    0.0  ,   51.0,'(f5.1)','-99.9',  0.1   , 2,
     +   1,'   IT',    0.   ,    9. ,'(i2)',  '-9',     1.    , 1,
     +   4,'   AT',  -99.9  ,   99.9,'(f6.1)','-999.9', 0.1   , 2,
     +   1,' WBTI',    0.   ,    3. ,'(i2)',  '-9',     1.    , 1,
     +   4,'  WBT',  -99.9  ,   99.9,'(f6.1)','-999.9', 0.1   , 2,
     +   1,' DPTI',    0.   ,    3. ,'(i2)',  '-9',     1.    , 1,
     +   4,'  DPT',  -99.9  ,   99.9,'(f6.1)','-999.9', 0.1   , 2,
     +   2,'   SI',    0.   ,   12. ,'(i3)',  '-99',    1.    , 1,
     +   4,'  SST',  -99.9  ,   99.9,'(f6.1)','-999.9', 0.1   , 2,
     +   1,'    N',    0.   ,    9. ,'(i2)',  '-9',     1.    , 1,
     +   1,'   NH',    0.   ,    9. ,'(i2)',  '-9',     1.    , 1,
     +   1,'   CL',    0.   ,   10. ,'(1x,a1)',' ',     0.    , 3,
     +   1,'   HI',    0.   ,    1. ,'(i2)',  '-9',     1.    , 1,
     +   1,'    H',    0.   ,   10. ,'(1x,a1)',  ' ',   0.    , 3,
     +   1,'   CM',    0.   ,   10. ,'(1x,a1)',  ' ',   0.    , 3,
     +   1,'   CH',    0.   ,   10. ,'(1x,a1)',  ' ',   0.    , 3,
     +   2,'   WD',    0.   ,   38. ,'(i3)',  '-99',    1.    , 1,
     +   2,'   WP',    0.   ,   30. ,'(i3)',  '-99',    1.    , 1,
     +   2,'   WH',    0.   ,   99. ,'(i3)',  '-99',    1.    , 1,
     +   2,'   SD',    0.   ,   38. ,'(i3)',  '-99',    1.    , 1,
     +   2,'   SP',    0.   ,   30. ,'(i3)',  '-99',    1.    , 1,
     +   2,'   SH',    0.   ,   99. ,'(i3)',  '-99',    1.    , 1/
      DATA (ILEN(I),ABBR(I),FMIN1(I),FMAX1(I),AFMTS(I),OMISS(I),
     + FUNITS(I),ITYPE(I),I=49,68)/
     +   1,'  BSI',    0.,       0. ,'(i2)',  '-9',     1.    , 1,
     +   3,'  B10',    1.   ,  648. ,'(i4)',  '-999',   1.    , 1,
     +   2,'   B1',    0.   ,   99. ,'(i3)',  '-99',    1.    , 1,
     +   3,'  DCK',    0.   ,  999. ,'(i4)',  '-999',   1.    , 1,
     +   3,'  SID',    0.   ,  999. ,'(i4)',  '-999',   1.    , 1,
     +   2,'   PT',    0.   ,   21. ,'(i3)',  '-99',    1.    , 1,
     +   2,' DUPS',    0.   ,   14. ,'(i3)',  '-99',    1.    , 1,
     +   1,' DUPC',    0.   ,    2. ,'(i2)',  '-9',     1.    , 1,
     +   1,'   TC',    0.   ,    1. ,'(i2)',  '-9',     1.    , 1,
     +   1,'   PB',    0.   ,    2. ,'(i2)',  '-9',     1.    , 1,
     +   1,'   WX',    1.   ,    1. ,'(i2)',  '-9',     1.    , 1,
     +   1,'   SX',    1.   ,    1. ,'(i2)',  '-9',     1.    , 1,
     +   2,'   C2',    0.   ,   40. ,'(i3)',  '-99',    1.    , 1,
     +  12,' AQCS',    1.   ,   35. ,'(1x,a12)', ' ',   0.    , 3,
     +   1,'   ND',    1.   ,    2. ,'(i2)',  '-9',     1.    , 1,
     +   6,' TRMS',    1.   ,   15. ,'(1x,a6)',  ' ',   0.    , 3,
     +  14,' NQCS',    1.   ,   10. ,'(1x,a14)', ' ',   0.    , 3,
     +   2,'  QCE',    0.   ,   63. ,'(i3)',  '-99',    1.    , 1,
     +   1,'   LZ',    1.   ,    1. ,'(i2)',  '-9',     1.    , 1,
     +   2,'  QCZ',    0.   ,   31. ,'(i3)',  '-99',    1.    , 1/
      DATA (ILEN(I),ABBR(I),FMIN1(I),FMAX1(I),AFMTS(I),OMISS(I),
     + FUNITS(I),ITYPE(I),I=69,105)/
     +   1,'   OS',    0.   ,    6. ,'(i2)',  '-9',     1.    , 1,
     +   1,'   OP',    0.   ,    9. ,'(i2)',  '-9',     1.    , 1,
     +   1,'   FM',    0.   ,   35. ,'(1x,a1)',  ' ',   0.    , 3,
     +   1,' IMMV',    0.   ,   35. ,'(1x,a1)',  ' ',   0.    , 3,
     +   1,'   IX',    1.   ,    7. ,'(i2)',  '-9',     1.    , 1,
     +   1,'   W2',    0.   ,    9. ,'(i2)',  '-9',     1.    , 1,
     +   1,'  WMI',    0.   ,    9. ,'(i2)',  '-9',     1.    , 1,
     +   2,'  SD2',    0.   ,   38. ,'(i3)',  '-99',    1.    , 1,
     +   2,'  SP2',    0.   ,   30. ,'(i3)',  '-99',    1.    , 1,
     +   2,'  SH2',    0.   ,   99. ,'(i3)',  '-99',    1.    , 1,
     +   1,'   IS',    1.   ,    5. ,'(i2)',  '-9',     1.    , 1,
     +   2,'   ES',    0.   ,   99. ,'(i3)',  '-99',    1.    , 1,
     +   1,'   RS',    0.   ,    4. ,'(i2)',  '-9',     1.    , 1,
     +   1,'  IC1',    0.   ,   10. ,'(1x,a1)',  ' ',   0.    , 3,
     +   1,'  IC2',    0.   ,   10. ,'(1x,a1)',  ' ',   0.    , 3,
     +   1,'  IC3',    0.   ,   10. ,'(1x,a1)',  ' ',   0.    , 3,
     +   1,'  IC4',    0.   ,   10. ,'(1x,a1)',  ' ',   0.    , 3,
     +   1,'  IC5',    0.   ,   10. ,'(1x,a1)',  ' ',   0.    , 3,
     +   1,'   IR',    0.   ,    4. ,'(i2)',  '-9',     1.    , 1,
     +   3,'  RRR',    0.   ,  999. ,'(i4)',  '-999',   1.    , 1,
     +   1,'   TR',    1.   ,    9. ,'(i2)',  '-9',     1.    , 1,
     +   1,'   NU',   32.   ,  126. ,'(1x,a1)',  ' ',   0.    , 3,
     +   1,'  QCI',    0.   ,    9. ,'(i2)',  '-9',     1.    , 1,
     +  20,'  QIS',    0.   ,    9. ,'(1x,a20)', ' ',   0.    , 3,
     +   1,' QI21',    0.   ,    9. ,'(i2)',  '-9',     1.    , 1,
     +   3,'  HDG',    0.   ,  360. ,'(i4)',  '-999',   1.    , 1,
     +   3,'  COG',    0.   ,  360. ,'(i4)',  '-999',   1.    , 1,
     +   2,'  SOG',    0.   ,   99. ,'(i3)',  '-99',    1.    , 1,
     +   2,'  SLL',    0.   ,   99. ,'(i3)',  '-99',    1.    , 1,
     +   3,' SLHH',  -99.   ,   99. ,'(i4)',  '-999',   1.    , 1,
     +   3,'  RWD',    1.   ,  362. ,'(i4)',  '-999',   1.    , 1,
     +   3,'  RWS',    0.0  ,   99.9,'(f5.1)','-99.9',  0.1   , 2,
     +   8,' QI22',    0.   ,    9. ,'(1x,a8)',  ' ',   0.    , 3,
     +   4,'   RH',    0.0  ,  100.0,'(f6.1)','-999.9', 0.1   , 2,
     +   1,'  RHI',    0.   ,    4. ,'(i2)',  '-9',     1.    , 1,
     +   1,' AWSI',    0.   ,    2. ,'(i2)',  '-9',     1.    , 1,
     +   7,'IMONO',    0.  ,9999999.,'(i8)','-9999999', 1.    , 1/
      DATA (ILEN(I),ABBR(I),FMIN1(I),FMAX1(I),AFMTS(I),OMISS(I),
     + FUNITS(I),ITYPE(I),I=106,124)/
     +   4,' CCCC',   65.   ,   90. ,'(1x,a4)',  ' ',   0.    , 3,
     +   6,' BUID',   48.   ,   57. ,'(1x,a6)',  ' ',   0.    , 3,
     +   1,'FBSRC',    0.   ,    0. ,'(i2)',  '-9',     1.    , 1,
     +   5,'  BMP',  870.0  , 1074.6,'(f7.1)','-9999.9',0.1   , 2,
     +   4,' BSWU',  -99.9  ,   99.9,'(f6.1)','-999.9', 0.1   , 2,
     +   4,'  SWU',  -99.9  ,   99.9,'(f6.1)','-999.9', 0.1   , 2,
     +   4,' BSWV',  -99.9  ,   99.9,'(f6.1)','-999.9', 0.1   , 2,
     +   4,'  SWV',  -99.9  ,   99.9,'(f6.1)','-999.9', 0.1   , 2,
     +   4,' BSAT',  -99.9  ,   99.9,'(f6.1)','-999.9', 0.1   , 2,
     +   3,' BSRH',    0.   ,  100. ,'(i4)',  '-999',   1.    , 1,
     +   3,'  SRH',    0.   ,  100. ,'(i4)',  '-999',   1.    , 1,
     +   5,' BSST', -99.99  ,  99.99,'(f7.2)','-999.99',0.01  , 2,
     +   1,'  MST',    0.   ,    9. ,'(i2)',  '-9',     1.    , 1,
     +   4,'  MSH', -999.   , 9999. ,'(i5)',  '-9999',  1.    , 1,
     +   4,'   BY',    0.   , 9999. ,'(i5)',  '-9999',  1.    , 1,
     +   2,'   BM',    1.   ,   12. ,'(i3)',  '-99',    1.    , 1,
     +   2,'   BD',    1.   ,   31. ,'(i3)',  '-99',    1.    , 1,
     +   2,'   BH',    0.   ,   23. ,'(i3)',  '-99',    1.    , 1,
     +   2,'  BFL',    0.   ,   99. ,'(i3)',  '-99',    1.    , 1/
      DATA (ILEN(I),ABBR(I),FMIN1(I),FMAX1(I),AFMTS(I),OMISS(I),
     + FUNITS(I),ITYPE(I),I=125,145)/
     +   1,'  MDS',    0.   ,    2. ,'(i2)',  '-9',     1.    , 1,
     +   2,'  C1M',   65.   ,   90. ,'(1x,a2)',  ' ',   0.    , 3,
     +   2,'  OPM',    0.   ,   99. ,'(i3)',  '-99',    1.    , 1,
     +   2,'  KOV',   32.   ,  126. ,'(1x,a2)',  ' ',   0.    , 3,
     +   2,'  COR',   65.   ,   90. ,'(1x,a2)',  ' ',   0.    , 3,
     +   3,'  TOB',   32.   ,  126. ,'(1x,a3)',  ' ',   0.    , 3,
     +   3,'  TOT',   32.   ,  126. ,'(1x,a3)',  ' ',   0.    , 3,
     +   2,'  EOT',   32.   ,  126. ,'(1x,a2)',  ' ',   0.    , 3,
     +   2,'  LOT',   32.   ,  126. ,'(1x,a2)',  ' ',   0.    , 3,
     +   1,'  TOH',   32.   ,  126. ,'(1x,a1)',  ' ',   0.    , 3,
     +   2,'  EOH',   32.   ,  126. ,'(1x,a2)',  ' ',   0.    , 3,
     +   3,'  SIM',   32.   ,  126. ,'(1x,a3)',  ' ',   0.    , 3,
     +   3,'  LOV',    0.   ,  999. ,'(i4)',  '-999',   1.    , 1,
     +   2,'  DOS',    0.   ,   99. ,'(i3)',  '-99',    1.    , 1,
     +   3,'  HOP',    0.   ,  999. ,'(i4)',  '-999',   1.    , 1,
     +   3,'  HOT',    0.   ,  999. ,'(i4)',  '-999',   1.    , 1,
     +   3,'  HOB',    0.   ,  999. ,'(i4)',  '-999',   1.    , 1,
     +   3,'  HOA',    0.   ,  999. ,'(i4)',  '-999',   1.    , 1,
     +   5,'  SMF',    0.   ,99999. ,'(i6)',  '-99999', 1.    , 1,
     +   5,'  SME',    0.   ,99999. ,'(i6)',  '-99999', 1.    , 1,
     +   2,'  SMV',    0.   ,   99. ,'(i3)',  '-99',    1.    , 1/
      DATA (ILEN(I),ABBR(I),FMIN1(I),FMAX1(I),AFMTS(I),OMISS(I),
     + FUNITS(I),ITYPE(I),I=146,168)/
     +   5,'  OTV',  -3.000 ,38.999 ,'(f7.3)','-99.999',0.001 , 2,
     +   4,'  OTZ',    0.00 , 99.99 ,'(f6.2)','-99.99', 0.01  , 2,
     +   5,'  OSV',   0.000 ,40.999 ,'(f7.3)','-99.999',0.001 , 2,
     +   4,'  OSZ',    0.00 , 99.99 ,'(f6.2)','-99.99', 0.01  , 2,
     +   4,'  OOV',    0.00 , 12.99 ,'(f6.2)','-99.99', 0.01  , 2,
     +   4,'  OOZ',    0.00 , 99.99 ,'(f6.2)','-99.99', 0.01  , 2,
     +   4,'  OPV',    0.00 , 30.99 ,'(f6.2)','-99.99', 0.01  , 2,
     +   4,'  OPZ',    0.00 , 99.99 ,'(f6.3)','-99.99', 0.01  , 2,
     +   5,' OSIV',    0.00 ,250.99 ,'(f7.2)','-999.99',0.01  , 2,
     +   4,' OSIZ',    0.00 , 99.99 ,'(f6.2)','-99.99', 0.01  , 2,
     +   5,'  ONV',    0.00 ,500.99 ,'(f7.2)','-999.99',0.01  , 2,
     +   4,'  ONZ',    0.00 , 99.99 ,'(f6.2)','-99.99', 0.01  , 2,
     +   3,' OPHV',    6.20 ,  9.20 ,'(f5.2)','-9.99',  0.01  , 2,
     +   4,' OPHZ',    0.00 , 99.99 ,'(f6.2)','-99.99', 0.01  , 2,
     +   4,'  OCV',    0.00 , 50.99 ,'(f6.2)','-99.99', 0.01  , 2,
     +   4,'  OCZ',    0.00 , 99.99 ,'(f6.2)','-99.99', 0.01  , 2,
     +   3,'  OAV',    0.00 ,  3.10 ,'(f6.2)','-99.99', 0.01  , 2,
     +   4,'  OAZ',    0.00 , 99.99 ,'(f6.2)','-99.99', 0.01  , 2,
     +   4,' OPCV',    0.0  ,999.0  ,'(f6.1)','-999.9', 0.1   , 2,
     +   4,' OPCZ',    0.00 , 99.99 ,'(f6.2)','-99.99', 0.01  , 2,
     +   2,'  ODV',    0.0  ,  4.0  ,'(f4.1)','-9.9',   0.1   , 2,
     +   4,'  ODZ',    0.00 , 99.99 ,'(f6.2)','-99.99', 0.01  , 2,
     +  10,' PUID',    32.  ,126.   ,'(1x,a10)', ' ',   0.    , 3/
      DATA (ILEN(I),ABBR(I),FMIN1(I),FMAX1(I),AFMTS(I),OMISS(I),
     + FUNITS(I),ITYPE(I),I=169,183)/
     +   1,'  CCE',    0.   ,   13. ,'(1x,a1)',  ' ',   0.    , 3,
     +   2,'  WWE',    0.   ,   99. ,'(i3)',  '-99',    1.    , 1,
     +   1,'   NE',    0.   ,    8. ,'(i2)',  '-9',     1.    , 1,
     +   1,'  NHE',    0.   ,    8. ,'(i2)',  '-9',     1.    , 1,
     +   1,'   HE',    0.   ,    9. ,'(i2)',  '-9',     1.    , 1,
     +   2,'  CLE',    0.   ,   11. ,'(i3)',  '-99',    1.    , 1,
     +   2,'  CME',    0.   ,   12. ,'(i3)',  '-99',    1.    , 1,
     +   1,'  CHE',    0.   ,    9. ,'(i2)',  '-9',     1.    , 1,
     +   3,'   AM',    0.   ,    8. ,'(f5.2)','-9.99',  0.01  , 2,
     +   3,'   AH',    0.   ,    8. ,'(f5.2)','-9.99',  0.01  , 2,
     +   1,'   UM',    0.   ,    8. ,'(i2)',  '-9',     1.    , 1,
     +   1,'   UH',    0.   ,    8. ,'(i2)',  '-9',     1.    , 1,
     +   1,'  SBI',    0.   ,    1. ,'(i2)',  '-9',     1.    , 1,
     +   4,'   SA',  -90.0  ,   90.0,'(f6.1)','-999.9', 0.1   , 2,
     +   4,'   RI',   -1.10 ,   1.17,'(f6.2)','-99.99', 0.01  , 2/
      DATA (ILEN(I),ABBR(I),FMIN1(I),FMAX1(I),AFMTS(I),OMISS(I),
     + FUNITS(I),ITYPE(I),I=184,196)/
     +   2,' ICNR',    0.   ,   99. ,'(i3)',  '-99',    1.    , 1,
     +   2,'  FNR',    1.   ,   99. ,'(i3)',  '-99',    1.    , 1,
     +   2,' DPRO',    1.   ,   99. ,'(i3)',  '-99',    1.    , 1,
     +   2,' DPRP',    1.   ,   99. ,'(i3)',  '-99',    1.    , 1,
     +   1,'  UFR',    1.   ,    6. ,'(i2)',  '-9',     1.    , 1,
     +   7,' MFGR',-999999.,9999999.,'(i8)', '-9999999',1.    , 1,
     +   7,'MFGSR',-999999.,9999999.,'(i8)', '-9999999',1.    , 1,
     +   7,'  MAR',-999999.,9999999.,'(i8)', '-9999999',1.    , 1,
     +   7,' MASR',-999999.,9999999.,'(i8)', '-9999999',1.    , 1,
     +   7,'  BCR',-999999.,9999999.,'(i8)', '-9999999',1.    , 1,
     +   4,' ARCR',   48.   ,   57. ,'(1x,a4)', ' ',    0.    , 3,
     +   8,'  CDR',   48.   ,   57. ,'(1x,a8)', ' ',    0.    , 3,
     +   1,' ASIR',    0.   ,    1. ,'(i2)',  '-9',     1.    , 1/
      DATA (ILEN(I),ABBR(I),FMIN1(I),FMAX1(I),AFMTS(I),OMISS(I),
     + FUNITS(I),ITYPE(I),I=197,213)/
     +   2,' ICNI',    0.   ,   99. ,'(i3)',  '-99',     1.   , 1,
     +   2,'  FNI',    1.   ,   99. ,'(i3)',  '-99',     1.   , 1,
     +   1,' JVAD',    0.   ,   35. ,'(1x,a1)',  ' ',    0.   , 3,
     +   6,'  VAD',-99999.  ,999999.,'(i7)',  '-999999', 1.   , 1,
     +   1,'IVAU1',    1.   ,   35. ,'(1x,a1)',  ' ',    0.   , 3,
     +   1,'JVAU1',    0.   ,   35. ,'(1x,a1)',  ' ',    0.   , 3,
     +   6,' VAU1',-99999.  ,999999.,'(i7)',  '-999999', 1.   , 1,
     +   1,'IVAU2',    1.   ,   35. ,'(1x,a1)',  ' ',    0.   , 3,
     +   1,'JVAU2',    0.   ,   35. ,'(1x,a1)',  ' ',    0.   , 3,
     +   6,' VAU2',-99999.  ,999999.,'(i7)',  '-999999', 1.   , 1,
     +   1,'IVAU3',    1.   ,   35. ,'(1x,a1)',  ' ',    0.   , 3,
     +   1,'JVAU3',    0.   ,   35. ,'(1x,a1)',  ' ',    0.   , 3,
     +   6,' VAU3',-99999.  ,999999.,'(i7)',  '-999999', 1.   , 1,
     +   1,'  VQC',    1.   ,    4. ,'(i2)',  '-9',      1.   , 1,
     +   4,' ARCI',   48.   ,   57. ,'(1x,a4)',  ' ',    0.   , 3,
     +   8,'  CDI',   48.   ,   57. ,'(1x,a8)',  ' ',    0.   , 3,
     +   1,' ASII',    0.   ,    1. ,'(i2)',  '-9',      1.   , 1/
      DATA (ILEN(I),ABBR(I),FMIN1(I),FMAX1(I),AFMTS(I),OMISS(I),
     + FUNITS(I),ITYPE(I),I=214,219)/
     +   6,'  UID',   48.   ,   57. ,'(1x,a6)',  ' ',    0.   , 3,
     +   1,'  RN1',    0.   ,   35. ,'(1x,a1)',  ' ',    0.   , 3,
     +   1,'  RN2',    0.   ,   35. ,'(1x,a1)',  ' ',    0.   , 3,
     +   1,'  RN3',    0.   ,   35. ,'(1x,a1)',  ' ',    0.   , 3,
     +   1,'  RSA',    0.   ,    2. ,'(i2)',  '-9',      1.   , 1,
     +   1,'  IRF',    0.   ,    2. ,'(i2)',  '-9',      1.   , 1/
      END
