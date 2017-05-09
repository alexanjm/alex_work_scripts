## Alex's work scripts
An assortment of random scripts that may/may not be useful in the future

### ultimate_parser.py
Probably the only useful thing in here --

#### Usage: 
ultimate_parser.py [-h] [-p] [-hd] [-c COLUMN] [-sa SORT_ASC]
                          [-sd SORT_DESC] [-o OUT_FILE] [-id IDEL] [-od ODEL]
                          input_file

GOAL: Parse anything and everything however you would like

positional arguments:
  input_file            File to be parsed.

optional arguments:
  -h, --help\tshow this help message and exit
  -p, --parse           Convert files to comma separated, tab separated or
                        even custom delimiters. Default = False
  -hd, --header         <-hd> File contains a header?. Default = False.
  -c COLUMN, --column COLUMN
                        <int,int(...)> Column numbers to output.
  -sa SORT_ASC, --sort_asc SORT_ASC
                        <int> Sort column in ascending order by this column
                        number.
  -sd SORT_DESC, --sort_desc SORT_DESC
                        <int> Sort column in descending order by this column
                        number.
  -o OUT_FILE, --out_file OUT_FILE
                        Output file location.
  -id IDEL, --idel IDEL
                        <str> Custom input delimiter.
  -od ODEL, --odel ODEL
                        <str> Custom output delimiter.

Colons can be used to align columns.

| Tables        | Are           | Cool  |
| ------------- |:-------------:| -----:|
| col 3 is      | right-aligned | $1600 |
| col 2 is      | centered      |   $12 |
| zebra stripes | are neat      |    $1 |

There must be at least 3 dashes separating each header cell.
The outer pipes (|) are optional, and you don't need to make the 
raw Markdown line up prettily. You can also use inline Markdown.
