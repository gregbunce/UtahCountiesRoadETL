import sys
# go up a level in directory structure
# sys.path.insert(0, '..')
# import functions from global functions
from UtransETL_GlobalFunctions import CalcUtransFields, GetUtransFieldSpecs, UpperCoreUtransFields, RemoveSpecialCharacters, FormatToAgrcHighwayNamingConvention, MoveNumericA1orA2ToANfield
from UtransETL_FieldMappingFunctions import Washington, Utah, Davis, Weber, SaltLake, Beaver, BoxElder, Carbon, Wasatch, Duchesne, Iron, Summit, Tooele, Morgan, Cache, Daggett, Emery, Grand, SanJuan, Kane, Rich, Piute, Sevier
import arcpy, os
from arcpy import env
import time
from datetime import date
from datetime import datetime

# get county name
countyName = arcpy.GetParameterAsText(1)

# create print message variables
total_steps = 16
current_step = 0

# get the date
today = date.today()
strDate = str(today.month).zfill(2) + str(today.day).zfill(2) +  str(today.year)

#### SET THE INPUT PATH TO COUNTY DATA ####
countySource = arcpy.GetParameterAsText(0)

# get the directory path from the countySource layer
dirname = os.path.dirname(arcpy.Describe(countySource).catalogPath)
desc = arcpy.Describe(dirname)
if hasattr(desc, "datasetType") and desc.datasetType=='FeatureDataset':
    dirname = os.path.dirname(dirname)

# create countySourceTEMP to not alter the county's data.
current_step += 1
arcpy.AddMessage("[step " + str(current_step) + " of " + str(total_steps) + "] Creating county-temp feature class...")
countySourceTEMP = countySource + "Temp"
arcpy.CopyFeatures_management(countySource, countySourceTEMP)

#tempfl = arcpy.MakeFeatureLayer_management(countySourceTEMP, "fclayer")

#outputFeatureClass = dirname + "\\" + countyName + "ETL_" + strDate
outputFeatureClass = dirname + "\\" + countyName + "Temp"

#utdm = r"K:\AGRC Projects\UtransEditing\Data\UtahRoadsNGSchema.gdb\Roads_Edit"
#utdm = r"O:\UtransEditing\Data\UtahRoadsNGSchema.gdb\Roads_Edit"
utdm = r"L:\agrc\data\schemas\UtahRoadsNGSchema.gdb\Roads_Edit"
arcpy.CopyFeatures_management(utdm, outputFeatureClass)

# get array of utrans field info.
current_step += 1
arcpy.AddMessage("[step " + str(current_step) + " of " + str(total_steps) + "] Getting Utrans field specs...")
utransFieldSpecs = GetUtransFieldSpecs()

# add utrans field info to county source (temp) data.
current_step += 1
arcpy.AddMessage("[step " + str(current_step) + " of " + str(total_steps) + "] Adding missing fields to county-temp layer...")
for field in utransFieldSpecs:
    # the field is not there, so add the utrans-based-schema one
    if not arcpy.ListFields(countySourceTEMP, field[0]):
        arcpy.AddField_management(*(countySourceTEMP,) + field)
    else:
        # field is there so rename it (add underscore after field name so we know it's the county's field when field mapping)
        new_field_name = str(field[0]) + "_"
        arcpy.AddMessage("  renamed county's " + field[0] + " field to " + new_field_name)
        arcpy.AlterField_management(countySourceTEMP, field[0], new_field_name, new_field_name)
        # add utrans-based-domain one
        arcpy.AddField_management(*(countySourceTEMP,) + field)

# get roadtype domain values in list
current_step += 1
arcpy.AddMessage("[step " + str(current_step) + " of " + str(total_steps) + "] Getting valid domain values from utah data model...")
#listOfStreetTypes = GetRoadTypeDomains("K:/AGRC Projects/UtransEditing/Data/UtahRoadsNGSchema.gdb")

# loop through all the fields and calc over values.
current_step += 1
arcpy.AddMessage("[step " + str(current_step) + " of " + str(total_steps) + "] Begin calculating over values to utrans schema...")
rows = arcpy.UpdateCursor(countySourceTEMP)
# call the update rows function for the specified county
eval(countyName)(rows)
del rows
current_step += 1
arcpy.AddMessage("[step " + str(current_step) + " of " + str(total_steps) + "] Finished calculating over values to utrans schema...")

# append county temp schema with UTNGDM
current_step += 1
arcpy.AddMessage("[step " + str(current_step) + " of " + str(total_steps) + "] Appending county-temp values to Utrans Data Model feature class.")
arcpy.Append_management (countySourceTEMP, outputFeatureClass, "NO_TEST", "", "")

# delete spaces in UTDM, and calculate county name values
current_step += 1
arcpy.AddMessage("[step " + str(current_step) + " of " + str(total_steps) + "] Converting null to empty string or zeros...")
rows = arcpy.UpdateCursor(outputFeatureClass)
CalcUtransFields(rows)
del rows

# upper case some of the core utrans fields
current_step += 1
arcpy.AddMessage("[step " + str(current_step) + " of " + str(total_steps) + "] Uppercasing core utrans fields...")
rows = arcpy.UpdateCursor(outputFeatureClass)
UpperCoreUtransFields(rows)
del rows

# remove special characters apostrophes, if present in NAME, A1_NAME, and A2_NAME fields
current_step += 1
arcpy.AddMessage("[step " + str(current_step) + " of " + str(total_steps) + "] Removing special characters in road name fields...")
rows = arcpy.UpdateCursor(outputFeatureClass)
RemoveSpecialCharacters(rows)
del rows

# format the county's highway name convention to match agrcs
current_step += 1
arcpy.AddMessage("[step " + str(current_step) + " of " + str(total_steps) + "] Formatting highway names to match AGRC's convention...")
rows = arcpy.UpdateCursor(outputFeatureClass)
FormatToAgrcHighwayNamingConvention(rows)
del rows

# move numeric alias values from A1 or A2 to AN fields
current_step += 1
arcpy.AddMessage("[step " + str(current_step) + " of " + str(total_steps) + "] Moving numeric alias values from A1 and A2 to AN fields...")
rows = arcpy.UpdateCursor(outputFeatureClass)
MoveNumericA1orA2ToANfield(rows)
del rows

# delete the temp/scratch layer
arcpy.Delete_management (countySourceTEMP, "")

# remove curves from the the data in our schema
current_step += 1
arcpy.AddMessage("[step " + str(current_step) + " of " + str(total_steps) + "] Removing curves, if any...")
arcpy.Densify_edit(outputFeatureClass, "ANGLE","", "", "")

# enusre that vertices are not too close, causing errors for the roads and highways system that does not allow vertices within 1 meter - this tool also removes bezier curves and arc segments, converting them to strait lines so I don't think we need the densify tool above, but let's keep it for now.
current_step += 1
arcpy.AddMessage("[step " + str(current_step) + " of " + str(total_steps) + "] Generalizing the line features...")
arcpy.Generalize_edit(outputFeatureClass, "2 Meters")

# remove any segments that are not within the county
current_step += 1
arcpy.AddMessage("[step " + str(current_step) + " of " + str(total_steps) + "] Begin removing segments that are outside of the county...")
# add space to county name for county query if BoxElder, SaltLake, or SanJuan
queryCountyName = countyName
if queryCountyName == "BoxElder":
    queryCountyName = "Box Elder"
if queryCountyName == "SaltLake":
    queryCountyName = "Salt Lake"
if queryCountyName == "SanJuan":
    queryCountyName = "San Juan"
queryString = "NAME = '" + queryCountyName + "'"
current_step += 1
arcpy.AddMessage("[step " + str(current_step) + " of " + str(total_steps) + "] Query string for county boundaries layer: " + queryString)
arcpy.MakeFeatureLayer_management(r"Database Connections\DC_agrc@SGID10@sgid.agrc.utah.gov.sde\SGID10.BOUNDARIES.Counties", "counties_lyr", queryString)
arcpy.MakeFeatureLayer_management(outputFeatureClass, 'countyETL_lyr')

arcpy.SelectLayerByLocation_management('countyETL_lyr', 'intersect', "counties_lyr")
strTime = datetime.now().strftime('%H%M')
arcpy.CopyFeatures_management('countyETL_lyr', dirname + "\\" + countyName + "ETL_" + strDate + "_" + strTime)

# Execute Delete the Utah road layer will all the segments, including segments outside the county
arcpy.Delete_management(dirname + "\\" + countyName + "Temp")

# alter the alias name
finalFeatureClassOutput = dirname + "\\" + countyName + "ETL_" + strDate + "_" + strTime

# add alias name to the feature class for use in the ArcMap Utrans Editor (was outputFeatureClass)
arcpy.AlterAliasName(finalFeatureClassOutput, "COUNTY_STREETS")

arcpy.AddMessage("ETL Process Done!")
arcpy.AddMessage("*REMINDER*: Check for non-valid domains in either the UTRANS_NOTES field or the text file here L:\agrc\utrans\UtransEditing\scripts_and_tools\_script_logs\CountiesDomainValueErrors.txt")