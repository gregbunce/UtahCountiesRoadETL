import arcpy
from datetime import date
import os.path
from UtransETL_GlobalFunctions import ValidateAndAssign_FieldValue, setDefaultValues, removePostTypeIfNumeric, removePostDirIfAlpha, CreateDomainDictionary, GetCodedDomainValue, AddBadValueToTextFile, Validate_AN_NAME, ParseFullAddress, ParseAndAssign_FullAddress, FieldHasValue, HasValidDirection

## global scope variables -- see bottom of file for those dependent on fucntion data, aka: variable is assigned after the functions have been instantiated
#NextGenFGDB = "K:/AGRC Projects/UtransEditing/Data/UtahRoadsNGSchema.gdb"

def Washington(rows):
    for row in rows:
        # set all fields to empty or zero or none
        setDefaultValues(row)
        
        countyNumber = "49053"
        
        # set county specific fields
        row.STATE_L = "UT"
        row.STATE_R = "UT"
        row.COUNTY_L = countyNumber
        row.COUNTY_R = countyNumber


        # set fields that we don't have the same name for
        # Washington County uses both the POSTDIR AND SUFFIXDIR fields > POSTDIR for alpha roads names and SUFFIXDIR for numeric road names
        row.UPDATED = row.LAST_UPDATE
        row.CREATED = row.CREATED_DATE
        # row.EDITOR = row.LAST_EDITOR

        if row.POSTDIR_ in ("N", "NORTH", "S", "SOUTH", "E", "EAST", "W", "WEST"):
            row.POSTDIR = row.POSTDIR_[:1]        
        if row.SUFFIXDIR in ("N", "NORTH", "S", "SOUTH", "E", "EAST", "W", "WEST"):
            row.POSTDIR = row.SUFFIXDIR[:1]

        ## TRANSFER OVER SIMPLE VALUES THAT DON'T NEED VALIDATION ##
        # transfer values from same name fields that were renamed with an underscore (this allows us to enforce our domains via the validation code here) 
        row.CARTOCODE = row.CARTOCODE_
        row.FULLNAME = row.FULLNAME_
        row.FROMADDR_L = row.FROMADDR_L_
        row.TOADDR_L = row.TOADDR_L_
        row.FROMADDR_R = row.FROMADDR_R_
        row.TOADDR_R = row.TOADDR_R_
        row.PARITY_L = row.PARITY_L_
        row.PARITY_R = row.PARITY_R_
        row.PREDIR = row.PREDIR_[:1]
        row.NAME = row.NAME_
        row.AN_NAME = row.AN_NAME_
        row.AN_POSTDIR = row.AN_POSTDIR_
        row.A1_NAME = row.A1_NAME_
        row.A1_POSTTYPE = row.A1_POSTTYPE_
        row.A1_POSTDIR = row.A1_POSTDIR_
        row.A2_PREDIR = row.A2_PREDIR_
        row.A2_NAME = row.A2_NAME_
        row.A2_POSTTYPE = row.A2_POSTTYPE_
        row.A2_POSTDIR = row.A2_POSTDIR_
        row.ADDRSYS_L = row.ADDRSYS_L_
        row.ADDRSYS_R = row.ADDRSYS_R_
        row.ZIPCODE_L = row.ZIPCODE_L_
        row.ZIPCODE_R = row.ZIPCODE_R_
        row.INCMUNI_L = row.INCMUNI_L_
        row.INCMUNI_R = row.INCMUNI_R_
        row.UNINCCOM_L = row.UNINCCOM_L_
        row.UNINCCOM_R = row.UNINCCOM_R_
        row.VERT_LEVEL = row.VERT_LEVEL_
        row.SPEED_LMT = row.SPEED_LMT_
        row.ACCESSCODE = row.ACCESSCODE_
        row.DOT_HWYNAM = row.DOT_HWYNAM_
        row.DOT_RTNAME = row.DOT_RTNAME_
        row.DOT_RTPART = row.DOT_RTPART_
        row.DOT_F_MILE = row.DOT_F_MILE_
        row.DOT_T_MILE = row.DOT_T_MILE_
        row.DOT_FCLASS = row.DOT_FCLASS_
        row.DOT_SRFTYP = row.DOT_SRFTYP_
        row.DOT_CLASS = row.DOT_CLASS_
        row.DOT_OWN_L = row.DOT_OWN_L_
        row.DOT_OWN_R = row.DOT_OWN_R_
        row.DOT_AADT = row.DOT_AADT_
        row.DOT_AADTYR = row.DOT_AADTYR_
        row.BIKE_L = row.BIKE_L_
        row.BIKE_R = row.BIKE_R_
        row.BIKE_PLN_L = row.BIKE_PLN_L_
        row.BIKE_PLN_R = row.BIKE_PLN_R_
        row.BIKE_NOTES = row.BIKE_NOTES_
        row.UNIQUE_ID = row.UNIQUE_ID_
        row.LOCAL_UID = row.LOCAL_UID_
        row.UTAHRD_UID = row.UTAHRD_UID_
        row.SOURCE = row.SOURCE_
        row.EFFECTIVE = row.EFFECTIVE_
        row.EXPIRE = row.EXPIRE_
        row.CUSTOMTAGS = row.CUSTOMTAGS_

        ## TRANSFER OVER VALUES THAT NEED VALIDATION AND FURTHER PROCESSING ##
        # validate POSTTYPE value
        postTypeDomain = GetCodedDomainValue(row.POSTTYPE_, dictOfValidPostTypes)
        if postTypeDomain != "":
            row.POSTTYPE = postTypeDomain
        elif postTypeDomain == "" and row.POSTTYPE_ != None: 
            if len(row.POSTTYPE_) > 1:  
                if not row.POSTTYPE_.isspace():
                    # add the post type they gave to the notes field so we can evaluate it
                    row.UTRANS_NOTES = row.UTRANS_NOTES + "POSTTYPE: " + row.POSTTYPE_ + "; "
                    # add the bad domain value to the text file log
                    AddBadValueToTextFile(countyNumber, "POSTTYPE", str(row.POSTTYPE_))

        # validate STATUS value
        statusDomain = GetCodedDomainValue(row.STATUS_, dictOfValidStatus)
        if statusDomain != "":
            row.STATUS = statusDomain
        elif statusDomain == "" and row.STATUS_ != None: 
            if len(row.STATUS_) > 1:  
                # add the post type they gave to the notes field so we can evaluate it
                row.UTRANS_NOTES = row.UTRANS_NOTES + "STATUS: " + row.STATUS_ + "; "
                # add the bad domain value to the text file log
                AddBadValueToTextFile(countyNumber, "STATUS", str(row.STATUS_))

        # validate ONEWAY value (vecc doesn't have a domain on this field, but their length is limited to one character)
        onewayDomain = GetCodedDomainValue(row.ONEWAY_, dictOfValidOneWay)
        if onewayDomain != "":
            row.ONEWAY = onewayDomain
        elif onewayDomain == "" and row.ONEWAY_ != None: 
            if len(row.ONEWAY_) > 1:  
                # add the post type they gave to the notes field so we can evaluate it
                row.UTRANS_NOTES = row.UTRANS_NOTES + "ONEWAY: " + row.ONEWAY_ + "; "
                # add the bad domain value to the text file log
                AddBadValueToTextFile(countyNumber, "ONEWAY", str(row.ONEWAY_))


        # clear the A1_NAME AND A1_POSTYPE fields if the same data is in AN_NAME
        if (row.A1_NAME_ != ' ' or row.A1_NAME_ != None or row.A1_NAME_ is not None) and (row.AN_NAME_ != ' ' or row.AN_NAME_ != None or row.AN_NAME_ is not None):
            a1_name = str(row.A1_NAME_) # the numeric street name and post type, and sometimes post dir
            an_name = str(row.AN_NAME_) # just the numeric street name
            # check if street name is contained in the A1_NAME field
            if a1_name != '' and an_name != '':
                if str(an_name) in str(a1_name):
                    # clear out the A1_NAME fields
                    row.A1_PREDIR = ""
                    row.A1_NAME = ""
                    row.A1_POSTTYPE = ""
                    row.A1_POSTDIR = ""
  
         # clear the A2_NAME AND A2_POSTYPE fields if the same data is in AN_NAME
        if (row.A2_NAME_ != ' ' or row.A2_NAME_ != None or row.A2_NAME_ is not None) and (row.AN_NAME_ != ' ' or row.AN_NAME_ != None or row.AN_NAME_ is not None):
            a2_name = str(row.A2_NAME_) # the numeric street name and post type, and sometimes post dir
            an_name = str(row.AN_NAME_) # just the numeric street name
            # check if street name is contained in the A2_NAME field
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


def Utah(rows):
    for row in rows:
        # variables
        countyNumber = "49049"
        POSTDIR_FROM_ROADNAME = None
        POSTDIR_FROM_ALTROADNAME = None
        ACS_FROM_ALTROADNAME = None
        POSTDIR_FROM_ALTROADNAME2 = None
        ACS_FROM_ALTROADNAME2 = None
        str_roadname_split = None

        # set all fields to empty or zero or none
        setDefaultValues(row)

        # set county specific fields
        row.COUNTY_L = countyNumber
        row.COUNTY_R = countyNumber
        row.FROMADDR_L = row.FROMLEFT
        row.TOADDR_L = row.TOLEFT
        row.FROMADDR_R = row.FROMRIGHT
        row.TOADDR_R = row.TORIGHT
        row.PREDIR = row.ROADPREDIR.upper()

        # check their roadname field
        if row.ROADNAME != None or row.ROADNAME != " ":
            # if it begins with a digit, then check if it ends with a North, South, East, or West - if so export that to the sufdir field
            str_roadname = row.ROADNAME.strip()

            if str_roadname != None or str_roadname != "":
                if len(str_roadname) > 0:
                    if str_roadname[0].isdigit():
                        # it's an numeric numbered road name
                        # parse out the string to check if sufdir exists
                        str_roadname_split = str_roadname.split(" ")

                        #get the last word in the array
                        if str_roadname_split[-1] == "NORTH" or str_roadname_split[-1] == "SOUTH" or str_roadname_split[-1] == "EAST" or str_roadname_split[-1] == "WEST":
                            POSTDIR_FROM_ROADNAME = str(str_roadname_split[-1]).strip()

                            # check if first word in split is number
                            if str_roadname_split[0].isdigit():
                                row.NAME = str_roadname_split[0].strip()
                            else:
                                row.NAME = row.ROADNAME[:30].upper()
                        else:
                            row.NAME = row.ROADNAME[:30].upper()
                    else:
                        # it's alpha road name
                        row.NAME = row.ROADNAME[:30].upper()

        # validiate POSTTYPE
        ValidateAssign_POSTTYPE(row, row.ROADTYPE, countyNumber)

        # assign POSTDIR
        if row.ROADPOSTDIR != None or POSTDIR_FROM_ROADNAME != None:
            if POSTDIR_FROM_ROADNAME != None:
                # use the first character to pass into the sufdir
                row.POSTDIR = POSTDIR_FROM_ROADNAME[0]
            else:
                row.POSTDIR = row.ROADPOSTDIR.upper()


        # check the altroadname field values and see if they placed an acs value in there, if so move it to the acs alias fields
        if row.ALTROADNAME != None or row.ALTROADNAME != "" or row.ALTROADNAME != " ":
            # if it begins with a digit, then check if it ends with a North, South, East, or West - if so export that to the sufdir field
            str_altroadname1 = row.ALTROADNAME.strip()

            if str_altroadname1 != None or str_altroadname1 != "" or str_altroadname1 != " ":
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

        if row.ALTROADTYPE != None or row.ALTROADTYPE != "" or row.ALTROADTYPE != " ":
            postTypeDomain = GetCodedDomainValue(row.ALTROADTYPE, dictOfValidPostTypes)
            if postTypeDomain != "":
                # it's valid
                row.ALTROADTYPE = postTypeDomain

            #ValidateAssign_POSTTYPE(row,row.ALTROADTYPE,countyNumber)
            #row.A1_POSTTYPE = row.ALTROADTYPE.upper()

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

        # if row.ALTROADTYPE2 != None:
            # row.A1_POSTTYPE = row.ALTROADTYPE2

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

        if row.ALTROADTYPE != None or row.ALTROADTYPE != "" or row.ALTROADTYPE != " ":
            altname = row.ALTROADTYPE
            altname_split = altname.split(" ")
            if len(altname_split) > 0:
                if not altname_split[0].isdigit():
                    # check if valid
                    postTypeDomain = GetCodedDomainValue(altname_split[0], dictOfValidPostTypes)
                    if postTypeDomain != "":
                        # it's valid
                        row.A1_POSTTYPE = postTypeDomain

        # remove posttype if numeric street name
        if row.NAME.isdigit():
            row.POSTTYPE = ""

        # remove the posttype if the 
        if row.A1_NAME is None or row.A1_NAME == "":
            row.A1_POSTTYPE = ""

        # store the row
        rows.updateRow(row)  
        del row


def Davis(rows):
    # get post direction domains
    countyNumber = "49011"

    for row in rows:
        # set all fields to empty or zero or none
        setDefaultValues(row)

        # set county specific fields
        row.COUNTY_L = countyNumber
        row.COUNTY_R = countyNumber
        row.FROMADDR_L = row.LeftFrom
        row.TOADDR_L = row.LeftTo
        row.FROMADDR_R = row.RightFrom
        row.TOADDR_R = row.RightTo
        if row.PrefixDire != None:
            row.PREDIR = row.PrefixDire[:1]
        if row.RoadName != None:
            row.NAME = row.RoadName[:40]

        # check if valid post type
        postTypeDomain = GetCodedDomainValue(row.RoadNameTy, dictOfValidPostTypes)
        if postTypeDomain != "":
            row.POSTTYPE = postTypeDomain
        elif postTypeDomain == "" and len(row.RoadNameTy) > 1:  
            # add the post type they gave to the notes field so we can evaluate it
            row.UTRANS_NOTES = row.UTRANS_NOTES + "POSTTYPE: " + row.RoadNameTy + "; "
            # add the bad domain value to the text file log
            AddBadValueToTextFile(countyNumber, "POSTTYPE", str(row.STREETTYPE))
           
        row.POSTDIR = row.PostDirect
        row.DOT_SRFTYP = row.RoadSurfac

        # check if alias names exist (maybe make this a global function that we can reuse for other counties who do a similar alias name concatination field)
        if row.RoadAliasN != None:
            # get alias name as string
            davisAliasName = row.RoadAliasN

            # check if there's a least one letter in the string
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
                        if davisAliasName_split[-1].upper() in dictOfValidPostTypes:
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
    for row in rows:
        # set all fields to empty or zero or none
        setDefaultValues(row)
        countyNumber = "49057"

        # set county specific fields
        row.COUNTY_L = countyNumber
        row.COUNTY_R = countyNumber        
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
        elif postTypeDomain == "" and row.STREETTYPE != None:
            if len(row.STREETTYPE) > 1:
                # add the post type they gave to the notes field so we can evaluate it
                row.UTRANS_NOTES = row.UTRANS_NOTES + "POSTTYPE: " + row.STREETTYPE + "; "
                # add the bad domain value to the text file log
                AddBadValueToTextFile(countyNumber, "POSTTYPE", str(row.STREETTYPE))
        
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
        countyNumber = "49035"
        
        # set county specific fields
        row.STATE_L = "UT"
        row.STATE_R = "UT"
        row.COUNTY_L = countyNumber
        row.COUNTY_R = countyNumber

        ## TRANSFER OVER SIMPLE VALUES THAT DON'T NEED VALIDATION ##
        # transfer values from same name fields that were renamed with an underscore (this allows us to enforce our domains via the validation code here) 
        row.CARTOCODE = row.CARTOCODE_
        row.FULLNAME = row.FULLNAME_
        row.FROMADDR_L = row.FROMADDR_L_
        row.TOADDR_L = row.TOADDR_L_
        row.FROMADDR_R = row.FROMADDR_R_
        row.TOADDR_R = row.TOADDR_R_
        row.PARITY_L = row.PARITY_L_
        row.PARITY_R = row.PARITY_R_
        row.PREDIR = row.PREDIR_
        row.NAME = row.NAME_
        row.POSTDIR = row.POSTDIR_
        row.AN_NAME = row.AN_NAME_
        row.AN_POSTDIR = row.AN_POSTDIR_
        row.A1_NAME = row.A1_NAME_
        row.A1_POSTTYPE = row.A1_POSTTYPE_
        row.A1_POSTDIR = row.A1_POSTDIR_
        row.A2_PREDIR = row.A2_PREDIR_
        row.A2_NAME = row.A2_NAME_
        row.A2_POSTTYPE = row.A2_POSTTYPE_
        row.A2_POSTDIR = row.A2_POSTDIR_
        row.ADDRSYS_L = row.ADDRSYS_L_
        row.ADDRSYS_R = row.ADDRSYS_R_
        row.ZIPCODE_L = row.ZIPCODE_L_
        row.ZIPCODE_R = row.ZIPCODE_R_
        row.INCMUNI_L = row.INCMUNI_L_
        row.INCMUNI_R = row.INCMUNI_R_
        row.UNINCCOM_L = row.UNINCCOM_L_
        row.UNINCCOM_R = row.UNINCCOM_R_
        row.VERT_LEVEL = row.VERT_LEVEL_
        row.SPEED_LMT = row.SPEED_LMT_
        row.ACCESSCODE = row.ACCESSCODE_
        row.DOT_HWYNAM = row.DOT_HWYNAM_
        row.DOT_RTNAME = row.DOT_RTNAME_
        row.DOT_RTPART = row.DOT_RTPART_
        row.DOT_F_MILE = row.DOT_F_MILE_
        row.DOT_T_MILE = row.DOT_T_MILE_
        row.DOT_FCLASS = row.DOT_FCLASS_
        row.DOT_SRFTYP = row.DOT_SRFTYP_
        row.DOT_CLASS = row.DOT_CLASS_
        row.DOT_OWN_L = row.DOT_OWN_L_
        row.DOT_OWN_R = row.DOT_OWN_R_
        row.DOT_AADT = row.DOT_AADT_
        row.DOT_AADTYR = row.DOT_AADTYR_
        row.BIKE_L = row.BIKE_L_
        row.BIKE_R = row.BIKE_R_
        row.BIKE_PLN_L = row.BIKE_PLN_L_
        row.BIKE_PLN_R = row.BIKE_PLN_R_
        row.BIKE_NOTES = row.BIKE_NOTES_
        row.UNIQUE_ID = row.UNIQUE_ID_
        row.LOCAL_UID = row.LOCAL_UID_
        row.UTAHRD_UID = row.UTAHRD_UID_
        row.SOURCE = row.SOURCE_
        row.UPDATED = row.UPDATED_
        row.EFFECTIVE = row.EFFECTIVE_
        row.EXPIRE = row.EXPIRE_
        row.EDITOR = row.EDITOR_
        row.CUSTOMTAGS = row.CUSTOMTAGS_

        ## TRANSFER OVER VALUES THAT NEED VALIDATION AND FURTHER PROCESSING ##
        # validate POSTTYPE value
        postTypeDomain = GetCodedDomainValue(row.POSTTYPE_, dictOfValidPostTypes)
        if postTypeDomain != "":
            row.POSTTYPE = postTypeDomain
        elif postTypeDomain == "" and row.POSTTYPE_ != None: 
            if len(row.POSTTYPE_) > 1:  
                # add the post type they gave to the notes field so we can evaluate it
                row.UTRANS_NOTES = row.UTRANS_NOTES + "POSTTYPE: " + row.POSTTYPE_ + "; "
                # add the bad domain value to the text file log
                AddBadValueToTextFile(countyNumber, "POSTTYPE", str(row.POSTTYPE_))

        # validate STATUS value
        statusDomain = GetCodedDomainValue(row.STATUS_, dictOfValidStatus)
        if statusDomain != "":
            row.STATUS = statusDomain
        elif statusDomain == "" and row.STATUS_ != None: 
            if len(row.STATUS_) > 1:  
                # add the post type they gave to the notes field so we can evaluate it
                row.UTRANS_NOTES = row.UTRANS_NOTES + "STATUS: " + row.STATUS_ + "; "
                # add the bad domain value to the text file log
                AddBadValueToTextFile(countyNumber, "STATUS", str(row.STATUS_))

        # validate ONEWAY value (vecc doesn't have a domain on this field, but their length is limited to one character)
        onewayDomain = GetCodedDomainValue(row.ONEWAY_, dictOfValidOneWay)
        if onewayDomain != "":
            row.ONEWAY = onewayDomain
        elif onewayDomain == "" and row.ONEWAY_ != None: 
            if len(row.ONEWAY_) > 1:  
                # add the post type they gave to the notes field so we can evaluate it
                row.UTRANS_NOTES = row.UTRANS_NOTES + "ONEWAY: " + row.ONEWAY_ + "; "
                # add the bad domain value to the text file log
                AddBadValueToTextFile(countyNumber, "ONEWAY", str(row.ONEWAY_))


        # clear the A1_NAME AND A1_POSTYPE fields if the same data is in AN_NAME
        if (row.A1_NAME_ != ' ' or row.A1_NAME_ != None or row.A1_NAME_ is not None) and (row.AN_NAME_ != ' ' or row.AN_NAME_ != None or row.AN_NAME_ is not None):
            a1_name = str(row.A1_NAME_) # the numeric street name and post type, and sometimes post dir
            an_name = str(row.AN_NAME_) # just the numeric street name
            # check if street name is contained in the A1_NAME field
            if a1_name != '' and an_name != '':
                if str(an_name) in str(a1_name):
                    # clear out the A1_NAME fields
                    row.A1_PREDIR = ""
                    row.A1_NAME = ""
                    row.A1_POSTTYPE = ""
                    row.A1_POSTDIR = ""
  
         # clear the A2_NAME AND A2_POSTYPE fields if the same data is in AN_NAME
        if (row.A2_NAME_ != ' ' or row.A2_NAME_ != None or row.A2_NAME_ is not None) and (row.AN_NAME_ != ' ' or row.AN_NAME_ != None or row.AN_NAME_ is not None):
            a2_name = str(row.A2_NAME_) # the numeric street name and post type, and sometimes post dir
            an_name = str(row.AN_NAME_) # just the numeric street name
            # check if street name is contained in the A2_NAME field
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
        countyNumber = "49001"

        # set county specific fields
        row.COUNTY_L = countyNumber
        row.COUNTY_R = countyNumber        
        row.FROMADDR_L = row.L_F_ADD
        row.TOADDR_L = row.L_T_ADD
        row.FROMADDR_R = row.R_F_ADD
        row.TOADDR_R = row.R_T_ADD
        row.PREDIR = row.PREDIR_[:1]
        row.NAME = row.STREETNAME[:30]

        # check if valid post type
        postTypeDomain = GetCodedDomainValue(row.STREETTYPE, dictOfValidPostTypes)
        if postTypeDomain != "":
            row.POSTTYPE = postTypeDomain
        elif postTypeDomain == "" and len(row.STREETTYPE) > 1:  
            # add the post type they gave to the notes field so we can evaluate it
            row.UTRANS_NOTES = row.UTRANS_NOTES + "POSTTYPE: " + row.STREETTYPE + "; "
            # add the bad domain value to the text file log
            AddBadValueToTextFile(countyNumber, "POSTTYPE", str(row.STREETTYPE))

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

        # check for status valid values
        statusValue = GetCodedDomainValue(row.STATUS_, dictOfValidStatus)
        if statusValue != "":
            row.STATUS = statusValue
        elif statusValue == "" and len(row.STATUS_) > 0:
            # add the post type they gave to the notes field so we can evaluate it
            row.UTRANS_NOTES = row.UTRANS_NOTES + "STATUS: " + row.STATUS_ + "; "
            # add the bad domain value to the text file log
            AddBadValueToTextFile(countyNumber, "STATUS", str(row.STATUS_))

        ## remove PostDir if street name is alpha
        #if removePostDirIfAlpha(row) == True:
        #    row.POSTDIR = ""

        # remove PostType is street name is numeric
        if removePostTypeIfNumeric(row) == True:
            row.POSTTYPE = ""

        # store the row
        rows.updateRow(row)
        del row


def BoxElder(rows):
    for row in rows:
        # set all fields to empty or zero or none
        setDefaultValues(row)
        countyNumber = "49003"

        # set county specific fields
        row.COUNTY_L = countyNumber
        row.COUNTY_R = countyNumber    
            
        row.FROMADDR_L = row.L_F_ADD
        row.TOADDR_L = row.L_T_ADD
        row.FROMADDR_R = row.R_F_ADD
        row.TOADDR_R = row.R_T_ADD
        row.PREDIR = row.PRE_DIR[:1]
        row.NAME = row.S_NAME[:30]

        # POSTTYPE
        ValidateAssign_POSTTYPE(row, row.S_TYPE, countyNumber)

        row.POSTDIR = row.SUF_DIR

        # validate the AN_NAME value
        if row.ACS_NAME != "":
            # call the validation function
            an_Name, an_PostDir = Validate_AN_NAME(row.ACS_NAME)
            # AN_NAME
            row.AN_NAME = an_Name            

            # AN_POSTDIR
            if an_PostDir != "":
                row.AN_POSTDIR = an_PostDir
            else:
                row.AN_POSTDIR = row.ACS_SUF

        row.A1_NAME = row.ALIAS1
        row.A1_POSTTYPE = row.ALIAS1_TYP
        row.A2_NAME = row.ALIAS2
        row.A2_POSTTYPE = row.ALIAS2_TYP
        
        # check if valid CLASS
        classDomain = GetCodedDomainValue(row.CLASS, dictOfValidRoadClass)
        if classDomain != "":
            row.DOT_FCLASS = classDomain
        elif classDomain == "" and row.CLASS is not None:
            if not row.CLASS.isspace():
                # add the CLASS they gave to the notes field so we can evaluate it
                row.UTRANS_NOTES = row.UTRANS_NOTES + "DOT_FCLASS: " + row.CLASS + "; "
                # add the bad domain value to the text file log
                AddBadValueToTextFile(countyNumber, "DOT_FCLASS", str(row.CLASS))
        
        row.VERT_LEVEL = row.VERTLEVEL
        row.SPEED_LMT = row.SPD_LMT
        row.LOCAL_UID = row.CO_UNIQUE
        row.ONEWAY = row.ONE_WAY

        # these fields have been renamed in UtransETL_CountyToUtrans.py (in step 3) becuase they had the same field name so we added an underscore to enforce our domain
        row.DOT_RTNAME = row.DOT_RTNAME_
        row.DOT_RTPART = row.DOT_RTPART_
        row.SOURCE = row.SOURCE_

        # store the row
        rows.updateRow(row)
        del row


def Carbon(rows):
    for row in rows:
        # set all fields to empty or zero or none
        setDefaultValues(row)
        countyNumber = "49007"
        postType_fromStreetName = False

        # set county specific fields
        row.COUNTY_L = countyNumber
        row.COUNTY_R = countyNumber    
          
        row.FROMADDR_L = row.L_F_ADD
        row.TOADDR_L = row.L_T_ADD
        row.FROMADDR_R = row.R_F_ADD
        row.TOADDR_R = row.R_T_ADD
        row.PREDIR = row.PRE_DIR[:1]
        
        ## NAME
        # remove the posttype, if present.
        # get the last word in the string.
        countystreetname = row.S_NAME
        if countystreetname != "":
            if not countystreetname.isspace():
                row.NAME = countystreetname
                
                countystreetname_split = countystreetname.split()
                # make sure there's more than one word
                if len(countystreetname_split) > 1:
                    last_word = countystreetname_split[-1]
                    # if the last word is "AV" just remove it and move on (they add AV when they have an AVE already in the s_type)
                    if last_word == "AV":
                        # remove the word.
                        countystreetname = countystreetname.rsplit(' ', 1)[0]
                        # write value to NAME field.
                        row.NAME = countystreetname
                    else:
                        # check if last word in streetname is posttype, only if it's two characters long (so we don't remove valid road names line canyon, creek, park, etc.)
                        if len(last_word) == 2:
                            postTypeDomain = GetCodedDomainValue(last_word, dictOfValidPostTypes)
                            if postTypeDomain != "":
                                # a recognized posttype was found in the streettype, maybe use this as the valid posttype
                                # check if county's s_type has a value, if not use this one from the streetname.
                                if row.S_TYPE == "":
                                    # no value in s_type, so use this value.
                                    row.POSTTYPE = postTypeDomain
                                    postType_fromStreetName = True

                                    # remove this posttype value from the streetname and then assign it.
                                    countystreetname = countystreetname.rsplit(' ', 1)[0]
                    
                                    # write value to NAME field.
                                    row.NAME = countystreetname
                                else: # s_type has a posttype, so use this one instead below
                                    # remove this posttype value from the streetname.
                                    countystreetname = countystreetname.rsplit(' ', 1)[0]
                                    postType_fromStreetName = False
                                    row.NAME = countystreetname
                            else: # last word in street name is not a valid posttype   
                                row.NAME = countystreetname
                        else: # the last word is not two characters long so just use the whole thing in the NAME field
                            row.NAME = countystreetname
                else:
                    # the county street name is less than two words
                    row.NAME = countystreetname

        
        ## POSTTYPE 
        if postType_fromStreetName == False:
            ValidateAssign_POSTTYPE(row, row.S_TYPE, countyNumber)
        
        ## POSTDIR
        if row.SUF_DIR in ("N","S","E","W"):
            row.POSTDIR = row.SUF_DIR

        # AN_NAME and AN_POSTDIR
        if row.ACS_ALIAS != "":
            # call the validation function
            an_Name, an_PostDir = Validate_AN_NAME(row.ACS_ALIAS)
            # AN_NAME
            if an_Name != "":
                row.AN_NAME = an_Name            

            # AN_POSTDIR
            if an_PostDir != "":
                row.AN_POSTDIR = an_PostDir
                # if an_postdir is same as postdir then remove postdir
                if an_PostDir == row.POSTDIR:
                    row.POSTDIR = ""

        row.A1_NAME = row.ALIAS1
        row.A1_POSTTYPE = row.ALIAS1_TYP
        row.A2_NAME = row.ALIAS2
        row.A2_POSTTYPE = row.ALIAS2_TYP
        
        ## DOT_SRFTYP - check if valid value
        classSurfType = GetCodedDomainValue(row.S_SURF2, dictOfValidSurfaceType)
        if classSurfType != "":
            row.DOT_SRFTYP = classSurfType

        # CLASS - check if valid value
        classDomain = GetCodedDomainValue(row.CLASS, dictOfValidRoadClass)
        if classDomain != "":
            row.DOT_FCLASS = classDomain
        elif classDomain == "" and row.CLASS is not None:
            if not row.CLASS.isspace():
                # add the CLASS they gave to the notes field so we can evaluate it
                row.UTRANS_NOTES = row.UTRANS_NOTES + "DOT_FCLASS: " + row.CLASS + "; "
                # add the bad domain value to the text file log
                AddBadValueToTextFile(countyNumber, "DOT_FCLASS", str(row.CLASS))
        
        row.SPEED_LMT = row.SPD_LMT

        ## check if NAME is empty and one of the numeric alias field is not, if so carry those values to the primary road name fields
        if row.NAME == "" and row.AN_NAME != "":
            row.NAME = row.AN_NAME
            row.POSTDIR = row.AN_POSTDIR
            row.AN_NAME = ""
            row.AN_POSTDIR = ""

        # store the row
        rows.updateRow(row)
        del row


def Wasatch(rows):
    for row in rows:
        # set all fields to empty or zero or none
        setDefaultValues(row)
        countyNumber = "49051"
 
        ## TRANSFER OVER SIMPLE VALUES THAT DON'T NEED VALIDATION ##
        row.COUNTY_L = countyNumber
        row.COUNTY_R = countyNumber
        row.FROMADDR_L = row.L_F_ADD
        row.TOADDR_L = row.L_T_ADD
        row.FROMADDR_R = row.R_F_ADD
        row.TOADDR_R = row.R_T_ADD
        row.PREDIR = row.PRE_DIR[:1]
        row.NAME = row.S_NAME  
        row.POSTDIR = row.SUF_DIR[:1]              
        row.AN_NAME = row.ACS_STREET
        row.AN_POSTDIR = row.ACS_SUFDIR[:1] 

        ## TRANSFER OVER FIELDS THAT WE RENAMED BECUASE WE SHARED THE SAME NAME (this allows us to validate our domain names) ##
        ValidateAssign_STATUS(row, row.STATUS_, countyNumber)

        ## TRANSFER OVER VALUES THAT NEED VALIDATION AND FURTHER PROCESSING ##
        ValidateAssign_POSTTYPE(row, row.S_TYPE, countyNumber)
        ValidateAssign_DOT_FCLASS(row, row.S_AGFUNC, countyNumber) 
        ValidateAssign_DOT_SRFTYP(row, row.S_SURF, countyNumber)

        # check if we need to parse the ALIAS_1 field (they have predir, postdir, and posttypes in the field)
        if row.ALIAS_1 is not None or row.ALIAS_1 != "":
            is_valid_parse, pre_dir, street_name, post_type, post_dir = ParseFullAddress(row.ALIAS_1)

            if is_valid_parse == True:
                # it WAS a valid parse
                if street_name.isdigit():
                    # the street name is numeric
                    row.AN_NAME = street_name
                    row.AN_POSTDIR = post_dir
                else:
                    # the streetname is alpha
                    row.A1_PREDIR = pre_dir
                    row.A1_NAME = street_name
                    row.A1_POSTTYPE = post_type
                    row.A1_POSTDIR = post_dir
            else:
                # it was NOT a valid parse
                row.A1_NAME = row.ALIAS_1
                        
        # store the row
        rows.updateRow(row)
        del row


def Duchesne(rows):
    for row in rows: 
        # set all fields to empty or zero or none
        setDefaultValues(row)
        countyNumber = "49013"
        
        ## TRANSFER OVER SIMPLE VALUES THAT DON'T NEED VALIDATION ##
        row.COUNTY_L = countyNumber
        row.COUNTY_R = countyNumber   
        if row.L_F_ADD != "":
            row.FROMADDR_L = row.L_F_ADD
        if row.L_T_ADD != "":
            row.TOADDR_L = row.L_T_ADD
        if row.R_F_ADD != "":     
            row.FROMADDR_R = row.R_F_ADD
        if row.R_T_ADD != "":
            row.TOADDR_R = row.R_T_ADD
        if HasValidDirection(row,"PREDIR_"):
            row.PREDIR = row.PREDIR_[:1]
        row.NAME = row.STREETNAME[:30]
        if HasValidDirection(row, "SUFDIR"):
            row.POSTDIR = row.SUFDIR[:1]
        row.AN_NAME = row.ACSNAME
        row.AN_POSTDIR = row.ACSSUF
        row.A1_PREDIR = ""
        row.A1_POSTTYPE = row.ALIAS1TYPE
        row.A1_POSTDIR = ""
        row.A2_PREDIR = ""
        row.A2_POSTTYPE = row.ALIAS2TYPE
        row.A2_POSTDIR = ""
        row.VERT_LEVEL = row.VERTLEVEL
        row.SPEED_LMT = row.SPEED
        row.LOCAL_UID = row.COUNIQUE

        ## TRANSFER OVER FIELDS THAT WE RENAMED WITH AN APPENDED UNDERSCORE (FIELDNAME_) BECUASE WE SHARED THE SAME NAME (this allows us to validate our domain names) ##
        #row.ONEWAY = row.ONEWAY_

        ## TRANSFER OVER VALUES THAT NEED VALIDATION AND FURTHER PROCESSING ##
        ValidateAndAssign_FieldValue(row, "POSTTYPE", row.STREETTYPE, countyNumber, dictOfValidPostTypes)
        ValidateAndAssign_FieldValue(row, "ONEWAY", row.ONEWAY_, countyNumber, dictOfValidOneWay)
        ValidateAndAssign_FieldValue(row, "DOT_SRFTYP", row.SURFTYPE, countyNumber, dictOfValidSurfaceType)
        ValidateAndAssign_FieldValue(row, "STATUS", row.STATUS_, countyNumber, dictOfValidStatus)
        ValidateAndAssign_FieldValue(row, "DOT_CLASS", row.CLASS, countyNumber, dictOfValidRoadClass)

        # check if we need to parse the ALIAS1 field (they have predir, postdir, and posttypes in the field - as well as numeric alias road names)
        ParseAndAssign_FullAddress(row, "ALIAS1", False, True, False)
        # check if we need to parse the ALIAS2 field (they have predir, postdir, and posttypes in the field - as well as numeric alias road names)
        ParseAndAssign_FullAddress(row, "ALIAS2", False, False, True)

        # check if the alias1type and alias2type fields have valid posttypes, if so overwrite what was assigned from the fullname parser above
        ValidateAndAssign_FieldValue(row, "A1_POSTTYPE", row.ALIAS1TYPE, countyNumber, dictOfValidPostTypes)
        ValidateAndAssign_FieldValue(row, "A2_POSTTYPE", row.ALIAS2TYPE, countyNumber, dictOfValidPostTypes)

        # store the row
        rows.updateRow(row)
        del row


def Iron(rows):
    for row in rows: 
        # set all fields to empty or zero or none
        setDefaultValues(row)
        countyNumber = "49021"
        
        ## TRANSFER OVER SIMPLE VALUES THAT DON'T NEED VALIDATION ##
        row.COUNTY_L = countyNumber
        row.COUNTY_R = countyNumber   
        if row.L_F_ADD != "":
            row.FROMADDR_L = row.L_F_ADD
        if row.L_T_ADD != "":
            row.TOADDR_L = row.L_T_ADD
        if row.R_F_ADD != "":     
            row.FROMADDR_R = row.R_F_ADD
        if row.R_T_ADD != "":
            row.TOADDR_R = row.R_T_ADD
        if HasValidDirection(row,"PREDIR_"):
            row.PREDIR = row.PREDIR_[:1]
        row.NAME = row.STREETNAME[:30]
        if HasValidDirection(row,"SUFDIR"):
            row.POSTDIR = row.SUFDIR
        row.AN_NAME = row.ACSNAME
        if HasValidDirection(row,"ACSSUF"):
            row.AN_POSTDIR = row.ACSSUF[:1]
        row.A1_PREDIR = ""
        row.A1_NAME = row.ALIAS1
        row.A1_POSTTYPE = row.ALIAS1TYPE
        row.A1_POSTDIR = ""
        row.A2_PREDIR = ""
        row.A2_NAME = row.ALIAS2
        row.A2_POSTTYPE = row.ALIAS2TYPE
        row.A2_POSTDIR = ""
        row.VERT_LEVEL = row.VERTLEVEL
        row.SPEED_LMT = row.SPEED
        row.LOCAL_UID = row.COUNIQUE

        ## TRANSFER OVER FIELDS THAT WE RENAMED WITH AN APPENDED UNDERSCORE (FIELDNAME_) BECUASE WE SHARED THE SAME NAME (this allows us to validate our domain names) ##
        row.DOT_RTNAME = row.DOT_RTNAME_ 
        row.DOT_RTPART = row.DOT_RTPART_

        ## TRANSFER OVER VALUES THAT NEED VALIDATION AND FURTHER PROCESSING ##
        ValidateAndAssign_FieldValue(row, "POSTTYPE", row.STREETTYPE, countyNumber, dictOfValidPostTypes)
        ValidateAndAssign_FieldValue(row, "ONEWAY", row.ONEWAY_, countyNumber, dictOfValidOneWay)
        ValidateAndAssign_FieldValue(row, "DOT_SRFTYP", row.SURFTYPE, countyNumber, dictOfValidSurfaceType)
        ValidateAndAssign_FieldValue(row, "STATUS", row.STATUS_, countyNumber, dictOfValidStatus)
        ValidateAndAssign_FieldValue(row, "DOT_CLASS", row.CLASS, countyNumber, dictOfValidRoadClass)
        

        # store the row
        rows.updateRow(row)
        del row


def Summit(rows):
    for row in rows: 
        # set all fields to empty or zero or none
        setDefaultValues(row)
        countyNumber = "49043"
        
        ## TRANSFER OVER SIMPLE VALUES THAT DON'T NEED VALIDATION ##
        row.COUNTY_L = countyNumber
        row.COUNTY_R = countyNumber   
        if row.FROMLEFT != "":
            row.FROMADDR_L = row.FROMLEFT
        if row.TOLEFT != "":
            row.TOADDR_L = row.TOLEFT
        if row.FROMRIGHT != "":     
            row.FROMADDR_R = row.FROMRIGHT
        if row.TORIGHT != "":
            row.TOADDR_R = row.TORIGHT
        if HasValidDirection(row, "PREFIX_DIR"):
            row.PREDIR = row.PREFIX_DIR[:1]
        if FieldHasValue(row, "STREET"):
            row.NAME = row.STREET[:30]
        if HasValidDirection(row,"POST_DIR"):
            row.POSTDIR = row.POST_DIR[:1]
        
        ## TRANSFER OVER FIELDS THAT WE RENAMED WITH AN APPENDED UNDERSCORE (FIELDNAME_) BECUASE WE SHARED THE SAME NAME (this allows us to validate our domain names) ##

        ## TRANSFER OVER VALUES THAT NEED VALIDATION AND FURTHER PROCESSING ##
        ValidateAndAssign_FieldValue(row, "POSTTYPE", row.SUFF_TYPE, countyNumber, dictOfValidPostTypes)
        ValidateAndAssign_FieldValue(row, "ONEWAY", row.ONEWAY_, countyNumber, dictOfValidOneWay)
        ValidateAndAssign_FieldValue(row, "STATUS", row.STATUS_, countyNumber, dictOfValidStatus)

        # add the pre_type value to the street name if one exists (summit puts the highway type here)
        if FieldHasValue(row, "PRE_TYPE"):
            row.NAME = str(row.PRE_TYPE) + " " + str(row.NAME)
            row.NAME = row.NAME.strip()
        
        # check if there's an alias name: if OTHER_NAME is different from STREET
        if FieldHasValue(row, "OTHER_NAME"):
             # check if the fisrt value/word and if they are the same, then assume it's not an alias name, if different then pass the OTHER_NAME into the alias1 fulladdress parser
             _other_name = row.OTHER_NAME
             _street = row.STREET
             _other_name_split = _other_name.split(" ")
             _street_split = _street.split(" ")
             if len(_other_name_split) > 0:
                _alias_first_word = _other_name_split[0]
                _alias_first_word = str(_alias_first_word).upper()
             if len(_street_split) > 0:
                _primary_first_word = _street_split[0]
                _primary_first_word = str(_primary_first_word).upper()
                   
             if _alias_first_word != _primary_first_word:
                ParseAndAssign_FullAddress(row, "OTHER_NAME", False, True, False)

        # store the row
        rows.updateRow(row)
        del row

######################################################################
#### GENERAL (NON-FIELD COUNTY MAPPING) FUNCTIONS BELOW THIS LINE ####

### THESE VALIDATE... ONES I'VE DEPRECATED BUT I'M LEAVING THEM HERE FOR NOW AS THEY ARE BEING USED IN SOME OF THE FISRT COUNTIES I DID THE ETL SCRIPT FOR... I NEED TO CONVERT THOSE SCRIPTS TO USE THE UNIVERSAL FUNCTION IN THE GLOBALFUNCTIONS SCRIPT AND THEN I CAN DELETE THESE
# validate and assign values to POSTTYPE
def ValidateAssign_POSTTYPE(row, county_posttype, countyNumber):
    # check if valid
    postTypeDomain = GetCodedDomainValue(county_posttype, dictOfValidPostTypes)
    if postTypeDomain != "":
        # is valid
        row.POSTTYPE = postTypeDomain
    elif postTypeDomain == "" and len(county_posttype) > 1:
        # is not valid
        # add the post type they gave to the notes field so we can evaluate it
        row.UTRANS_NOTES = row.UTRANS_NOTES + "POSTTYPE: " + county_posttype + "; "
        # add the bad domain value to the text file log
        AddBadValueToTextFile(countyNumber, "POSTTYPE", str(county_posttype))

# validate and assign values to STATUS
def ValidateAssign_STATUS(row, county_status, countyNumber):
    statusValue = GetCodedDomainValue(county_status, dictOfValidStatus)
    if statusValue != "":
        row.STATUS = statusValue
    elif statusValue == "" and len(county_status) > 0:
        # add the post type they gave to the notes field so we can evaluate it
        row.UTRANS_NOTES = row.UTRANS_NOTES + "STATUS: " + county_status + "; "
        # add the bad domain value to the text file log
        AddBadValueToTextFile(countyNumber, "STATUS", str(county_status))

# validate and assign values to DOT_FCLASS
def ValidateAssign_DOT_FCLASS(row, county_fclass, countyNumber):
    # convert the value to stirng, in case it was an int value
    _county_fclass = str(county_fclass)
    fclassValue = GetCodedDomainValue(_county_fclass, dictOfValidFunctionalClass)
    if fclassValue != "":
        row.DOT_FCLASS = fclassValue
    elif fclassValue == "" and len(_county_fclass) > 0:
        # add the dot_fclass they gave to the notes field so we can evaluate it
        row.UTRANS_NOTES = row.UTRANS_NOTES + "DOT_FCLASS: " + _county_fclass + "; "
        # add the bad domain value to the text file log
        AddBadValueToTextFile(countyNumber, "DOT_FCLASS", _county_fclass)

# validate and assign values to DOT_SRFTYP
def ValidateAssign_DOT_SRFTYP(row, county_srftype, countyNumber):
    # convert the value to stirng, in case it was an int value
    _county_srftype =str(county_srftype)
    srftypeValue = GetCodedDomainValue(_county_srftype, dictOfValidSurfaceType)
    if srftypeValue != "":
        row.DOT_SRFTYP = srftypeValue
    elif srftypeValue == "" and len(county_srftype) > 0:
        # add the dot_fclass they gave to the notes field so we can evaluate it
        row.UTRANS_NOTES = row.UTRANS_NOTES + "DOT_SRFTYP: " + _county_srftype + "; "
        # add the bad domain value to the text file log
        AddBadValueToTextFile(countyNumber, "DOT_SRFTYP", _county_srftype)
 

## global variables that are dependent on function instantiation
dictOfValidPostTypes = CreateDomainDictionary('CVDomain_StreetType')
dictOfValidStatus = CreateDomainDictionary('CVDomain_Status')
dictOfValidAccessIssues = CreateDomainDictionary('CVDomain_AccessIssues')
dictOfValidRoadClass = CreateDomainDictionary('CVDomain_RoadClass')
dictOfValidSurfaceType = CreateDomainDictionary('CVDomain_SurfaceType')
dictOfValidOneWay = CreateDomainDictionary('CVDomain_OneWay')
dictOfValidVerticalLevel = CreateDomainDictionary('CVDomain_VerticalLevel')
dictOfValidFunctionalClass = CreateDomainDictionary('CVDomain_FunctionalClass')
#arcpy.AddMessage("  Approved-Domain PostType: " + str(dictOfValidPostTypes))
#arcpy.AddMessage("  Approved-Domain Status: " + str(dictOfValidStatus))
#arcpy.AddMessage("  Approved-Domain AccessIssues: " + str(dictOfValidAccessIssues))
#arcpy.AddMessage("  Approved-Domain RoadClass: " + str(dictOfValidRoadClass))
#arcpy.AddMessage("  Approved-Domain SurfaceType: " + str(dictOfValidSurfaceType))
#arcpy.AddMessage("  Approved-Domain OneWay: " + str(dictOfValidOneWay))
#arcpy.AddMessage("  Approved-Domain VerticalLevels: " + str(dictOfValidVerticalLevel))
#arcpy.AddMessage("  Approved-Domain DOT_FClass: " + str(dictOfValidFunctionalClass))