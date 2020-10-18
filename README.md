## Inspiration
We were inspired by the rankings in the starter notebook of the challenge, but we wanted to go further. From the beginning, we decided to make a tool that would allow users to select the qualities that are the most important to them in selecting a city, and we wanted to include as much data on those cities as possible so our users could make their choices with the most information possible. We know that not everyone has the same preferences for what their looking for in their optimum city, so we employed a clustering algorithm to recommend users relevant cities based on their preferences. We also knew we wanted to host an amazingly awesome webtool with an easy to remember domain name (purchased from Domain.com) where users could input their priorities and find multiple cities matching their criteria, and SO MUCH MORE!

## What it does
We combined, census, weather, voting, economic, crime, weather and MORE data to provide users with the **most** robust data on all U.S cities with populations greater than 50,000 people, presented to the user in an easy to read format. 

A user of our service would go to [link](http://www.whereishould.live) and from there they'd use our simple interface and select their priorities in a city. Our written-from-scratch **clustering algorithm** determines the cities that best match their preferences.

Finally, each city is presented with maps, charts, and rankings so the user knows how their city sits in the categories they selected.

## How we built it

1. **Data Agregation** - We  synthesized a total of 8 datasets with the goal of generating a relevant subset of variables to consider when city shopping. We ended up generating a master dataset with 701 cities each with 59 attributes!
    -  [DP03 - Economic/Demographic Population Estimates](https://data.census.gov/cedsci/table?tid=ACSDP1Y2018.DP03&tp=false&hidePreview=true) 
    - [City/County Population Estimates](https://www.census.gov/data/datasets/time-series/demo/popest/2010s-total-cities-and-towns.html#ds)
    - [U.S Census Demographic Data](https://www.kaggle.com/muonneutrino/us-census-demographic-data?select=acs2017_census_tract_data.csv)
    - [U.S Violent Crime Dataset](https://ucr.fbi.gov/crime-in-the-u.s/2015/crime-in-the-u.s.-2015)
    - [Voter Share by County](https://github.com/MEDSL/2018-elections-unoffical/blob/master/election-context-2018.md)
    - [IRS Tax Data](https://www.irs.gov/statistics/soi-tax-stats-county-data)
    -	[Weather Data](https://www.ncdc.noaa.gov/cag/county/mapping)
    - [COVID-19 Data](https://github.com/nytimes/covid-19-data/blob/master/us-counties.csv)


2. **Clustering** - Based on user preferences, we wanted to be able to recommend cities with your desired characteristics. At first glance it might make sense to just recommend cities who's attributes fall within some interval. For example I could say I want to living in a city that has $70k income per capita and is very cold. From the get go, I am already limiting myself to cities that strictly meet these two characteristics! How can we move from limited search results to a richer collection of cities to suggest? The answer is K-Means! With the K-Means algorithm, we are able identify each city uniquely as a high dimensional vector (59-dim) and find clusters of cities in this richer space! These data was Z-transformed before being fed into a k-means++ clustering algorithm which gave us 100 clusters with about 5-20 cities per cluster. To determine what clusters should be used to make a user recommendation, we constructed 13 metrics using all of the data which allow us to measure more qualitative things like racial diversity and wealth. By asking the user for preferences across these 13 things with dropdown ranges, we were able to construct a feature vector for each user based on their custom preferences.  We calculated the inner product between the user's input and the feature vectors for each of the centroids identified by K-Means and suggested cities within these clusters. Note that we applied K-Means on our original 59-dimensional space, and then calculated the inner product with vectors in the subspace defined by span input features with the centroids in the higher dimensional vector space.

3. **Product** - With our data and clustering algorithm in hand, we now have the tools needed in order to create an effective recommendation tool. We decided to go with the Plotly/Dash/Heroku stack in order to host our web app because of the minimal overhead to get started. These packages support rich I/O and interactive functionality allowing for an immersive user experience. All a user has to do is fill out which data fields are important to them and based on that they will be shown cities that suit them!

## Challenges we ran into
Finding and processing the data was a challenge because we used many sources that didn’t always have data for the same places. We had to do some fuzzy matching between cities and counties to map county-level data to cities.

We also had some discussions around how (if at all) to preprocess the data before clustering it. Eventually we decided to give each column zero mean and unit variance, which improved the quality of our clusters. When it came to clustering, the written algorithm does work, but we went with sklearn.KMeans for performance purposes, however the written one gave us good data on how the clusters changed over each time step.

With respect to the web application we had some difficulty working as a team simultaneously with Microsoft Liveshare. 

## Accomplishments that we're proud of
We are proud of being able to put out such a large project in ~24 hours. It required bringing elements from many different stacks including data analysis, web development and tools like Excel.

We also tried to stay true to the values of a datathon, and this means that we made sure data took center stage. By doing this we were able to generate some pretty cool insights and confirmed some predictions of ours that made sense.

## What we learned
We learned how to clean and use large datasets, and how to design methods to use the information. We came up with quite a few recommender algorithms before we settled on the matrix factorization/k-means++ idea, which gave us the ability to prioritize a small number of features that a user could implement while also using all of them in the background to make clusters.

## What's next for whereishould.live
We would like to incorporate more of our data into various graphs and charts. This would give users even more comprehensive information on their city rankings.

We would also like to eventually include more cities, so that users have more choice than the ~700 that they have currently.

Most importantly — we would like to continue to improve the user experience in everything from latency to the style of the graphs to make sure that people have an enjoyable time using the site.
