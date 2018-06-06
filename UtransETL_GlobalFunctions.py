import arcpy
import os.path
from datetime import date

# global scope variables -- see bottom of file for those dependent on fucntion data, aka: variable is assigned after the functions have been instantiated
NextGenFGDB = "K:/AGRC Projects/UtransEditing/Data/UtahRoadsNGSchema.gdb"
officialPostTypeDomains = []

### THESE FUNCTIONS ARE USED IN THE COUNTY TO UTRANS SCRIPT ###
# this function recalcs the listed fields to empty string if ' ', == None, or is None
def CalcUtransFields (rows):
    for row in rows:

        #arrayOfStringFields = [ADDRSYS_L,ADDRSYS_R,CARTOCODE,FULLNAME,PREDIR,NAME,POSTTYPE,POSTDIR,A1_PREDIR,A1_NAME,A1_POSTTYPE,A1_POSTDIR,A2_PREDIR,A2_NAME,A2_POSTTYPE,A2_POSTDIR,AN_NAME,AN_POSTDIR,QUADRANT_L,QUADRANT_R,POSTCOMM_L,POSTCOMM_R,DOT_CLASS,DOT_FCLASS,DOT_HWYNAM,DOT_RTNAME,DOT_RTPART,UTRANS_NOTES,LOCAL_UID,STATUS,ACCESSCODE]
        #for stringField in arrayOfStringFields:
        #    if row.item == ' ' or row.item == None or row.item is None:
        #        row.item = ""

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
        if row.A1_PREDIR == ' 'or row.A1_PREDIR == None or row.A1_PREDIR is None:
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

# uppercase the needed fields
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

# remove special characters... apostophes, etc
def RemoveSpecialCharacters(rows):
    for row in rows:
        _original_name_value = row.getValue("NAME")
        _original_a1_name_value = row.getValue("A1_NAME")
        _original_a2_name_value = row.getValue("A2_NAME")

        _new_name_value = ""
        _new_a1_name_value = ""
        _new_a2_name_value = ""

        # check NAME
        if HasFieldValue(row.NAME):
            if not _original_name_value.isdigit() and "'" in _original_name_value:
                _new_name_value = _original_name_value.replace("'", "")
                row.NAME = _new_name_value
    
        # check A1_NAME
        if HasFieldValue(row.A1_NAME):
            if not _original_a1_name_value.isdigit() and "'" in _original_a1_name_value:
                _new_a1_name_value = _original_a1_name_value.replace("'", "")
                row.A1_NAME = _new_a1_name_value

        # check A2_NAME
        if HasFieldValue(row.A2_NAME):
            if not _original_a2_name_value.isdigit() and "'" in _original_a2_name_value:
                _new_a2_name_value = _original_a2_name_value.replace("'", "")
                row.A2_NAME = _new_a2_name_value

        rows.updateRow(row)
    del row

# apply agrc highway formatting to county's, if different
def FormatToAgrcHighwayNamingConvention(rows):
    for row in rows:
        _original_name_value = row.getValue("NAME")
        _new_name_value = ""
        _highway_name = ""
        _highway_number = ""

        # check NAME field for highway attributes
        if HasFieldValue(row.NAME):
            if not _original_name_value.isdigit():
                _original_name_value = _original_name_value.upper()

                # check if state or us route, if so then reformat
                if "US" in _original_name_value or "SR" in _original_name_value or "HWY" in _original_name_value:
                    # see if we can split the name on a numeric value
                    _highway_name = _original_name_value.rstrip('0123456789')
                    _highway_number = _original_name_value[len(_highway_name):]
                
                    if _highway_name != "" and _highway_number != "":
                        _highway_name = _highway_name.strip()
                        if _highway_name in ("US", "SR", "HWY") and _highway_number.isdigit():
                            _new_name_value = "HIGHWAY " + str(_highway_number)
                            # recalc NAME
                            row.NAME = _new_name_value
                            row.POSTTYPE = ""
                            # recalc DOT_HWYNAM
                            row.DOT_HWYNAM = str(_highway_name) + " " + str(_highway_number)
                # check if interstate, if so then reformat
                elif (_original_name_value in ('I70', 'I80', 'I15', 'I84')):
                      # split on 'I' and then add the '-'
                      _highway_interstate = _original_name_value.split('I')
                      _highway_interstate_reformatted = ""
                      if len(_highway_interstate) > 1:
                          if _highway_interstate[0] == "I" and _highway_interstate[1].isdigit(): 
                            _highway_interstate_reformatted = _highway_interstate[0] + "-" + _highway_interstate[1]
                            # recalc NAME
                            row.NAME = _highway_interstate_reformatted
                            row.POSTTYPE = ""
        rows.updateRow(row)
    del row


# Check the values in the A1 and A2 fields and if numeric then move to AN fields
def MoveNumericA1orA2ToANfield(rows):
    for row in rows:
        aliasFieldsList = ["A1_", "A2_"]

        # loop through the alias road name fields
        for aliasField in aliasFieldsList:
            if HasFieldValue(row.getValue(aliasField + "NAME")):
                _roadName = ""
                _roadName = str(row.getValue(aliasField + "NAME"))
                _postdir = ""
                _postdir = row.getValue(aliasField + "POSTDIR")
                 
                if _roadName.isdigit():
                    # it's digit so move the values to alias numeric fields
                    row.setValue("AN_NAME", _roadName)
                    row.setValue("AN_POSTDIR", _postdir)

                    # clear-out the alias alpha fields
                    if aliasField == "A1_":
                        row.A1_PREDIR = ""
                        row.A1_NAME = ""
                        row.A1_POSTTYPE = ""
                    else:
                        row.A2_PREDIR = ""
                        row.A2_NAME = ""
                        row.A2_POSTTYPE = ""

                # save the changes to the row
                rows.updateRow(row)
    del row




#### THESE FUNCTIONS USED IN THE FIELD MAPPINGS SCRIPT ####
def setDefaultValues(row):
        row.STATE_L = "UT"
        row.STATE_R = "UT"
        row.COUNTY_L = ""
        row.COUNTY_R = "" 
        row.STATUS = ""
        row.CARTOCODE = ""
        row.FULLNAME = ""
        row.FROMADDR_L = 0
        row.TOADDR_L = 0
        row.FROMADDR_R = 0
        row.TOADDR_R = 0
        row.PARITY_L = ""
        row.PARITY_R = ""
        row.PREDIR = ""
        row.NAME = ""
        row.POSTTYPE = ""
        row.POSTDIR = ""
        row.AN_NAME = ""
        row.AN_POSTDIR = ""
        row.A1_PREDIR = ""
        row.A1_NAME = ""
        row.A1_POSTTYPE = ""
        row.A1_POSTDIR = ""
        row.A2_PREDIR = ""
        row.A2_NAME = ""
        row.A2_POSTTYPE = ""
        row.A2_POSTDIR = ""
        row.QUADRANT_L = ""
        row.QUADRANT_R = ""
        row.ADDRSYS_L = ""
        row.ADDRSYS_R = ""
        row.POSTCOMM_L = ""
        row.POSTCOMM_R = ""
        row.ZIPCODE_L = ""
        row.ZIPCODE_R = ""
        row.INCMUNI_L = ""
        row.INCMUNI_R = ""
        row.UNINCCOM_L = ""
        row.UNINCCOM_R = ""
        row.NBRHDCOM_L = ""
        row.NBRHDCOM_R = ""
        row.ER_CAD_ZONES = ""
        row.ESN_L = ""
        row.ESN_R = ""
        row.MSAGCOMM_L = ""
        row.MSAGCOMM_R = ""
        row.ONEWAY = ""
        row.VERT_LEVEL = ""
        row.SPEED_LMT = None
        row.ACCESSCODE = ""
        row.DOT_HWYNAM = ""
        row.DOT_RTNAME = ""
        row.DOT_RTPART = ""
        row.DOT_F_MILE = None
        row.DOT_T_MILE = None
        row.DOT_FCLASS = ""
        row.DOT_SRFTYP = ""
        row.DOT_CLASS = ""
        row.DOT_OWN_L = ""
        row.DOT_OWN_R = ""
        row.DOT_AADT = None
        row.DOT_AADTYR = ""
        row.DOT_THRULANES = None
        row.BIKE_L = ""
        row.BIKE_R = ""
        row.BIKE_PLN_L = ""
        row.BIKE_PLN_R = ""
        row.BIKE_REGPR = ""
        row.BIKE_NOTES = ""
        row.UNIQUE_ID = ""
        row.LOCAL_UID = ""
        row.UTAHRD_UID = ""
        row.SOURCE = ""
        row.UPDATED = None
        row.EFFECTIVE = None
        row.EXPIRE = None
        row.CREATED = None
        row.CREATOR = ""
        row.EDITOR = ""
        row.CUSTOMTAGS = ""
        row.UTRANS_NOTES = ""


# remove the post type if the street name is numeric
def removePostTypeIfNumeric(row):
    if row.NAME[0].isdigit():
        return True

# remove the post dir if the street name is alpha
def removePostDirIfAlpha(row):
    if row.NAME[0].isalpha():
        return True


# create a dictionary of coded domain values and descripitons for fields with domains
def CreateDomainDictionary(domain_name):
    dictOfDomainsValuesDescriptions = {}
    domains = arcpy.da.ListDomains(NextGenFGDB)

    for domain in domains:
        if domain.name == domain_name:
            coded_values = domain.codedValues
            for val, desc in coded_values.items():

                # create a list for the dictionary of coded value and description
                listOfDomainDescriptions = []

                # check if domain val is same as description, if so only add one to list
                if val.upper() == desc.upper():
                    listOfDomainDescriptions.append(val.upper().strip())
                else:
                    listOfDomainDescriptions.append(val.upper().strip())
                    listOfDomainDescriptions.append(desc.upper().strip())

                # ADD CUSTOM VALUES TO DICTIONARY #
                # if domain is 'CVDomain_StreetType'
                if domain_name == 'CVDomain_StreetType':
                    # add custom values to certain coded domain vals - these would be common, known abbreviations the counties use
                    if val == "WAY":
                        listOfDomainDescriptions.append("WY")
                    if val == "PKWY":
                        listOfDomainDescriptions.append("PKY")

                # if domain is 'CVDomain_Status'
                if domain_name == 'CVDomain_Status':
                    # add custom values to certain coded domain vals - these would be common, known abbreviations the counties use
                    if val.upper() == "ACTIVE":
                        listOfDomainDescriptions.append("A")
                    if val.upper() == "PLANNED":
                        listOfDomainDescriptions.append("P")
                    if val.upper() == "RETIRED":
                        listOfDomainDescriptions.append("R")
                    if val.upper() == "CONSTRUCTION":
                        listOfDomainDescriptions.append("D") # wasatch uses D for "In Develeopment"
                    #if val.upper() == "RECONSTRUCTION":
                    #    listOfDomainDescriptions.append("")

                # if domain is 'CVDomain_SurfaceType'
                if domain_name == 'CVDomain_SurfaceType':
                    # add custom values to certain coded domain vals - these would be common, known abbreviations the counties use
                    # the nuberic values are from the older data model - which some counties are still using
                    if val.upper() == "U": # UNKNOWN
                        listOfDomainDescriptions.append("UNDEFINED")
                        listOfDomainDescriptions.append("999")
                    if val.upper() == "I": # IMPROVED
                        listOfDomainDescriptions.append("GRAVEL")
                        listOfDomainDescriptions.append("200")
                    if val.upper() == "P": # PAVED
                        listOfDomainDescriptions.append("100")
                    #if val.upper() == "P-ASP": # PAVED ASPHALT
                    #    listOfDomainDescriptions.append("")
                    #if val.upper() == "P-CON": # PAVED CONCRETE
                    #    listOfDomainDescriptions.append("")
                    if val.upper() == "D": # DIRT
                        listOfDomainDescriptions.append("300")
                    #if val.upper() == "N": # NATIVE
                    #    listOfDomainDescriptions.append("")

                # if domain is 'CVDomain_FunctionalClass'
                if domain_name == 'CVDomain_FunctionalClass':
                    # add custom values to certain coded domain vals - these would be common, known abbreviations the counties use
                    # the nuberic values are from the older data model - which some counties are still using (see Wasatch County data for many of these values, Domain = ST_Agfunc)
                    if val.upper() == "INTERSTATE":
                        listOfDomainDescriptions.append("11")
                    #if val.upper() == "OTHER FREEWAY":
                    #    listOfDomainDescriptions.append("")
                    if val.upper() == "PRINCIPAL ARTERIAL":
                        listOfDomainDescriptions.append("10")
                    #if val.upper() == "MINOR ARTERIAL":
                    #    listOfDomainDescriptions.append("")
                    if val.upper() == "MAJOR COLLECTOR":
                        listOfDomainDescriptions.append("21")
                    if val.upper() == "MINOR ARTERIAL":
                        listOfDomainDescriptions.append("22")
                    if val.upper() == "LOCAL":
                        listOfDomainDescriptions.append("30")
                        listOfDomainDescriptions.append("32")
                        listOfDomainDescriptions.append("33")


                ## if domain is 'CVDomain_AccessIssues'
                #if domain_name == 'CVDomain_AccessIssues':
                #    # add custom values to certain coded domain vals - these would be common, known abbreviations the counties use
                #    if val.upper() == "":
                #        listOfDomainDescriptions.append("")

                ## if domain is 'CVDomain_RoadClass'
                #if domain_name == 'CVDomain_RoadClass':
                #    # add custom values to certain coded domain vals - these would be common, known abbreviations the counties use
                #    if val.upper() == "":
                #        listOfDomainDescriptions.append("")

                ## if domain is 'CVDomain_OneWay'
                #if domain_name == 'CVDomain_OneWay':
                #    # add custom values to certain coded domain vals - these would be common, known abbreviations the counties use
                #    if val.upper() == "":
                #        listOfDomainDescriptions.append("")

                ## if domain is 'CVDomain_VerticalLevel'
                #if domain_name == 'CVDomain_VerticalLevel':
                #    # add custom values to certain coded domain vals - these would be common, known abbreviations the counties use
                #    if val.upper() == "":
                #        listOfDomainDescriptions.append("")

                # add value and descripiton to the dictionary 
                dictOfDomainsValuesDescriptions[val] = listOfDomainDescriptions

    return dictOfDomainsValuesDescriptions


# return the coded domain val (aka: the dict key) from the dictionary 
def GetCodedDomainValue(valueToCheck, dictionaryToCheck):
    if valueToCheck == None or valueToCheck is None or valueToCheck == " ":
        valueToCheck = ""
    else:
        if type(valueToCheck) is int:
            valueToCheck = str(valueToCheck)
        else:
            valueToCheck = valueToCheck.upper()
    for key, value in dictionaryToCheck.iteritems():
        if valueToCheck == "":
            return ""
        if valueToCheck == key:
            return key
        if type(value) is str:
            if valueToCheck == value:
                return key
        else:
            for v in value:
                if valueToCheck == v:
                    return key
    return ""


# add bad value to domain text file log
def AddBadValueToTextFile(county_number, field_name, field_value):
    # add the bad domain value to the text doc so we can inspect them
    text_file_path = "K:/AGRC Projects/UtransEditing/Scripts and Tools/_script_logs/CountiesDomainValueErrors.txt"
    if os.path.exists(text_file_path):
        file = open(text_file_path, "a")
        # DATE, COUNTY, FIELDNAME, VALUE
        file.write("\n" + str(date.today()) + "," + county_number + "," + field_name + "," + field_value)
        file.close()


# validate the county's AN_NAME value and parse if necessary 
def Validate_AN_NAME(an_Name):
    # call this function this way to get both values
    # an_Name, an_PostDir = Validate_AN_NAME(value)
    
    returnAN_NAME = ""
    returnAN_POSTDIR = ""
    
    if an_Name.isdigit():
        # row.AN_NAME = an_Name
        returnAN_NAME = an_Name
    else:
        # check if any of the values are numeric (maybe they added the postdir in the field)
        if any(char.isdigit() for char in an_Name):
            # parse the streetname
            an_Name_split = an_Name.split(" ")
            # see if there's more than one word
            if len(an_Name_split) > 1:
                # check if first word is numeric
                if an_Name_split[0].isdigit():
                    # this is a valid AN_NAME
                    returnAN_NAME = an_Name_split[0]
                    # check if second word is a valid AN_POSTDIR
                    an_POSTDIR = an_Name_split[1].upper()
                    if an_POSTDIR in ("N","S","E","W"):
                        returnAN_POSTDIR = an_POSTDIR
    return returnAN_NAME, returnAN_POSTDIR

# ParseFullAddress is an internal function that is typically called ParseAndAssign_FullAddres function
# parse out full address - ie: "N 1300 S" or "1300 S" or "W Broadway RD" or "Broadway RD"
# if it doesn't parse out based on one of these formats just retrun the original value
# it is assumed that full_address parameter has a value and is not None or "" or .isspace()
def ParseFullAddress(full_address):
    from UtransETL_FieldMappingFunctions import dictOfValidPostTypes
    # call this function this way to get all values:
    # is_valid_parse, pre_dir, street_name, post_type, post_dir = ParseFullAddress(full_address)

    full_address = full_address.strip()
    _full_address = full_address
    _is_valid_parsed = False
    _predir = ""
    _predirFullSpelling = ""
    _streetname = ""
    _posttype = ""
    _postdir = ""
    _postdirFullSpelling = ""
    _checkForStreetName = ""
    __has_predir = False
    __has_postype = False
    __has_postdir = False

    # parse string into array
    full_address_split = full_address.split(" ")
    word_count = len(full_address_split)

    if word_count > 1:
        # check first word and see if predirection
        first_word = full_address_split[0]
        first_word = first_word.strip()
        if first_word in ("N", "S", "E", "W"):
            _predir = first_word
            __has_predir = True
        elif first_word in ("NORTH", "SOUTH", "EAST", "WEST"):
            _predirFullSpelling = first_word
            __has_predir = True


        # check last word and see if it's a valid posttype (only check if for posttype if last word is four characters long so we don't trim off valid streetname such as Canyon, Creek, Park, etc.)
        last_word = full_address_split[-1]
        last_word = last_word.strip()
        if last_word in officialPostTypeDomains:
            # test if posttype
            _posttype = GetCodedDomainValue(full_address_split[-1], dictOfValidPostTypes)
            if _posttype != "":
                __has_postype = True
        elif last_word in ("N", "S", "E", "W", "NORTH", "SOUTH", "EAST", "WEST"):
            # test if postdir
            if last_word in ("N", "S", "E", "W"):
                _postdir = last_word
                __has_postdir = True
            elif last_word in ("NORTH", "SOUTH", "EAST", "WEST"):
                _postdirFullSpelling = last_word
                __has_postdir = True
                        
        # get street name value from full_address variable, if present
        if __has_postdir == True or __has_postype == True:
             # remove the last word from full_address
             _full_address = _full_address.rsplit(' ', 1)[0]
        if __has_predir == True:
            # remove the first word from full_address  
            # but first, check if there's anything left to split on (i was getting errors when the orig value was "E ST".. then after the last word was removed about it was "E")
            if ' ' in _full_address:
                _full_address = _full_address.split(' ', 1)[1]
            else:
                # there's not enough words in the array to parse correctly, just return the original value
                _full_address = ""

        _full_address = _full_address.strip()

        if _full_address != "":
            _checkForStreetName = str(_full_address)

        # check if it's a numeric streetname
        if _checkForStreetName.isdigit():
            # see if predir is full spelling, if so only use first character
            _streetname = _checkForStreetName
            if _predirFullSpelling != "":
                _predir = _predirFullSpelling[:1]
            if _postdirFullSpelling != "":
                _postdir = _postdirFullSpelling[:1]
        else:
            _streetname = _checkForStreetName                    

        # set name and confirm it's parsed
        if __has_postdir == True or __has_postype == True or __has_predir == True:
            # check if there's a street name now that the predir, or posttype, or postdir has been removed
            if _streetname != "":
                #_streetname = _full_address
                _is_valid_parsed = True
            else:
                _is_valid_parsed = False
        else:
            _is_valid_parsed = False

    else:
        # just one word string so return empty parsed values
        return _is_valid_parsed, _predir, _streetname, _posttype, _postdir

    # return tuple
    return _is_valid_parsed, _predir, _streetname, _posttype, _postdir


# parse and assign values for an address that might be concatinated
def ParseAndAssign_FullAddress(row, county_field_value, field_name_to_parse, bool_primary=False, bool_alias1=False, bool_alias2=False):
    """ example: (row, row.ALIAS1, "ALIAS1", False, True, False) """
    # check if we need to parse the field (they have predir, postdir, and posttypes in the field)
    #if row.getValue(field_name_to_parse) is not None or row.getValue(field_name_to_parse) != "":
    if HasFieldValue(county_field_value):
        _original_field_value = row.getValue(field_name_to_parse)
        is_valid_parse, pre_dir, street_name, post_type, post_dir = ParseFullAddress(row.getValue(field_name_to_parse))

        if is_valid_parse == True:
            # it WAS a valid parse
            if bool_primary:
                # we're parsing primary fields
                row.setValue("PREDIR", pre_dir)
                row.setValue("NAME", street_name)
                row.setValue("POSTTYPE", post_type)
                row.setValue("POSTDIR", post_dir)
            else:
                # we're parsing alias fields, so incorporate a check for numeric values
                if street_name.isdigit():
                    # the street name is numeric
                    # check if there are existing values in the alias numeric field
                    if row.AN_NAME == "" or row.AN_NAME is None or row.AN_NAME.isspace():
                        # there are no existing values in the alias numeric field
                        row.AN_NAME = street_name
                        row.AN_POSTDIR = post_dir
                    else:
                        # there are existing values in the alias numeric fields so put the values in the alpha numeric field
                        if bool_alias1:
                            row.setValue("A1_NAME", _original_field_value)
                        if bool_alias2:
                            row.setValue("A2_NAME", _original_field_value)
                else:
                    # the streetname is alpha
                    if bool_alias1:
                        row.setValue("A1_PREDIR", pre_dir)
                        row.setValue("A1_NAME", street_name)
                        row.setValue("A1_POSTTYPE", post_type)
                        row.setValue("A1_POSTDIR", post_dir)
                    if bool_alias2:
                        row.setValue("A2_PREDIR", pre_dir)
                        row.setValue("A2_NAME", street_name)
                        row.setValue("A2_POSTTYPE", post_type)
                        row.setValue("A2_POSTDIR", post_dir)
        else:
            # it was NOT a valid parse, so use the original text for the field value
            if bool_primary:
                row.setValue("NAME", _original_field_value)
            if bool_alias1:
                row.setValue("A1_NAME", _original_field_value)
            if bool_alias2:
                row.setValue("A2_NAME", _original_field_value)


# validate and assing field values using the field name and dictionary of valid field values
def ValidateAndAssign_FieldValue(row, utrans_field_name, county_field_value, county_number, dict_of_valid_values):
    """ example: (row, "POSTTYPE", row.STREETTYPE, countyNumber, dictOfValidPostTypes) """
    # get county field name
    #_test = locals()
    #arcpy.AddMessage(_test)
    #_county_field_name = _test.split(".")
    #arcpy.AddMessage(_county_field_name)

    if HasFieldValue(county_field_value):
        #if county_field_value == "" or county_field_value is None:
            # do something
            #county_field_value = ""
        #else:
            # convert the raw county field value to stirng, in case it was an int value (the valid dictionary values are all string)

        _county_field_value =str(county_field_value)

        # check for valid value in dictionary
        _validated_field_value = GetCodedDomainValue(_county_field_value.strip(), dict_of_valid_values)

        if _validated_field_value != "":
            # has valid value
            row.setValue(utrans_field_name, _validated_field_value)
        elif _validated_field_value == "" and len(_county_field_value) > 0:
            # does not have valid value
            # add the dot_fclass they gave to the notes field so we can evaluate it
            row.setValue("UTRANS_NOTES", row.getValue("UTRANS_NOTES") + utrans_field_name + ": " + _county_field_value + "; ")
            # add the bad domain value to the text file log
            AddBadValueToTextFile(county_number, utrans_field_name, _county_field_value)


def HasFieldValue(field_value):
    """ example: (row.STATUS) """
    if field_value is None:
        # the value is of NoneType
        return False
    else:
        _str_field_value = str(field_value)

        # value is not of NoneType
        if _str_field_value.isdigit():
            # it's an int
            if _str_field_value == "":
                return False
            else:
                return True
        else:
            # it's not an int
            if _str_field_value == "" or _str_field_value is None or _str_field_value.isspace():       
                return False
            else:
                return True

def HasValidDirection(field_value):
    """ example: (row.STATUS) """
    if HasFieldValue(field_value):
        if field_value in ("N", "S", "E", "W", "NORTH", "SOUTH", "EAST", "WEST"):
            return True
        else:
            return False

def VertLevel_TranslateOldDomainToNewDomain(row, old_vert_domain_value, county_number):
    """ example: (row, row.VERTLEVEL, countyNumber) """
    # NEW DOMAIN VALUES 
    # 0: Ground/Lowest
    # 1: Overpassing Level 1
    # 2: Overpassing Level 2
    # 3: Overpassing Level 3

    # OLD DOMAIN VALUES
    # 1: Road feature does not cross over another road feature
    # 2: Road feature crosses over another road feature
    # 3: Road feature crosses over and/or under two or more road features

    _old_domain_val = str(old_vert_domain_value)
    _old_domain_val = _old_domain_val.strip()

    if HasFieldValue(_old_domain_val):
        if _old_domain_val == "1":
            row.VERT_LEVEL = "0"
        elif _old_domain_val == "2":
            row.VERT_LEVEL = "1"
        elif _old_domain_val == "3":
            row.VERT_LEVEL = "2"
        else:
            # does not have valid value
            # add the vertical level they gave to the notes field so we can evaluate it
            row.setValue("UTRANS_NOTES", row.getValue("UTRANS_NOTES") + "VERT_LEVEL" + ": " + _old_domain_val + "; ")
            # add the bad domain value to the text file log
            AddBadValueToTextFile(county_number, "VERT_LEVEL", _old_domain_val)     


# get a list of coded domain values for posttype field for the full name parser function (used when parsing the full address)
def GetOfficalPOSTTYPE_domainValues():
    listOfDomainValues = []
    domains = arcpy.da.ListDomains(NextGenFGDB)

    for domain in domains:
        if domain.name == 'CVDomain_StreetType':
            coded_values = domain.codedValues
            for val, desc in coded_values.items():
                #print(val)
                listOfDomainValues.append(val)
    return listOfDomainValues
# call the function and create the list
officialPostTypeDomains = GetOfficalPOSTTYPE_domainValues()