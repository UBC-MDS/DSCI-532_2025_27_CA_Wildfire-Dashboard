<!-- TO BE UPDATED BASED ON COLLABORATIVE GOOGLE DOC: https://docs.google.com/document/d/15RFVEje4KcVk8RdTqWSU9hqasnSogVI98SqBVtU6uJw/edit?tab=t.0 
 -->
# PROJECT PROPOSAL
## Problem & Motivation structured
### Our role: Data scientist team

## Target Audience: - Fire management officer 

Wildfires are increasingly frequent and severe in California, causing massive environmental, economic, and human damage, costing billions and straining emergency resources. Understanding their causes and impacts is critical for developing prevention plans, aiding mitigation efforts, and improving disaster preparedness.  However, analyzing vast datasets is slow, time consuming and complex. This delays decision-making, hinders resource allocation, and limits the effectiveness of prevention and response efforts.
To address this, we propose a Wildfire Data Dashboard that allows Fire Management officers to explore wildfire data interactively. The dashboard will visualize key metrics like area burned, financial losses, and human impact, while enabling users to filter by location, date, and cause. The dashboard also allows export visualizations and summaries for stakeholders and policymakers. 
By identifying trends and hotspots, the dashboard will help allocate resources effectively, reduce wildfire frequency, increase response time and protect communities and ecosystems from the devastating impact of wildfires. 


## App sketch and description
![](img/sketch.png)
The app has a landing page that shows a heatmap superimposed on the map of California in the middle. The heatmap is based on the total finanical loss for that county due to wildfires, when the mouse hovers over it, the financial loss amount and count of the different damage categories for that county will show up. On the right of the map, there will be the total burned area and the number of total injuries and fatalities. Below the map there are 2 charts, the one on the left is a time series chart on the estimated financial loss over the years based on the different causes of the wildfire. On the right, it is a bar chart that shows the total count of homes, businesses, and vehicles that were damaged in the different counties. The filter menu is a pop out menu on the left. Using radio buttons, the user can filter to only include wildfire incidences of specific or all causes. Below it, using a sliding range, the year of the incident can also be filtered for. There are also two drop down menu for the user to filter for wildfires by county or by specific wildfire incident ID. All of those filter options will have an effect on all the graphs and summary statistics in the dashboard. Finally, there is an option to change the unit of financial loss to be based on Millions USD or Millions USD per acre, this setting will specifically influence the time series chart and the tooltip brush on the map only.