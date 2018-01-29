import sys
# go up a level in directory structure
# sys.path.insert(0, '..')
# import functions from global functions
from UtransETL_GlobalFunctions import CalcUtransFields, GetUtransFieldSpecs, UpperCoreUtransFields, GetRoadTypeDomains
from UtransETL_FieldMappingFunctions import Washington, Utah, Davis, Weber
import arcpy, os
from arcpy import env
import time
from datetime import date

countyName = arcpy.GetParameterAsText(1)

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
arcpy.AddMessage("Creating county-temp feature class...")
countySourceTEMP = countySource + "Temp"
arcpy.CopyFeatures_management(countySource, countySourceTEMP)

#tempfl = arcpy.MakeFeatureLayer_management(countySourceTEMP, "fclayer")

#outputFeatureClass = dirname + "\\" + countyName + "ETL_" + strDate
outputFeatureClass = dirname + "\\" + countyName + "Temp"

utdm = r"K:\AGRC Projects\UtransEditing\Data\UtahRoadsNGSchema.gdb\Roads_Edit"

arcpy.CopyFeatures_management(utdm, outputFeatureClass)

# get array of utrans field info.
arcpy.AddMessage("Getting Utrans field specs...")
utransFieldSpecs = GetUtransFieldSpecs()

# add utrans field info to county source (temp) data.
arcpy.AddMessage("Adding missing fields to county-temp layer...")
for field in utransFieldSpecs:
   if not arcpy.ListFields(countySourceTEMP, field[0]):
       arcpy.AddField_management(*(countySourceTEMP,) + field)

# get roadtype domain values in list
arcpy.AddMessage("Get domain values for street types from utah data model...")
listOfStreetTypes = GetRoadTypeDomains("K:/AGRC Projects/UtransEditing/Data/UtahRoadsNGSchema.gdb")

# loop through all the fields and calc over values.
arcpy.AddMessage("Begin calculating over values to utrans schema...")
rows = arcpy.UpdateCursor(countySourceTEMP)
#if countyName == "Washington":
#    Washington(rows)
eval(countyName)(rows, listOfStreetTypes)
del rows
arcpy.AddMessage("Finished calculating over values to utrans schema...")
      
# append VECC temp schema with UTNGDM
arcpy.AddMessage("Append county-temp values to Utrans Data Model feature class.")
arcpy.Append_management (countySourceTEMP, outputFeatureClass, "NO_TEST", "", "")

# delete spaces in UTDM, and calculate county name values
arcpy.AddMessage("Convert null to empty string or zeros...")
rows = arcpy.UpdateCursor(outputFeatureClass)
CalcUtransFields(rows)
del rows

# upper case some of the core utrans fields
arcpy.AddMessage("Uppercase core utrans fields...")
rows = arcpy.UpdateCursor(outputFeatureClass)
UpperCoreUtransFields(rows)
del rows

## remove the street type if a numeric street name
#arcpy.AddMessage("Remove PostType if numeric street name...")
#rows = arcpy.UpdateCursor(outputFeatureClass)
#removePostTypeIfNumeric(rows)
#del rows

arcpy.Delete_management (countySourceTEMP, "")

# remove curves from the the data in our schema
arcpy.AddMessage("Begin removing curves, if any...")
arcpy.Densify_edit(outputFeatureClass, "ANGLE","", "", "")

# enusre that vertices are not too close, causing errors for the roads and highways system that does not allow vertices within 1 meter - this tool also removes bezier curves and arc segments, converting them to strait lines so I don't think we need the densify tool above, but let's keep it for now.
arcpy.AddMessage("Generalize the line features...")
arcpy.Generalize_edit(outputFeatureClass, "2 Meters")

# remove any segments that are not within the county
arcpy.AddMessage("Begin removing segments that are outside of the county...")
# add space to county name for county query if BoxElder, SaltLake, or SanJuan
queryCountyName = countyName
if queryCountyName == "BoxElder":
    queryCountyName = "Box Elder"
if queryCountyName == "SaltLake":
    queryCountyName = "Salt Lake"
if queryCountyName == "SanJuan":
    queryCountyName = "San Juan"
queryString = "NAME = '" + queryCountyName + "'"
arcpy.AddMessage("Query string for county boundaries layer: " + queryString)
arcpy.MakeFeatureLayer_management(r"Database Connections\DC_agrc@SGID10@sgid.agrc.utah.gov.sde\SGID10.BOUNDARIES.Counties", "counties_lyr", queryString)
arcpy.MakeFeatureLayer_management(outputFeatureClass, 'countyETL_lyr')

arcpy.SelectLayerByLocation_management('countyETL_lyr', 'intersect', "counties_lyr")
arcpy.CopyFeatures_management('countyETL_lyr', dirname + "\\" + countyName + "ETL_" + strDate)

# Execute Delete the Utah road layer will all the segments, including segments outside the county
arcpy.Delete_management(dirname + "\\" + countyName + "Temp")

# alter the alias name
finalFeatureClassOutput = dirname + "\\" + countyName + "ETL_" + strDate
# add alias name to the feature class for use in the ArcMap Utrans Editor (was outputFeatureClass)
arcpy.AlterAliasName(finalFeatureClassOutput, "COUNTY_STREETS")

arcpy.AddMessage("ETL Process Done!")