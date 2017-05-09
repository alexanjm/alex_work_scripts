## Alex's work scripts
An assortment of random scripts that may/may not be useful in the future

### ultimate_parser.py
Probably the only useful thing in here --

#### Usage: 
ultimate_parser.py [-h] [-p] [-hd] [-c COLUMN] [-sa SORT_ASC]
                          [-sd SORT_DESC] [-o OUT_FILE] [-id IDEL] [-od ODEL]
                          input_file

GOAL: Parse anything and everything however you would like


| Arguments |    Input Type     | Description                                       |
| ----------|:-----------------:| -------------------------------------------------:|
| -h        |                   | help menu                                         |
| -p        |                   | convert delimiters ("," "\t" or custom delimiters)|
| -c        | < int,int(...) >  | keep certain columns                              |
| -sa       | < int >           | Sort ascending by a certain column #              |
| -sd       | < int >           | Sort descending by a certain column #             |
| -hd       |                   | is a header present? (Needed for sort)            |
| -o        | < filename.txt >  | Name of output file                               |
| -id       | < string >        | Custom input delimiter                            |
| -od       | < string >        | Custom output delimiter                           |


