# Businesses-Recommendation-on-Maps-using-RRR

## An interactive map that could provide a recommended subset of businesses given the starting point and the range by users.

## Abstract
Selecting ideal businesses from a wide range of choices is a burdensome task for all users. It is practically infeasible for them to go through all these businesses, 
especially considering various kinds of attributes. Therefore, a reliable and flexible recommendation system would save huge amounts of time and provide better 
results for users. The idea of this project comes from the rank-regret representative notion. It is guaranteed to find a minimal subset of the data containing at least one of the top-k of any possible ranking function, which means all users’ requirements would be met. This project is made to show the feasibility of RRR used for 
recommendation. It is a html5 + Ajax + Django project, using leaflet written in html5 as the front end to provide an interactive map, Ajax to post the data to the 
backend, and Django to interact with the front map. It identifies a subset of businesses by looking for Rank-Regret Representative given the selected starting 
point and the distance range of businesses. Using the Yelp dataset for businesses, users could run this project where the starting point is in 11 covered metropolitan
areas. They get the returned subset in 5 seconds in most cases, and 20 seconds in extreme cases. The subset of recommended businesses is shown on the map using 
markers, and the detailed information is included in the popups of markers. 

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
What things you need to install the software and how to install them

## Running
Explain how to run the automated tests for this system

##Built with

##Authors

##Reference
[1] Asudeh A, Nazi A, Zhang N, et al. RRR: Rank-regret representative[C]//Proceedings of the 2019 International Conference on Management of Data. 2019: 263-280.
