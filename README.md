## Alex's work scripts
An assortment of random scripts that may/may not be useful in the future

# ultimate_parser.py
Probably the only useful thing in here --

Usage: ultimate_parser.py [-h] [-p] [-hd] [-c COLUMN] [-sa SORT_ASC]
                          [-sd SORT_DESC] [-o OUT_FILE] [-id IDEL] [-od ODEL]
                          input_file

GOAL: Parse anything and everything however you would like

positional arguments:
  input_file            File to be parsed.

optional arguments:
  -h, --help            show this help message and exit
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
