import arcpy
arcpy.env.workspace = arcpy.GetParameterAsText(1) #In the tool, this is the second input (Input Folder) which is the folder that contains all the feature classes.

main = arcpy.GetParameterAsText(0) #Choose any shapefile to be the main layer that everything will be projected to. In the tool, this is the first input (Input Feature).
name = main.replace(".shp","") #Create variable for main file's name without .shp

main_spatial_ref = arcpy.Describe(main).spatialReference #create variable to easily extract spatial reference information from main shapefile

print name+": "+ main_spatial_ref.name #Check to see what projection the main file is using
print "Factory Code: "+ str(main_spatial_ref.factoryCode) #Check which factory code corresponds to this projection
out_coordinate_system = arcpy.SpatialReference(main_spatial_ref.factoryCode) #Assign variable to main file's projection to use when projecting the other feature classes

feature_classes = arcpy.ListFeatureClasses() #Create list of the feature classes that are in the Data folder
for fc in feature_classes: #Start for loop that runs through each feature class in the data folder
    spatial_ref = arcpy.Describe(fc).spatialReference #Create variable to easily extract spatial reference info from any of the feature classes
    if fc != main: #Excludes the main shapefile libraries from the for loop 
        if spatial_ref.name == main_spatial_ref.name: #If the projection of the feature class is the same as that of the main file
            print fc, "has the same projection as ",name #Prints feature class name has the same projection as the main file           
        else:
            print fc,": "+spatial_ref.name #If it does not have the name projection, print what it does have
            file_name_new = fc.replace(".shp", "") #Create variable for feature class output name that can be used in the path by replacing the .shp with nothing
            file_name_new = "/proj/"+file_name_new+'_proj' #Send outputs to the proj folder by adding the file path /proj/ then add _proj to the end of each newly projected feature class
            arcpy.Project_management(fc,file_name_new, out_coordinate_system)#Project the feature classes to the coordinate system of the main shapefile and assign them new names in a different folder
