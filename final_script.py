import arcpy
arcpy.env.workspace = "F:/Other/Final_Project/Data"

libraries = "LIBRARIES_PT.shp" #Choose any shapefile to be the main layer that everything will be projected to

library_spatial_ref = arcpy.Describe(libraries).spatialReference #create variable to easily extract spatial reference information from main shapefile

print library_spatial_ref.name #Check to see what projection the main file is using
print library_spatial_ref.factoryCode #Check which factory code corresponds to this projection
out_coordinate_system = arcpy.SpatialReference(library_spatial_ref.factoryCode) #assign variable to main file's projection to use when projecting the other feature classes

feature_classes = arcpy.ListFeatureClasses() #Create list of the feature classes that are in the Data folder
for fc in feature_classes: #Start for loop that runs through each feature class in the data folder
    spatial_ref = arcpy.Describe(fc).spatialReference #create variable to easily extract spatial reference info from any of the feature classes
    if fc != libraries: #Excludes the main shapefile libraries from the for loop 
        if spatial_ref.name == library_spatial_ref.name: #if the projection of the feature class is the same as that of the main file
            print fc, "has the same projection as Libraries" #print this statement           
        else:
            print spatial_ref.name #if it does not have the name projection, print what it does have
            file_name_new = fc.replace(".shp", "") #create variable for feature class output name that can be used in the path by replacing the .shp with nothing
            file_name_new = '/proj/'+file_name_new+'_proj' #send outputs to the proj folder by adding the file path /proj/ then add _proj to the end of each newly projected feature class
            print file_name_new #print to make sure it correctly changed the name
            arcpy.Project_management(fc,file_name_new, out_coordinate_system) #Project the feature classes to the coordinate system of the main shapefile and assign them new names in a different folder
