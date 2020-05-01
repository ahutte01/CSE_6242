DESCRIPTION
Our visualization takes a variety of flood and property data sources and visualizes them in ArcGIS in addition to the predictions from our model.
Our file package includes the following:
1. DOC/team93report.pdf: Final Report pdf
2. CODE/map.html: HTML file of our mapping visualization
3. CODE/PricingFloodRiskByZip.ipynb: Jupyter notebook containing our modeling work
4. CODE/Data: Data folder containing necessary data for modeling and for the visualization
5. CODE/Data/processing_code: Data processing code for the NOAA storm events data and for attaching the predictions to the zip code shapefiles
6. CODE/Data/processing_code/arcgis_input.R: Ingests zip code shapefiles from Tiger Lines and appends our price predictions. Outputs new shapefiles with predictions appended which is used in our visualization.
7. CODE/Data/processing_code/NOAA Storm Data Processing.ipynb: Takes NOAA storm events csv files from 1996-2019 and aggregates coastal flood events to the county-level.

INSTALLATION
To view and interact with the visualization:
1. Place the html file in a local folder of your choice.
2. Right click the file and choose “Open With” any internet browser. We have verified that our file works on Firefox, Chrome, Safari, and Internet Explorer, but one of our users during testing had an issue with a browser version in which they could not see any of our map layers. Please try multiple browsers if you encounter a similar situation.

To run the modeling code:
1. Open up the jupyter notebook.
2. Click Kernel in the ribbon and then click "Restart Kernel and Run All Cells." 
3. You can view our data work and full modeling results in each cell's output.

EXECUTION
Once the html file is open in the browser, the user is in our application.
The application has 2 features for interactivity:
1. Clicking the zip code heat map (in red) or the FEMA flood zone heat map (in purple) to activate the popup messages.
2. Toggling the layers described in item #1 on or off using the check boxes provided at the top of the page.
