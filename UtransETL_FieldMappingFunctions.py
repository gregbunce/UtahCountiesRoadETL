import arcpy

def Washington(rows):
    for row in rows:
        # set all fields to empty or zero or none
        setDefaultValues(row)

        # set county specific fields
        row.COUNTY_L = "49053"
        row.COUNTY_R = "49053"
        row.FROMADDR_L = row.L_F_ADD
        row.TOADDR_L = row.L_T_ADD
        row.FROMADDR_R = row.R_F_ADD
        row.TOADDR_R = row.R_T_ADD
        row.PREDIR = row.PRE_DIR[:1]
        row.NAME = row.S_NAME.upper()
        row.POSTTYPE = row.S_TYPE
        row.POSTDIR = row.SUF_DIR
        row.AN_NAME = row.ACS_NAME
        row.AN_POSTDIR = row.ACS_SUF
        row.A1_NAME = row.ALIAS1
        row.A1_POSTTYPE = row.A1_POSTTYPE
        row.A2_NAME = row.ALIAS2
        row.A2_POSTTYPE = row.ALIAS2_TYP
        row.ONEWAY = row.ONE_WAY
        row.SPEED_LMT = row.SPD_LMT
        row.DOT_SRFTYP = row.S_SURF
        row.SOURCE = row.SOURCE
        
        # store the row
        rows.updateRow(row)  
        del row


def Utah(rows):
    for row in rows:
        # variables
        POSTDIR_FROM_ROADNAME = None
        POSTDIR_FROM_ALTROADNAME = None
        ACS_FROM_ALTROADNAME = None
        POSTDIR_FROM_ALTROADNAME2 = None
        ACS_FROM_ALTROADNAME2 = None
        str_roadname_split = None

        # set all fields to empty or zero or none
        setDefaultValues(row)

        # set county specific fields
        row.COUNTY_L = "49049"
        row.COUNTY_R = "49049"
        row.FROMADDR_L = row.FROMLEFT
        row.TOADDR_L = row.TOLEFT
        row.FROMADDR_R = row.FROMRIGHT
        row.TOADDR_R = row.TORIGHT
        row.PREDIR = row.ROADPREDIR.upper()

        # check their roadname field
        if row.ROADNAME != None or row.ROADNAME != " ":
            # if it begins with a digit, then check if it ends with a North, South, East, or West - if so export that to the sufdir field
            str_roadname = row.ROADNAME.strip()

            if str_roadname != None or str_roadname != " ":
                if len(str_roadname) > 0:
                    if str_roadname[0].isdigit():
                        # parse out the string to check if sufdir exists
                        str_roadname_split = str_roadname.split(" ")

                        #get the last work in the array
                        if str_roadname_split[-1] == "NORTH" or str_roadname_split[-1] == "SOUTH" or str_roadname_split[-1] == "EAST" or str_roadname_split[-1] == "WEST":
                            POSTDIR_FROM_ROADNAME = str(str_roadname_split[-1]).strip()

                            # check if first work in split is number
                            if str_roadname_split[0].isdigit():
                                row.NAME = str_roadname_split[0].strip()
                            else:
                                row.NAME = row.ROADNAME[:30].upper()
                        else:
                            row.NAME = row.ROADNAME[:30].upper()
                    else:
                        # it's not a digit, it's alpha roadname
                        row.NAME = row.ROADNAME[:30].upper()

        # check streettype
        if row.ROADTYPE != None:
            row.POSTTYPE = row.ROADTYPE.upper()

            # check if it's an acs road to see if we can ommit the streettype value that they often add
            if str_roadname_split != None:
                # use the first character to pass into the sufdir
                if str_roadname_split[0].isdigit():
                    row.POSTTYPE = ""

        # check if the sufdir was extracted from the roadname
        if row.ROADPOSTDIR != None or POSTDIR_FROM_ROADNAME != None:
            if POSTDIR_FROM_ROADNAME != None:
                # use the first character to pass into the sufdir
                row.POSTDIR = POSTDIR_FROM_ROADNAME[0]
            else:
                row.POSTDIR = row.ROADPOSTDIR.upper()

        # check the altroadname field values and see if they placed an acs value in there, if so move it to the acs fields
        if row.ALTROADNAME != None or row.ALTROADNAME != " ":
            # if it begins with a digit, then check if it ends with a North, South, East, or West - if so export that to the sufdir field
            str_altroadname1 = row.ALTROADNAME.strip()

            if str_altroadname1 != None or str_altroadname1 != " ":
                if len(str_altroadname1) > 0:
                    if str_altroadname1[0].isdigit():
                        # parse out the string to check if sufdir exists
                        str_altroadname1_split = str_altroadname1.split(" ")

                        # get the last work in the array
                        if str_altroadname1_split[-1] == "NORTH" or str_altroadname1_split[-1] == "SOUTH" or str_altroadname1_split[-1] == "EAST" or str_altroadname1_split[-1] == "WEST":
                            POSTDIR_FROM_ALTROADNAME = str(str_altroadname1_split[-1]).strip()

                            # check if first work in split is number
                            if str_altroadname1_split[0].isdigit():
                                ACS_FROM_ALTROADNAME = str_altroadname1_split[0].strip()
                                row.A1_NAME= ""
                            else:
                                row.A1_NAME = row.ALTROADNAME.upper()
                        else:
                            row.A1_NAME = row.ALTROADNAME.upper()
                    else:
                        # it's not a digit, it's alpha roadname
                        row.A1_NAME = row.ALTROADNAME.upper()

        if row.ALTROADTYPE != None:
            row.A1_POSTTYPE = row.ALTROADTYPE.upper()

        # check the altroadname2 field values and see if they placed an acs value in there, if so move it to the acs fields
        if row.ALTROADNAME2 != None or row.ALTROADNAME2 != " " or row.ALTROADNAME2 != "" or row.ALTROADNAME2 is not None:
            #row.A2_NAME = row.ALTROADNAME2.upper()
            # if it begins with a digit, then check if it ends with a North, South, East, or West - if so export that to the sufdir field
            str_altroadname2 = row.ALTROADNAME2.strip()

            if str_altroadname2 != None or str_altroadname2 != " " or str_altroadname2 != "":
                if len(str_altroadname2) > 0:
                    if str_altroadname2[0].isdigit():
                        # parse out the string to check if sufdir exists
                        str_altroadname2_split = str_altroadname2.split(" ")

                        # get the last work in the array
                        if str_altroadname2_split[-1] == "NORTH" or str_altroadname2_split[-1] == "SOUTH" or str_altroadname2_split[-1] == "EAST" or str_altroadname2_split[-1] == "WEST":
                            POSTDIR_FROM_ALTROADNAME2 = str(str_altroadname2_split[-1]).strip()

                            # check if first work in split is number
                            if str_altroadname2_split[0].isdigit():
                                ACS_FROM_ALTROADNAME2 = str_altroadname2_split[0].strip()
                                row.A2_NAME= ""
                            else:
                                row.A2_NAME = row.ALTROADNAME2.upper()
                        else:
                            row.A2_NAME = row.ALTROADNAME2.upper()
                    else:
                        # it's not a digit, it's alpha roadname
                        row.A2_NAME = row.ALTROADNAME2.upper()

        if row.ALTROADTYPE2 != None:
            row.A1_POSTTYPE = row.ALTROADTYPE2
        if ACS_FROM_ALTROADNAME2 != None:
            row.AN_NAME = ACS_FROM_ALTROADNAME2
            # remove the value in the alias1type field
            row.A1_POSTTYPE = ""
        if POSTDIR_FROM_ALTROADNAME2 != None:
            row.AN_POSTDIR = POSTDIR_FROM_ALTROADNAME2[0]
            # remove the value in the alias1type field
            row.A1_POSTTYPE = ""
        if ACS_FROM_ALTROADNAME != None:
            row.AN_NAME = ACS_FROM_ALTROADNAME
            # remove the value in the alias1type field
            row.A1_POSTTYPE = ""
        if POSTDIR_FROM_ALTROADNAME != None:
            row.AN_POSTDIR = POSTDIR_FROM_ALTROADNAME[0]
            # remove the value in the alias1type field
            row.A1_POSTTYPE = ""

        # store the row
        rows.updateRow(row)  
        del row


def Davis(rows):
    # get post direction domains
    listOfStreetTypes = GetRoadTypeDomains()

    for row in rows:
        # set all fields to empty or zero or none
        setDefaultValues(row)

        # set county specific fields
        row.COUNTY_L = "49011"
        row.COUNTY_R = "49011"
        row.FROMADDR_L = row.LeftFrom
        row.TOADDR_L = row.LeftTo
        row.FROMADDR_R = row.RightFrom
        row.TOADDR_R = row.RightTo
        if row.PrefixDire != None:
            row.PREDIR = row.PrefixDire[:1]
        if row.RoadName != None:
            row.NAME = row.RoadName[:40]
        if row.RoadNameTy != None:
            row.POSTTYPE = row.RoadNameTy
        row.POSTDIR = row.PostDirect
        row.DOT_SRFTYP = row.RoadSurfac

        # check if alias names exist (maybe make this a global function that we can reuse for other counties who do a similar alias name concatination field)
        if row.RoadAliasN != None:
            # get alias name as string
            davisAliasName = row.RoadAliasN

            # check if there's a least one word in the string
            if len(davisAliasName) > 0:
                # parse out the string into array, so we can check for sufdir or street type
                davisAliasName_split = davisAliasName.split(" ")

                # check if first word is number
                if davisAliasName[0].isdigit():
                    # get the last word in the array
                    if davisAliasName_split[-1] == "N" or davisAliasName_split[-1] == "S" or davisAliasName_split[-1] == "E" or davisAliasName_split[-1] == "W":
                        POSTDIR_FROM_ROADNAME = str(davisAliasName_split[-1]).strip()

                        # check if first word in array is number
                        if davisAliasName_split[0].isdigit():
                            row.AN_NAME = davisAliasName_split[0].strip()
                            row.AN_POSTDIR = davisAliasName_split[1].strip()
                        else:
                            row.A1_NAME = davisAliasName[:30]
                    else:
                        row.A1_NAME = davisAliasName[:30]
                # the first word was not a number, and is therefore an alpha
                else:
                    # check if last word is alpha, before we upper it and check if valid street type
                    if davisAliasName_split[-1].isalpha():
                        # check if last word in string is a valid street type
                        if davisAliasName_split[-1].upper() in listOfStreetTypes:
                            # add the street type to the street type field
                            row.A1_POSTTYPE = davisAliasName_split[-1]

                            # remove the street type from the string
                            alphaStreetName = davisAliasName.rsplit(' ', 1)[0]
                            row.A1_NAME = alphaStreetName
                        # check if street type is WY - Davis county uses that abbreviation for WAY
                        elif (davisAliasName_split[-1].upper() == "WY"):
                            row.A1_POSTTYPE = "WAY"

                            # remove the street type from the string
                            alphaStreetName = davisAliasName.rsplit(' ', 1)[0]
                            row.A1_NAME = alphaStreetName
                        else:
                            row.A1_NAME = davisAliasName[:30]
                    else:
                        row.A1_NAME = davisAliasName[:30]
        # store the row
        rows.updateRow(row)
        del row


def Weber(rows):
    # get post direction domains
    dictOfValidPostTypes = CreatePostTypeDictionary()

    for row in rows:
        # set all fields to empty or zero or none
        setDefaultValues(row)

        # set county specific fields
        row.COUNTY_L = "49057"
        row.COUNTY_R = "49057"        
        row.FROMADDR_L = row.LEFTFROM
        row.TOADDR_L = row.LEFTTO
        row.FROMADDR_R = row.RIGHTFROM
        row.TOADDR_R = row.RIGHTTO
        row.PREDIR = row.PREDIR[:1]
        row.NAME = row.S_NAME[:30]

        # check if valid post type
        postTypeDomain = GetCodedDomainValue(row.STREETTYPE, dictOfValidPostTypes)
        if postTypeDomain != "":
            row.POSTTYPE = postTypeDomain
        else: # add the post type they gave to the notes field so we can evaluate it
            if len(validPostType) > 0:
                row.UTRANS_NOTES = "POSTTYPE: " + postTypeDomain + "; "

        row.POSTDIR = row.SUFDIR
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
        row.SPEED_LMT = row.SPEEDLIMIT
        row.LOCAL_UID = row.S_UNIQUE

        # weed out the alias name from their "ALIAS" and "ACS_ALIAS" fields
        # check if ALIAS == S_NAME (Weber has tons of alias names that match the steret name)
        if row.ALIAS != ' ' or row.ALIAS != None or row.ALIAS is not None:
            if row.ALIAS.strip() != row.S_NAME.strip(): 
                # check if alias or numeric
                if row.ALIAS.isdigit():
                    # use the ACS_ALIAS field becuase it has the sufdir baked in
                    acsAlias = row.ACS_ALIAS.strip()
                    if len(acsAlias) > 0:
                        acsAlias_split = acsAlias.split(" ")
                        # check if last word in array is post dir
                        if acsAlias_split[-1] == "N" or acsAlias_split[-1] == "S" or acsAlias_split[-1] == "E" or acsAlias_split[-1] == "W":
                            row.AN_POSTDIR = acsAlias_split[-1].strip()
                            # remove the post dir from the string
                            an_name = acsAlias.rsplit(' ', 1)[0]
                            row.AN_NAME = an_name
                        else:
                            # use the suf dir field to get the post type
                            row.AN_NAME = row.ALIAS
                            row.AN_POSTDIR = row.SUFDIR
                else: # alias is alpha
                # get alias name as string
                    aliasName = row.ALIAS
                    # check if there's a least one word in the string
                    if len(aliasName) > 0:
                        # parse out the string into array, so we can check for sufdir or street type
                        aliasName_split = aliasName.split(" ")                
                        # check if the last word in array is an official street type from our domain
                        if aliasName_split[-1].isalpha():
                            # check if last word in string is a valid street type
                            postTypeDomain = GetCodedDomainValue(aliasName_split[-1].upper(), dictOfValidPostTypes)
                            if postTypeDomain != "":
                                # add the street type to the street type field
                                row.A1_POSTTYPE = postTypeDomain
                                # remove the street type from the string
                                alphaStreetName = aliasName.rsplit(' ', 1)[0]
                                row.A1_NAME = alphaStreetName
                            else:
                                row.A1_NAME = row.ALIAS

        # remove PostDir if street name is alpha
        if removePostDirIfAlpha(row) == True:
            row.POSTDIR = ""
        
        # remove PostType is street name is numeric
        if removePostTypeIfNumeric(row) == True:
            row.POSTTYPE = ""

        # store the row
        rows.updateRow(row)
        del row


def SaltLake(rows):
    for row in rows:
        # set county specific fields
        row.STATE_L = "UT"
        row.STATE_R = "UT"
        row.COUNTY_L = "49035"
        row.COUNTY_R = "49035"

        # clear the A1_NAME AND A1_POSTYPE fields if the same data is in AN_NAME
        if (row.A1_NAME != ' ' or row.A1_NAME != None or row.A1_NAME is not None) and (row.AN_NAME != ' ' or row.AN_NAME != None or row.AN_NAME is not None):
            a1_name = str(row.A1_NAME) # the numeric street name and post type, and sometimes post dir
            an_name = str(row.AN_NAME) # just the numeric street name
            # check if street name is contained in the A1_NAME field
            arcpy.AddMessage(a1_name + " " + an_name)
            if a1_name != '' and an_name != '':
                if str(an_name) in str(a1_name):
                    # clear out the A1_NAME fields
                    row.A1_PREDIR = ""
                    row.A1_NAME = ""
                    row.A1_POSTTYPE = ""
                    row.A1_POSTDIR = ""
  
         # clear the A2_NAME AND A2_POSTYPE fields if the same data is in AN_NAME
        if (row.A2_NAME != ' ' or row.A2_NAME != None or row.A2_NAME is not None) and (row.AN_NAME != ' ' or row.AN_NAME != None or row.AN_NAME is not None):
            a2_name = str(row.A2_NAME) # the numeric street name and post type, and sometimes post dir
            an_name = str(row.AN_NAME) # just the numeric street name
            # check if street name is contained in the A2_NAME field
            arcpy.AddMessage(a2_name + " " + an_name)
            if a2_name != '' and an_name != '':
                if an_name in a2_name:
                    # clear out the A1_NAME fields
                    row.A2_PREDIR = ""
                    row.A2_NAME = ""
                    row.A2_POSTTYPE = ""
                    row.A2_POSTDIR = ""                             

        # store the row
        rows.updateRow(row)
        del row


def Beaver(rows):
    for row in rows:
        # set all fields to empty or zero or none
        setDefaultValues(row)

        # set county specific fields
        row.COUNTY_L = "49001"
        row.COUNTY_R = "49001"        
        row.FROMADDR_L = row.L_F_ADD
        row.TOADDR_L = row.L_T_ADD
        row.FROMADDR_R = row.R_F_ADD
        row.TOADDR_R = row.R_T_ADD
        row.PREDIR = row.PREDIR[:1]
        row.NAME = row.STREETNAME[:30]
        row.POSTTYPE = row.STREETTYPE
        row.POSTDIR = row.SUFDIR
        row.AN_NAME = row.ACSNAME
        row.AN_POSTDIR = row.ACSSUF
        row.A1_PREDIR = ""
        row.A1_NAME = row.ALIAS1
        row.A1_POSTTYPE = row.ALIAS1TYP
        row.A1_POSTDIR = ""
        row.A2_PREDIR = ""
        row.A2_NAME = row.ALIAS2
        row.A2_POSTTYPE = row.ALIAS2TYP
        row.A2_POSTDIR = ""
        row.DOT_SRFTYP = row.SURFTYPE
        row.DOT_FCLASS = row.CLASS
        row.VERT_LEVEL = row.VERTLEVEL
        row.SPEED_LMT = row.SPEED
        row.LOCAL_UID = row.CO_UNIQUE

        # store the row
        rows.updateRow(row)
        del row


def BoxElder(rows):
    for row in rows:
        # set all fields to empty or zero or none
        setDefaultValues(row)

        # set county specific fields
        row.COUNTY_L = "49001"
        row.COUNTY_R = "49001"    
        
        #### fix these field names, i copied them from beaver function.....    
        ##row.FROMADDR_L = row.L_F_ADD
        ##row.TOADDR_L = row.L_T_ADD
        ##row.FROMADDR_R = row.R_F_ADD
        ##row.TOADDR_R = row.R_T_ADD
        ##row.PREDIR = row.PREDIR[:1]
        ##row.NAME = row.STREETNAME[:30]
        ##row.POSTTYPE = row.STREETTYPE
        ##row.POSTDIR = row.SUFDIR
        ##row.AN_NAME = row.ACSNAME
        ##row.AN_POSTDIR = row.ACSSUF
        ##row.A1_PREDIR = ""
        ##row.A1_NAME = row.ALIAS1
        ##row.A1_POSTTYPE = row.ALIAS1TYP
        ##row.A1_POSTDIR = ""
        ##row.A2_PREDIR = ""
        ##row.A2_NAME = row.ALIAS2
        ##row.A2_POSTTYPE = row.ALIAS2TYP
        ##row.A2_POSTDIR = ""
        ##row.DOT_SRFTYP = row.SURFTYPE
        ##row.DOT_FCLASS = row.CLASS
        ##row.VERT_LEVEL = row.VERTLEVEL
        ##row.SPEED_LMT = row.SPEED
        ##row.LOCAL_UID = row.CO_UNIQUE

        # store the row
        rows.updateRow(row)
        del row



###########################################
#### GENERAL FUNCTIONS BELOW THIS LINE ####

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


### get a list of road type domain names and descriptions
##def GetRoadTypeDomains ():
##    listOfDomains = []
##    domains = arcpy.da.ListDomains("K:/AGRC Projects/UtransEditing/Data/UtahRoadsNGSchema.gdb")

##    for domain in domains:
##        if domain.name == 'CVDomain_StreetType':
##            coded_values = domain.codedValues
##            for val, desc in coded_values.items():
##                listOfDomains.append(val.upper())
##                listOfDomains.append(desc.upper())
##    return listOfDomains



# create a dictionary of coded domain values and descripitons
def CreatePostTypeDictionary():
    dictOfPostTypeDomainsDescriptions = {}
    domains = arcpy.da.ListDomains("K:/AGRC Projects/UtransEditing/Data/UtahRoadsNGSchema.gdb")

    for domain in domains:
        if domain.name == 'CVDomain_StreetType':
            coded_values = domain.codedValues
            for val, desc in coded_values.items():

                # create a list for the dictionary of coded value and description
                listOfDomainDescriptions = []

                # check if domain val is same as description, if so only add one to list
                if val.upper() == desc.upper():
                    listOfDomainDescriptions.append(val.upper())
                else:
                    listOfDomainDescriptions.append(val.upper())
                    listOfDomainDescriptions.append(desc.upper())

                # add custom values to certain coded domain vals - these would be common, known abbreviations the counties use
                if val == "WAY":
                    listOfDomainDescriptions.append("WY")
                if val == "PKWY":
                    listOfDomainDescriptions.append("PKY")

                # add value and descripiton to the dictionary 
                dictOfPostTypeDomainsDescriptions[val.upper()] = listOfDomainDescriptions

    return dictOfPostTypeDomainsDescriptions


# return the coded domain val (aka: the dict key) from the dictionary 
def GetCodedDomainValue(valueToCheck, dictionaryToCheck):
    if valueToCheck == None:
        valueToCheck = ""
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



### _________________________________________________
### use this template for utrans field mapping etl
#row.STATE_L = "UT"
#row.STATE_R = "UT"
#row.COUNTY_L = "490**"
#row.COUNTY_R = "490**"
#row.STATUS = ""
#row.CARTOCODE = ""
#row.FULLNAME = ""
#row.FROMADDR_L = 0
#row.TOADDR_L = 0
#row.FROMADDR_R = 0
#row.TOADDR_R = 0
#row.PARITY_L = ""
#row.PARITY_R = ""
#row.PREDIR = ""
#row.NAME = ""
#row.POSTTYPE = ""
#row.POSTDIR = ""
#row.AN_NAME = ""
#row.AN_POSTDIR = ""
#row.A1_PREDIR = ""
#row.A1_NAME = ""
#row.A1_POSTTYPE = ""
#row.A1_POSTDIR = ""
#row.A2_PREDIR = ""
#row.A2_NAME = ""
#row.A2_POSTTYPE = ""
#row.A2_POSTDIR = ""
#row.QUADRANT_L = ""
#row.QUADRANT_R = ""
#row.ADDRSYS_L = ""
#row.ADDRSYS_R = ""
#row.POSTCOMM_L = ""
#row.POSTCOMM_R = ""
#row.ZIPCODE_L = ""
#row.ZIPCODE_R = ""
#row.INCMUNI_L = ""
#row.INCMUNI_R = ""
#row.UNINCCOM_L = ""
#row.UNINCCOM_R = ""
#row.NBRHDCOM_L = ""
#row.NBRHDCOM_R = ""
#row.ER_CAD_ZONES = ""
#row.ESN_L = ""
#row.ESN_R = ""
#row.MSAGCOMM_L = ""
#row.MSAGCOMM_R = ""
#row.ONEWAY = ""
#row.VERT_LEVEL = ""
#row.SPEED_LMT = None
#row.ACCESSCODE = ""
#row.DOT_HWYNAM = ""
#row.DOT_RTNAME = ""
#row.DOT_RTPART = ""
#row.DOT_F_MILE = None
#row.DOT_T_MILE = None
#row.DOT_FCLASS = ""
#row.DOT_SRFTYP = ""
#row.DOT_CLASS = ""
#row.DOT_OWN_L = ""
#row.DOT_OWN_R = ""
#row.DOT_AADT = None
#row.DOT_AADTYR = ""
#row.DOT_THRULANES = None
#row.BIKE_L = ""
#row.BIKE_R = ""
#row.BIKE_PLN_L = ""
#row.BIKE_PLN_R = ""
#row.BIKE_REGPR = ""
#row.BIKE_NOTES = ""
#row.UNIQUE_ID = ""
#row.LOCAL_UID = ""
#row.UTAHRD_UID = ""
#row.SOURCE = ""
#row.UPDATED = None
#row.EFFECTIVE = None
#row.EXPIRE = None
#row.CREATED = None
#row.CREATOR = ""
#row.EDITOR = ""
#row.CUSTOMTAGS = ""
#row.UTRANS_NOTES = ""