# Anomaly Detection Project

## Motivations
The main reason I wanted to do this project so that my portfolio could have some evidence of my use of data. I wanted to show off my data collection, generation, and cleanup skills all while exploring the concept of anomaly detection, which I was new to.

## Summary of Project
After some initial research I decided to use a HuggingFace dataset that had come from a wiki scrape of League of Legends champions. I had to filter the data by parsing through it and use regular expressions to extract the useful stats, which in this case was health and armor of each of the champions. I wasn't particularly interested in too many stats, I just wanted to play around with scikit's Isolation Forest to see how it would capture my introduced anomalies.

I used Synthetic Data Vault's library to capture the metadata of the dataframe I was keeping my extracted data in to then synthesize a whole new batch based on the metadata of the original set. I altered 5% of the generated data by incrementing it by various values to introduce anomalies (ended up settling on 100 for loss of generality).

I used matplotlib's library to show the contamination of the data in conjunction with IsolationForest to see how well it could capture the anomalies given the correct contamination rate. However, it got me thinking about when a dataset is contaminated outside the scope of the user...

In any contaminated dataset, there's an issue regarding how to determine the extent to which the dataset was contaminated unless there's information on how the data was contaminated. Thus, experimenting with different data cleansing methods is vital to expanding one's skills enough to understand how to clean contaminated data well.

After seeing how the isolation forest acted on the data that definitely had anomalies, I wanted to experiment with different contamination rates on the original dataset. It ended up highlighting the outliers, and if this project were to be continued, perhaps we could link it back to the Champions those stats refer to and see their place in the meta. 

Of course, there are hundreds of more factors that would play into the strength of any particular champion. However this could show that if these stats were all encoded together and modeled, perhaps one could use something adjacent to an IsolationForest to discover the strongest champions to play...