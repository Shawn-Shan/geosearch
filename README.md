# GeoSearch


## Function

This is a package enable basic search for geo locations in the text, improved on geotext

The core function search_region takes a string, and return a list of all geo locations in the text. 

## Data

The data base of all geo location is collected by region.py on geonames.org. 

## Idea and future improvements

I came up with this package, because I couldn’t find a package doing similar things on the whole python library. 

The nltk tag works inconstantly, and always characterize normal noun as locations. 

The geotext package works fine, but interestingly it couldn’t detect the location, if the word before the location is capitalized. Also it could detect location with more tha two words, like New Zealand. 
