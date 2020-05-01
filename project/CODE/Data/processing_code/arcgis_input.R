#Load libraries
##################################################
library(rgdal)
library(rgeos)
library(scales)
library(dplyr)

#Functions
##################################################
# function to load shapefile map as spatialpolygonsdataframe (with: simplification & transformation)
load_shapefile <- function(file, layer, validate=FALSE, transform=TRUE, simplify=NULL) {
  spdf <- readOGR(dsn=file, layer, verbose=FALSE)
  if (validate == TRUE) {
    message("Info: Validating shapefile geometry")
    gIsValid(spdf)
  }
  if (transform == TRUE) {
    message("Info: Transforming shapefile polygons to WGS84 coordinate reference system")
    spdf <- spTransform(spdf, CRS("+init=EPSG:4326"))
  }
  if (is.null(simplify) == FALSE) {
    message("Info: Simplifying shapefile polygons (tolerace=", simplify, ")")
    spdf <- SpatialPolygonsDataFrame(gSimplify(spgeom=spdf, tol=simplify, topologyPreserve=TRUE), data=spdf@data)
  }
  if (validate == TRUE) {
    message("Info: Validating topojson geometry")
    spdf <- repair_geometry(spdf)
  }
  return(spdf)
}

#Load inputs
##################################################
#Set path
directory <- "/Users/michaelpecorino/Documents/Machine_Learning/Data_Visual_Analytics/project/tl_2019_us_zcta510/tl_2019_us_zcta510.shp"
shapes_df <- load_shapefile(file = directory, layer = "tl_2019_us_zcta510", transform = TRUE, simplify = NULL)
predictions <- read.csv("/Users/michaelpecorino/Documents/Machine_Learning/Data_Visual_Analytics/project/Predictions_All_WithMissingSales.csv")

#Format columns for ArcGIS
##################################################
predictions$PercentChange <- round(predictions$PercentChange*100, 2)
predictions$UnemploymentRate <- paste0(predictions$UnemploymentRate, "%")
predictions$ZHVI <- dollar_format(big.mark = ",")(predictions$ZHVI)
predictions$PRED_PRICE <- dollar_format(big.mark = ",")(predictions$PRED_PRICE)

#Join model output to the shape file
##################################################
shapes_df <- merge(shapes_df, predictions[,c("ZIP",
                                             "ZHVI", "COASTAL_FLOOD_EVENTS_96_19", "DaysToSale", "UnemploymentRate",
                                             "PRED_PRICE", "PercentChange")], by.x = "ZCTA5CE10", by.y = "ZIP")
#Keep only relevant columns and zip codes
##################################################
shapes_df <- shapes_df[,c(1, 10:15)]
shapes_df <- shapes_df[!is.na(shapes_df$PRED_PRICE),]
shapes_df$zip_number <- as.numeric(as.character(shapes_df$ZCTA5CE10))

#Output
##################################################
writeOGR(shapes_df,
         "/Users/michaelpecorino/Documents/Machine_Learning/Data_Visual_Analytics/project/tl_2019_us_zcta510/",
         layer = "tl_2019_us_zcta510_2", "/Users/michaelpecorino/Documents/Machine_Learning/Data_Visual_Analytics/project/tl_2019_us_zcta510/shapes_df.shp",
         driver="ESRI Shapefile")
