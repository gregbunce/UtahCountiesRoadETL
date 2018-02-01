import arcpy

# this function recalcs the listed fields to empty string if ' ', == None, or is None
def CalcUtransFields (rows):
    for row in rows:
        if row.ADDRSYS_L == ' ' or row.ADDRSYS_L == None or row.ADDRSYS_L is None:
            row.ADDRSYS_L = ""
        if row.ADDRSYS_R == ' ' or row.ADDRSYS_R == None or row.ADDRSYS_R is None:
            row.ADDRSYS_R = ""
        if row.CARTOCODE == ' ' or row.CARTOCODE == None or row.CARTOCODE is None:
            row.CARTOCODE = ""
        if row.FULLNAME == ' ' or row.FULLNAME == None or row.FULLNAME is None:
            row.FULLNAME = ""
        if row.PREDIR == ' ' or row.PREDIR == None or row.PREDIR is None:
            row.PREDIR = ""
        if row.NAME == ' ' or row.NAME == None or row.NAME is None:
            row.NAME = ""
        if row.POSTTYPE == ' ' or row.POSTTYPE == None or row.POSTTYPE is None:
            row.POSTTYPE = ""
        if row.POSTDIR == ' ' or row.POSTDIR == None or row.POSTDIR is None:
            row.POSTDIR = ""
        if row.A1_PREDIR == ' ' or row.A1_PREDIR == None or row.A1_PREDIR is None:
            row.A1_PREDIR = ""
        if row.A1_NAME == ' ' or row.A1_NAME == None or row.A1_NAME is None:
            row.A1_NAME = ""
        if row.A1_POSTTYPE == ' ' or row.A1_POSTTYPE == None or row.A1_POSTTYPE is None:
            row.A1_POSTTYPE = ""
        if row.A1_POSTDIR == ' ' or row.A1_POSTDIR == None or row.A1_POSTDIR is None:
            row.A1_POSTDIR = ""
        if row.A2_PREDIR == ' ' or row.A2_PREDIR == None or row.A2_PREDIR is None:
            row.A2_PREDIR = ""
        if row.A2_NAME == ' ' or row.A2_NAME == None or row.A2_NAME is None:
            row.A2_NAME = ""
        if row.A2_POSTTYPE == ' ' or row.A2_POSTTYPE == None or row.A2_POSTTYPE is None:
            row.A2_POSTTYPE = ""
        if row.A2_POSTDIR == ' ' or row.A2_POSTDIR == None or row.A2_POSTDIR is None:
            row.A2_POSTDIR = ""
        if row.AN_NAME == ' ' or row.AN_NAME == None or row.AN_NAME is None:
            row.AN_NAME = ""
        if row.AN_POSTDIR == ' ' or row.AN_POSTDIR == None or row.AN_POSTDIR is None:
            row.AN_POSTDIR = ""
        if row.QUADRANT_L == ' ' or row.QUADRANT_L == None or row.QUADRANT_L is None:
            row.QUADRANT_L = ""
        if row.QUADRANT_R == ' ' or row.QUADRANT_R == None or row.QUADRANT_R is None:
            row.QUADRANT_R = ""
        if row.POSTCOMM_L == ' ' or row.POSTCOMM_L == None or row.POSTCOMM_L is None:
            row.POSTCOMM_L = ""
        if row.POSTCOMM_R == ' ' or row.POSTCOMM_R == None or row.POSTCOMM_R is None:
            row.POSTCOMM_R = ""
        if row.DOT_CLASS == ' ' or row.DOT_CLASS == None or row.DOT_CLASS is None:
            row.DOT_CLASS = ""
        if row.DOT_FCLASS == ' ' or row.DOT_FCLASS == None or row.DOT_FCLASS is None:
            row.DOT_FCLASS = ""
        if row.DOT_HWYNAM == ' ' or row.DOT_HWYNAM == None or row.DOT_HWYNAM is None:
            row.DOT_HWYNAM = ""
        if row.DOT_RTNAME == ' ' or row.DOT_RTNAME == None or row.DOT_RTNAME is None:
            row.DOT_RTNAME = ""
        if row.DOT_RTPART == ' ' or row.DOT_RTPART == None or row.DOT_RTPART is None:
            row.DOT_RTPART = ""
        if row.SOURCE == ' ' or row.SOURCE == None or row.SOURCE is None:
            row.SOURCE = ""
        if row.UTRANS_NOTES == ' ' or row.UTRANS_NOTES == None or row.UTRANS_NOTES is None:
            row.UTRANS_NOTES = ""
        if row.LOCAL_UID == ' ' or row.LOCAL_UID == None or row.LOCAL_UID is None:
            row.LOCAL_UID = ""
        if row.STATUS == ' ' or row.STATUS == None or row.STATUS is None:
            row.STATUS = ""
        if row.ACCESSCODE == ' ' or row.ACCESSCODE == None or row.ACCESSCODE is None:
            row.ACCESSCODE = ""
        if row.FROMADDR_L is None:
            row.FROMADDR_L = 0
        if row.TOADDR_L is None:
            row.TOADDR_L = 0
        if row.FROMADDR_R is None:
            row.FROMADDR_R = 0
        if row.TOADDR_R is None:
            row.TOADDR_R = 0
        rows.updateRow(row)
    del row


# this function returns an array of current ng911-based roads schema fields and their specs
def GetUtransFieldSpecs ():
    fieldsSpecs = [
        ("STATUS", "TEXT", "", "", 15),
        ("CARTOCODE", "TEXT", "", "", 10),
        ("FULLNAME", "TEXT", "", "", 50),
        ("FROMADDR_L", "DOUBLE"),
        ("TOADDR_L", "DOUBLE"),
        ("FROMADDR_R", "DOUBLE"),
        ("TOADDR_R", "DOUBLE"),
        ("PARITY_L", "TEXT", "", "", 1),
        ("PARITY_R", "TEXT", "", "", 1),
        ("PREDIR", "TEXT", "", "", 2),
        ("NAME", "TEXT", "", "", 40),
        ("POSTTYPE", "TEXT", "", "", 4),
        ("POSTDIR", "TEXT", "", "", 2),
        ("AN_NAME", "TEXT", "", "", 10),
        ("AN_POSTDIR", "TEXT", "", "", 2),
        ("A1_PREDIR", "TEXT", "", "", 2),
        ("A1_NAME", "TEXT", "", "", 40),
        ("A1_POSTTYPE", "TEXT", "", "", 4),
        ("A1_POSTDIR", "TEXT", "", "", 2),
        ("A2_PREDIR", "TEXT", "", "", 2),
        ("A2_NAME", "TEXT", "", "", 40),
        ("A2_POSTTYPE", "TEXT", "", "", 4),
        ("A2_POSTDIR", "TEXT", "", "", 2),
        ("QUADRANT_L", "TEXT", "", "", 2),
        ("QUADRANT_R", "TEXT", "", "", 2),
        ("STATE_L", "TEXT", "", "", 2),
        ("STATE_R", "TEXT", "", "", 2),
        ("COUNTY_L", "TEXT", "", "", 30),
        ("COUNTY_R", "TEXT", "", "", 30),
        ("ADDRSYS_L", "TEXT", "", "", 30),
        ("ADDRSYS_R", "TEXT", "", "", 30),
        ("POSTCOMM_L", "TEXT", "", "", 30),
        ("POSTCOMM_R", "TEXT", "", "", 30),
        ("ZIPCODE_L", "TEXT", "", "", 5),
        ("ZIPCODE_R", "TEXT", "", "", 5),
        ("INCMUNI_L", "TEXT", "", "", 30),
        ("INCMUNI_R", "TEXT", "", "", 30),
        ("UNINCCOM_L", "TEXT", "", "", 30),
        ("UNINCCOM_R", "TEXT", "", "", 30),
        ("NBRHDCOM_L", "TEXT", "", "", 30),
        ("NBRHDCOM_R", "TEXT", "", "", 30),
        ("ER_CAD_ZONES", "TEXT", "", "", 255),
        ("ESN_L", "TEXT", "", "", 5),
        ("ESN_R", "TEXT", "", "", 5),
        ("MSAGCOMM_L", "TEXT", "", "", 30),
        ("MSAGCOMM_R", "TEXT", "", "", 30),
        ("ONEWAY", "TEXT", "", "", 1),
        ("VERT_LEVEL", "TEXT", "", "", 1),
        ("SPEED_LMT", "SHORT"),
        ("ACCESSCODE", "TEXT", "", "", 1),
        ("DOT_HWYNAM", "TEXT", "", "", 15),
        ("DOT_RTNAME", "TEXT", "", "", 11),
        ("DOT_RTPART", "TEXT", "", "", 3),
        ("DOT_F_MILE", "SHORT"),
        ("DOT_T_MILE", "SHORT"),
        ("DOT_FCLASS", "TEXT", "", "", 20),
        ("DOT_SRFTYP", "TEXT", "", "", 30),
        ("DOT_CLASS", "TEXT", "", "", 1),
        ("DOT_OWN_L", "TEXT", "", "", 30),
        ("DOT_OWN_R", "TEXT", "", "", 30),
        ("DOT_AADT", "DOUBLE"),
        ("DOT_AADTYR", "TEXT", "", "", 4),
        ("DOT_THRULANES", "SHORT"),
        ("BIKE_L", "TEXT", "", "", 4),
        ("BIKE_R", "TEXT", "", "", 4),
        ("BIKE_PLN_L", "TEXT", "", "", 15),
        ("BIKE_PLN_R", "TEXT", "", "", 15),
        ("BIKE_REGPR", "TEXT", "", "", 5),
        ("BIKE_NOTES", "TEXT", "", "", 50),
        ("UNIQUE_ID", "TEXT", "", "", 75),
        ("LOCAL_UID", "TEXT", "", "", 30),
        ("UTAHRD_UID", "TEXT", "", "", 100),
        ("SOURCE", "TEXT", "", "", 75),
        ("UPDATED", "DATE"),
        ("EFFECTIVE", "DATE"),
        ("EXPIRE", "DATE"),
        ("CREATED", "DATE"),
        ("CREATOR", "TEXT", "", "", 20),
        ("EDITOR", "TEXT", "", "", 20),
        ("CUSTOMTAGS", "TEXT", "", "", 1000),
        ("UTRANS_NOTES", "TEXT", "", "", 50),
    ]
    return fieldsSpecs


def UpperCoreUtransFields (rows):
    for row in rows:
        if row.PREDIR != '':
            row.PREDIR = row.PREDIR.upper()
        if row.NAME != '':
            row.NAME = row.NAME.upper()
        if row.POSTTYPE != '':
            row.POSTTYPE = row.POSTTYPE.upper()
        if row.POSTDIR != '':
            row.POSTDIR = row.POSTDIR.upper()
        if row.A1_PREDIR != '':
            row.A1_PREDIR = row.A1_PREDIR.upper()
        if row.A1_NAME != '':
            row.A1_NAME = row.A1_NAME.upper()
        if row.A1_POSTTYPE != '':
            row.A1_POSTTYPE = row.A1_POSTTYPE.upper()
        if row.A1_POSTDIR != '':
            row.A1_POSTDIR = row.A1_POSTDIR.upper()
        if row.A2_PREDIR != '':
            row.A2_PREDIR = row.A2_PREDIR.upper()
        if row.A2_NAME != '':
            row.A2_NAME = row.A2_NAME.upper()
        if row.A2_POSTTYPE != '':
            row.A2_POSTTYPE = row.A2_POSTTYPE.upper()
        if row.A2_POSTDIR != '':
            row.A2_POSTDIR = row.A2_POSTDIR.upper()
        if row.AN_NAME != '':
            row.AN_NAME = row.AN_NAME.upper()
        if row.AN_POSTDIR != '':
            row.AN_POSTDIR = row.AN_POSTDIR.upper()
        rows.updateRow(row)
    del row


## get a list of road type domain names and descriptions
#def GetRoadTypeDomains (geoDatabaseNgSchema):
#    listOfDomains = []
#    domains = arcpy.da.ListDomains(geoDatabaseNgSchema)

#    for domain in domains:
#        if domain.name == 'CVDomain_StreetType':
#            coded_values = domain.codedValues
#            for val, desc in coded_values.items():
#                listOfDomains.append(val.upper())
#                listOfDomains.append(desc.upper())
#    return listOfDomains


## remove the post type if the street name is numeric
#def removePostTypeIfNumeric(rows):
#    for row in rows:
#        if len(row.NAME) == 1:
#            if row.NAME[0].isdigit():
#                row.POSTTYPE = ""
#        rows.updateRow(row)
#    del row