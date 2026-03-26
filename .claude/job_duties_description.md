I originally started as a data analyst on the customer operations team, but they really needed more than just an analyst. My first projects were building some data pipelines, KPI’s, and dashboards for the team. Then I started to do deeper investigative work into different parts of the business. These investigations would include a deep analysis and a presentation. We called this work “User Science”. Here are a couple examples:

- How we verify and pay our organizers - This covered how we verify our organizers and how we send our payouts. I found an easy way to lower the manual verifications by 50%, and discovered that we can flag checks that are being returned much earlier, and also that for large checks we can use a different option to make sure it arrives on time
- Customer Segmentation - I combined activity from all roles and did a density based clustering analysis to find what users are alike, and what makes a successful user. This found that the path of roles they take on the platform are strongly associated with their success
- Seller Discoverability - This was about digging deeper into how sellers bring buyers to their store. It showed:
    - over 15% of campaign views were outside the open campaign window, so these visitors were either too-early or too-late to purchase from the store for that event
    - Parents and family members often act as an untracked and un-supported user, trying to bring traffic to their kids store
    - Many people post on social media looking for an event to buy from, because they want to buy the popcorn but are unaware of an event going on that they can purchase from
    - Youth-related fundraisers have a lot of visitors to their store but a much lower conversion rate, resulting in less buyers

I also built a few machine learning projects including:
- k-means algorithm to classify VIP organizers who go straight to tier 3 customer support and get more personalized outreach. This is the only one that made it into production.
- a long-range forecasting model to predict monthly sales using Prophet and Sarima, and hierarchical reconciliation between state level and total aggregate level forecast
- Short-range model to predict the number of events upcoming by week, up to 4 weeks out. This used TSMixer and incorporated the event scheduling data at the time of that prediction

I also conduct strategic analyses including:
- Creating a Neo4j graph database to analyze the ancestor / descendant relationship between fundraisers - helping the company understand organic virality
- Causal effect of strategic outreach from the customer operations team. This used a propensity score matching model.
- Correlation between order processing time and order support tickets. This used weekly time series and non-parametric and non-linear correlations
- Root cause analysis into why sales had gone down

I also built some data pipelines in DBT. 

My current work duties are more focused in advanced statistics and are primarily the following:
- Experimentation 2.0 - The company’s experimentation has been very flawed. Everything from the design to the sampling and testing was unreliable and inaccurate. I put together a best practices framework for how the company should do testing. I am the resident statistics expert and advise on writing the correct hypothesis, choosing the right metrics, I run the power analyses, offer useful insights, and I will do the post experiment testing for further validation and heterogeneous effects. Our experiments are often randomized at the fundraiser level, meaning we often run clustered experiments. This means the post experiment modeling has to be a hierarchical model
- Semantic knowledge base - This started as necessary analysis prior to running a good experiment, but i have decided to repurpose this to be something that benefits in other areas. The company had not done any analysis on the distributions of metrics they want to test or confounders that they need to account for in sampling or testing. This project includes deeper analyses of key metrics like gross event sales, campaign sales, buyers per store, order value, and conversion rate. The analysis will include a review of the distribution and understanding if it needs to be transformed, bi-modal or multi-modal detection, key covariates, and causal drivers including the effect sizes or ranks of importance.
