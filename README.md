# GeoSearch


## Function

This is a package enable basic search for geo locations in the text, improved on geotext

The core class geoSearch takes a string, and return class.

locations = geoSearch(text, alpha)
  text is the target text
  alpha is between 0 and 1, and is to access how much of the database. The default alpha is 0.8, which means search the top 80% of geo locations in the database
 
 locations.countries, will return a list of all countries found in the text
 
 locations.locations, will return a list of all locations found in the text. If the locations is too specific, changing the alpha smaller will fix the problem. 
 
 locations.nationalities, will return a list of all nationalities found in the text

## Data

The data base of all geo location is collected by extract.py on geonames.org. The extract.py use a web parser to get top 5000 locations for each country. 

## Idea and future improvements

I came up with this package, because I couldn’t find a package doing similar things on the whole python library. 

The nltk tag works inconstantly, and always characterize normal noun as locations. 

The geotext package works fine, but interestingly it couldn’t detect the location, if the word before the location is capitalized. Also it could detect location with more tha two words, like New Zealand. 
