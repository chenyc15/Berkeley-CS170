"""
Mumbling Martians - CS170 programming project
Due 10/10
"""

def translate(d,s,t_d):
    """
    Returns a valid translation of s using words in d
    Breaks ties by shortest earliest word
    Runs in O(n^3)
    You don't need to worry about the t_d argument unless you're modifying transform_d
    >>> translate({"gork":"hello","bork":"world"},"gorkbork")
    "hello world"
    """
    #TODO: implement me!
    ...

def num_interpretations(d,s,t_d):
    """
    Returns the number of possible translations of s using words in d
    Runs in O(n^3)
    You don't need to worry about the t_d argument unless you're modifying transform_d
    >>> num_interpretations({"gork":"hello","g":"hi","ork":"friends"},"gork")
    2
    """
    #TODO: implement me!
    ...

def transform_d(d):
    """
    If you need to mutate d for any reason (probably only relevant for an O(n^2) solution),
    use this function instead of mucking around with the starter code
    Whatever is returned from this function will be passed in to translate
    and num_interpretations
    """
    return None

# you don't need to worry about anything below this line - it just parses input
# if your program is crashing somewhere here, it's likely the root cause is either
# in the way you called the program (is the file in your local directory and valid?)
# or originates somewhere in your code
# if not, please let us know on Piazza!
import sys
if len(sys.argv) != 4:
    print("USAGE: ./hw5.py INPUT_FILE OUTPUT_TRANSLATE_FILE OUTPUT_NUM_INTERPRETATIONS_FILE")
    exit(1)
input_file = sys.argv[1]
output_translate_file = sys.argv[2]
output_num_interpretations_file = sys.argv[3]
d = {}
queries = []
with open(input_file) as f:
    # first line gives us the number of elements in the dictionary
    n = int(f.readline())
    d = {}
    for _ in range(n):
        # each successive line is a space-separated dictionary element
        martian_word, english_word = f.readline().split(' ')
        d[martian_word] = english_word
    # the rest of the lines are queries
    for s in f:
        queries.append(s)
t_d = transform_d(d)
with open(output_translate_file,'w') as f:
    for query in queries:
        try:
            answer = translate(d,s,t_d)
            f.write(str(answer)+"\n")
        except Exception as err:
            print("translate had an error running on string {0} : {1}".format(query,err))
            exit(1)
with open(output_num_interpretations_file,'w') as f:
    for query in queries:
        try:
            answer = num_interpretations(d,s,t_d)
            f.write(str(answer)+"\n")
        except Exception as err:
            print("num_interpretations had an error running on string {0} : {1}".format(query, err))
            exit(1)
