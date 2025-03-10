# Milestone 3 - Reflection

## Original sketch of dashboard
![Sketch of California wildfire dashboard](../img/sketch.png)

## **Implemented Features**
- The interactive map is fully integrated, allowing seamless interaction.  
- Clicking a county filters all charts, supporting multi-county selection.  
- The Top 10 Counties by Economic Loss chart replaces the previous Top 5.  
- The Total Economic Loss summary card now renders correctly.  
- Hover-based tooltips show summary stats before filtering.  
- A loading indicator provides real-time feedback during updates.  
- The dashboard layout was improved with:  
  - A structured header, colored section titles, and a gray sidebar.  
  - Filters moved to a sidebar for a cleaner layout.  
  - A "Learn More!" button for additional guidance.  
  - A redesigned Total Economic Loss card for better emphasis.  
- All app files are properly organized.  
- **For Challenging Question**: We added a loading indicator for real-time feedback during updates, improving user experience and preventing confusion about lag. Inspired by Group 17’s design:(https://github.com/UBC-MDS/DSCI-532_2025_17_pharma_spend_dashboard).  

## **Features Not Implemented**
- Filtering by cause of fire was not implemented due to data limits, but we plan to add it to the map tooltip.  
- Financial loss display in Millions of USD or per Acre was not possible due to data constraints.  
- The total area burned summary card was replaced with total financial loss due to data limitations.    

-----------------------------------------------------------
## **Deviations from Proposal**
- Charts were initially non-interactive, requiring manual filtering. Click-based filtering on the map was added for easier selection, including multi-county filtering.  
- The dashboard layout was improved by placing related charts closer together for better readability.  
- A "Learn More" button was added for additional context.  
- The Total Economic Loss summary card was repositioned for better visibility.  
- A loading animation was added to improve user experience.  
- The year slider in the filters section is now more flexible. 
- The geospatial heatmap displays total fire count per county instead of financial loss.  


-----------------------------------------------------------
## **What the dashboard currently does well**
- Provides a clear visual summary of wildfire impact across California.  
- Supports multi-county comparisons through an interactive map, graphs, and filters.  
- Displays structure and roof type damage trends effectively.  
- Enhances user experience with tooltips, loading indicators, and a structured layout.  
- Allows users to compare wildfire damage by incident or by county.  
- Clearly highlights the most affected structure categories, roof types, and counties.  
- Visualizes economic loss trends, emphasizing financial damage over time.  
- Offers additional insights through the Learn More feature for deeper analysis.  

-----------------------------------------------------------
## **Current Limitations & Future Improvements**

### **Limitations**
- The "Structures Damaged by Category" chart height changes with county selection; a fixed height would ensure consistency.  
- The map tooltip struggled with category-based counts due to data inconsistencies and Plotly limitations.  
 

### **Future Enhancements**
- Refine visuals for better clarity and usability.  
- Improve optimization and interactivity.  
- Add two summary cards to balance the map area.  
- Explore better tooltip implementations for accuracy.  
