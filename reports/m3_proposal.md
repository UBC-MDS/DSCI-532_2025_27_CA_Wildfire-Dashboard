# Milestone 3 - Reflection

## Original sketch of dashboard
![Sketch of California wildfire dashboard](../img/sketch.png)

## **Implemented Features**
- The interactive map is now fully integrated with the app file, ensuring seamless interaction.  
- Clicking on a county on the map filters all other charts, supporting multi-county selection for comparative analysis.  
- The Top 10 Counties by Economic Loss chart has been expanded from the previous top 5 counties, providing a more comprehensive view of financial losses over time.  
- The Total Economic Loss summary card now renders perfectly and consistently displays "Total Economic Loss."  
- Hover-based tooltips have been added to the map, displaying summary statistics before clicking to filter.  
- A loading indicator for charts has been implemented, providing real-time feedback to users while the charts are updating.  
- The dashboard layout has been revamped with several enhancements:  
  - Enhanced visuals now include a structured orange header, colored section titles, and a gray sidebar, improving readability while incorporating all four charts inside a card layout.  
  - Filters have been moved to a sidebar, creating a cleaner and more intuitive layout.  
  - A "Learn More!" button has been added to guide users and provide additional information.  
  - The Total Economic Loss card has been redesigned for improved emphasis and readability. 
- All the files for the app are stacked according to the guidelines provided.
- **For Challenging Question**: We implemented a loading indicator as well for charts to provide real-time feedback while they are being generated or updated. This feature enhances the user experience, especially for those with slower computers or using the rendered app, where chart updates may take time due to filtering processes. By displaying a loading animation, users are assured that their input has been received and the dashboard is actively processing their request, preventing confusion about potential system lag or unresponsiveness. Our team drew inspiration for this feature from Group 17’s dashboard design, which can be found at this link- https://github.com/UBC-MDS/DSCI-532_2025_17_pharma_spend_dashboard


## **Features Not Implemented**
- Filter by cause of fire was not implemented due to data limitations.
- Option to display financial loss in Millions of USD or Millions of USD per Acre, also due to data limitations.
- Summary card for total area burned is replaced with summary card of total financial loss, also due to data limitations. 

-----------------------------------------------------------
## **Deviations from Proposal**
The dataset initially proposed in our original proposal was found to be synthetic. Consequently, we sourced an alternative dataset from the California Fire Department directly. Due to differences in data structure and available features, some originally planned implementations were not feasible. We adjusted our dashboard accordingly to align with the newly acquired dataset. The deviations are as followed:
- Filter by cause of fire was not implemented because the dataset only has that information for 10% of the reported fire incidences
- Total burned acreage was no longer available, therefore the summary card for total area burned is replaced with summary card of total financial loss. Additionally, it was not possible to implement the option to display financial loss in Millions of USD or Millions of USD per Acre either.
- The number of fatalties and injuries were not available in the new dataset. Instead, we utilized the information on what the damage category was instead.
- We had additional information on roof types in the new dataset. Hence we added an additional bar chart to reflect how the houses with different roof types have different distribution of damage levels.
- The geospatial heatmap represents the total number of fires in each county rather than the financial loss. When hovering over a county, it displays the total fire count instead of the financial loss amount or the count of different damage categories. 



-----------------------------------------------------------
## **What the dashboard currently does well**
- Gives a clear visual summary of wildfire impact across California. 
- Allows multi-county comparisons using an interactive map, graphs and filtering. 
- Displays structure and roof type damage trends.
- Enhances user experience with tooltips, loading indicators, and a structured layout.  
- Lets you see and compare the damage caused by each incident, or compare how much damage each county has suffered.
- It clearly showcases which structure categories, roof types and counties are most affected by wildfires.
- Visualizes economic loss trends and highlights financial damage over time.
- Offers additional insights with the "Learn More" feature for deeper analysis.

-----------------------------------------------------------
## **Current Limitations & Future Improvements**

### **Limitations**
- The height of the "Structures Damaged by Category in Top 10 Most Affected Counties" bar chart changes when selecting different numbers of counties. To ensure a consistent layout, consider setting a fixed height for this chart.


### **Future Enhancements**

- We aim to fine-tune visual elements, making the dashboard more intuitive and user-friendly.
- We aim to work on optimization and interactivity of app at advanced level
