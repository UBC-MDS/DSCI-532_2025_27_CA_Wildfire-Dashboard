<!-- TO BE UPDATED BASED ON COLLABORATIVE GOOGLE DOC: https://docs.google.com/document/d/15RFVEje4KcVk8RdTqWSU9hqasnSogVI98SqBVtU6uJw/edit?tab=t.0 
 -->
# PROJECT PROPOSAL
## Problem & Motivation structured
### Our role: Data scientist team

## Target Audience: - Fire management officer 

Wildfires are increasingly frequent and severe in California, causing massive environmental, economic, and human damage, costing billions and straining emergency resources. Understanding their causes and impacts is critical for developing prevention plans, aiding mitigation efforts, and improving disaster preparedness.  However, analyzing vast datasets is slow, time consuming and complex. This delays decision-making, hinders resource allocation, and limits the effectiveness of prevention and response efforts.
To address this, we propose a Wildfire Data Dashboard that allows Fire Management officers to explore wildfire data interactively. The dashboard will visualize key metrics like area burned, financial losses, and human impact, while enabling users to filter by location, date, and cause. The dashboard also allows export visualizations and summaries for stakeholders and policymakers. 
By identifying trends and hotspots, the dashboard will help allocate resources effectively, reduce wildfire frequency, increase response time and protect communities and ecosystems from the devastating impact of wildfires. 


## Description of Data

We will be visualizing a dataset containing 100 rows and 10 columns, representing data on wildfire incidents in California from 2014 to 2024. Each wildfire event is associated with multiple attributes related to its impact, human risk, and financial loss. By analyzing these variables, we aim to provide insights into wildfire severity, its contributing factors, and how its consequences have changed over time. Wildfires pose significant threats to communities, causing destruction to infrastructure, loss of lives, and financial burdens. 

Understanding wildfire patterns and their impact can help in:

-  Identifying the most damaging causes of wildfires.
-  Assessing financial loss trends over time.
-  Determining which wildfire causes are associated with the highest human risks.

Our dataset includes the following key variables that will aid in these analyses:

| **Category**                     | **Variables**                                         | **Description**                                                 |
|----------------------------------|------------------------------------------------------|-----------------------------------------------------------------|
| **Identification & Temporal Variables** | Date, Location                                   | When and where the wildfire occurred.                          |
| **Total Damage Variables**        | Area_Burned (Acres), Homes_Destroyed, Businesses_Destroyed, Vehicles_Damaged | The scale of destruction caused by the wildfire.               |
| **Human Risk Variables**          | Fatalities, Injuries                               | The number of people killed or injured.                        |
| **Financial Impact Variables**    | Estimated_Financial_Loss (Million $)              | The total economic loss due to the wildfire.                   |
| **Causal Variable**               | Cause                                            | The factor that led to the wildfire (for example, lightning, human activities). |

To enhance our analysis, we plan to derive the following new variables:

-  **Injuries-to-Fatalities Ratio** – By grouping wildfires based on their causes and calculating this ratio, we can compare the relative risk level of different wildfire causes (for example, whether lightning-induced fires are deadlier than human-caused fires).

-  **Estimated Financial Loss per Acre Burned** – This metric will help us evaluate if the financial cost of wildfires has increased over time and whether certain wildfire causes result in disproportionately higher economic losses.x

## Research Question
Dr. Daniel, a Fire Management Officer at the California Department of Forestry and Fire Protection is responsible for investigating wildfires,
 determining their root causes, estimating their damage, and designing mitigation strategies to reduce the environmental, financial, and human harm caused by wildfires in California.
 As Dr. Daniel is not necessarily an experienced data scientist, our app will help him easily analyze wildfire data and aid him in creating appropriate plans and policies to reduce the destruction caused by wildfires in California.

Dr. Daniel’s final goal is to reduce the harm caused by wildfires in California. He wants to find out what factors affect the frequency and magnitude of wildfires, so that he can adjust his policy and strategy updates accordingly.

He will open our app, review the data visualizations displayed, take notes on the insights he gleans from those visualizations, he will then use the filter function to dive deeper into the data.
 Then, he will adjust California’s wildfire mitigation policies and strategies according to the insights he gained from our dashboard. 
 For example, Dr. Daniel may impose restrictions on campfires in Riverside County during the summer because he notices a frequent increase of wildfires caused by human activity in that region during that period from looking at historical data on our dashboard.  


## App sketch and description
![Sketch of California wildfire dashboard](../img/sketch.png)
The app has a landing page that shows a heatmap superimposed on the map of California in the middle. The heatmap is based on the total finanical loss for that county due to wildfires, when the mouse hovers over it, the financial loss amount and count of the different damage categories for that county will show up. On the right of the map, there will be the total burned area and the number of total injuries and fatalities. Below the map there are 2 charts, the one on the left is a time series chart on the estimated financial loss over the years based on the different causes of the wildfire. On the right, it is a bar chart that shows the total count of homes, businesses, and vehicles that were damaged in the different counties. The filter menu is a pop out menu on the left. Using radio buttons, the user can filter to only include wildfire incidences of specific or all causes. Below it, using a sliding range, the year of the incident can also be filtered for. There are also two drop down menu for the user to filter for wildfires by county or by specific wildfire incident ID. All of those filter options will have an effect on all the graphs and summary statistics in the dashboard. Finally, there is an option to change the unit of financial loss to be based on Millions USD or Millions USD per acre, this setting will specifically influence the time series chart and the tooltip brush on the map only.