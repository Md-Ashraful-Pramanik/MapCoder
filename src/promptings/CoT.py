from typing import List
import tiktoken
import os
from copy import deepcopy

from .Base import BaseStrategy
from models.Base import BaseModel

from results.Results import Results

from datasets.Dataset import Dataset
from datasets.APPSDataset import APPSDataset
from datasets.XCodeDataset import XCodeDataset
from datasets.HumanEvalDataset import HumanDataset
from datasets.CodeContestDataset import CodeContestDataset


class CoTStrategy(BaseStrategy):
    def run_single_pass(self, item: dict):
        prompt = None
        if type(self.data) == HumanDataset:
            prompt = """
def encrypt(s):
    '''
    Create a function encrypt that takes a string as an argument and
    returns a string encrypted with the alphabet being rotated. 
    The alphabet should be rotated in a manner such that the letters 
    shift down by two multiplied to two places.
    For example:
    encrypt('hi') returns 'lm'
    encrypt('asdfghjkl') returns 'ewhjklnop'
    encrypt('gf') returns 'kj'
    encrypt('et') returns 'ix'
    '''
    # Let's think step by step.

    # Define the alphabet as a string
    d = 'abcdefghijklmnopqrstuvwxyz'
    
    # Initialize an empty string to store the encrypted result
    out = ''
    
    # Iterate through each character in the input string
    for c in s:
        # Check if the character is a letter in the alphabet
        if c in d:
            # Find the index of the current letter in the alphabet
            index = d.index(c)
            
            # Rotate the alphabet by two multiplied to two places
            # Use modulo 26 to handle wrapping around the alphabet
            rotated_index = (index + 2 * 2) % 26
            
            # Append the encrypted letter to the result string
            out += d[rotated_index]
        else:
            # If the character is not a letter, append it unchanged to the result string
            out += c
    
    # Return the final encrypted string
    return out


-------

def check_if_last_char_is_a_letter(txt):
    ''' 
    Create a function that returns True if the last character of a given string is an alphabetical character and is not a part of a word, and False otherwise. Note: 'word' is a group of characters separated by space.
    Examples:
    check_if_last_char_is_a_letter('apple pie') → False
    check_if_last_char_is_a_letter('apple pi e') → True
    check_if_last_char_is_a_letter('apple pi e ') → False
    check_if_last_char_is_a_letter('') → False
    '''    
    # Let's think step by step.

    # Split the input string by space to get a list of words
    words = txt.split(' ')
    
    # Extract the last word from the list
    last_word = words[-1]
    
    # Check if the last character of the last word is an alphabetical character
    # and is not part of a longer word (length of last word is 1)
    is_last_char_letter = len(last_word) == 1 and (97 <= ord(last_word.lower()) <= 122)
    
    # Return True if the conditions are met, False otherwise
    return is_last_char_letter

-------

def file_name_check(file name):
    '''
    Create a function which takes a string representing a file's name, and returns 'Yes' if the the file's name is valid, and returns 'No' otherwise. A file's name is considered to be valid if and only if all the following conditions are met: - There should not be more than three digits ('0'-'9') in the file's name. - The file's name contains exactly one dot '.' - The substring before the dot should not be empty, and it starts with a letter from the latin alphapet ('a'-'z' and 'A'-'Z'). - The substring after the dot should be one of these: ['txt', 'exe', 'dll']
    Examples:
    file_name_check('example.txt') => 'Yes'
    file_name_check('1example.dll') => 'No' (the name should start with a latin alphapet letter)
    '''    
    # Let's think step by step.

    # Define a list of valid file extensions
    valid_suffixes = ['txt', 'exe', 'dll']
    
    # Split the file name into two parts using the dot as a separator
    parts = file_name.split(sep='.')
    
    # Check if there are exactly two parts after splitting
    if len(parts) != 2:
        return 'No'
    
    # Check if the second part (suffix) is in the list of valid suffixes
    if not parts[1] in valid_suffixes:
        return 'No'
    
    # Check if the first part (prefix) is not empty and starts with a letter from the Latin alphabet
    if len(parts[0]) == 0 or not parts[0][0].isalpha():
        return 'No'
    
    # Count the number of digits in the prefix and check if it's not more than three
    num_digits = len([x for x in parts[0] if x.isdigit()])
    if num_digits > 3:
        return 'No'
    
    # If all conditions are met, return 'Yes', indicating a valid file name
    return 'Yes'

-------

def fruit_distribution(s,n):
    '''
    In this task, you will be given a string that represents a number of apples and oranges that are distributed in a basket of fruit this basket contains apples, oranges, and mango fruits. Given the string that represents the total number of the oranges and apples and an integer that represent the total number of the fruits in the basket return the number of the mango fruits in the basket.
    for examble:
    fruit_distribution('5 apples and 6 oranges', 19) = 19 - 5 - 6 = 8
    fruit_distribution('0 apples and 1 oranges',3) = 3 - 0 - 1 = 2
    fruit_distribution('2 apples and 3 oranges', 100) = 100 - 2 - 3 = 95
    fruit_distribution('100 apples and 1 oranges',120) = 120 - 100 - 1 = 19
    '''
    # Let's think step by step.
    
    # Initialize an empty list to store the numeric values (apples and oranges) extracted from the string
    lis = list()

    # Split the input string by space and iterate through each word
    for i in s.split(' '):
        # Check if the word is a numeric value (digit)
        if i.isdigit():
            # Convert the numeric value to an integer and append it to the list
            lis.append(int(i))

    # Calculate the number of mango fruits by subtracting the sum of apples and oranges from the total
    return n - sum(lis)

-------

def prime_fib(n: int):
    '''
    prime_fib returns n-th number that is a Fibonacci number and it's also prime.
    Examples:
    >>> prime_fib(1) 2
    >>> prime_fib(2) 3
    >>> prime_fib(3) 5
    >>> prime_fib(4) 13
    >>> prime_fib(5) 89
    '''
    # Let's think step by step.

    # Import the math module for the square root function
    import math
    
    # Define a helper function to check if a number is prime
    def is_prime(p):
        if p < 2:
            return False
        for k in range(2, min(int(math.sqrt(p)) + 1, p - 1)):
            if p % k == 0:
                return False
        return True

    # Initialize the Fibonacci sequence with the first two numbers
    f = [0, 1]
    
    # Continue generating Fibonacci numbers until finding the n-th prime Fibonacci number
    while True:
        f.append(f[-1] + f[-2])
        
        # Check if the latest Fibonacci number is prime
        if is_prime(f[-1]):
            n -= 1
        
        # If the desired n-th prime Fibonacci number is found, return it
        if n == 0:
            return f[-1]

"""


        if type(self.data) == APPSDataset:
            prompt = """
An accordion is a string (yes, in the real world accordions are musical instruments, but let's forget about it for a while) which can be represented as a concatenation of: an opening bracket (ASCII code $091$), a colon (ASCII code $058$), some (possibly zero) vertical line characters (ASCII code $124$), another colon, and a closing bracket (ASCII code $093$). The length of the accordion is the number of characters in it.

For example, [::], [:||:] and [:|||:] are accordions having length $4$, $6$ and $7$. (:|:), {:||:}, [:], ]:||:[ are not accordions. 

You are given a string $s$. You want to transform it into an accordion by removing some (possibly zero) characters from it. Note that you may not insert new characters or reorder existing ones. Is it possible to obtain an accordion by removing characters from $s$, and if so, what is the maximum possible length of the result?


-----Input-----

The only line contains one string $s$ ($1 \le |s| \le 500000$). It consists of lowercase Latin letters and characters [, ], : and |.


-----Output-----

If it is not possible to obtain an accordion by removing some characters from $s$, print $-1$. Otherwise print maximum possible length of the resulting accordion.


-----Examples-----
Input
|[a:b:|]

Output
4

Input
|]:[|:]

Output
-1

2
1 2

## Let's think step by step and generate code to solve the problem.

```python
# Take user input and assign it to the variable 's'
s = input()

# Calculate the length of the string 's' and assign it to the variable 'n'
n = len(s)

# Initialize variables to store the indices of '[' and ']'
ind = -1
bind = -1

# Variable to track whether '[' or ']' characters have been encountered
f = False

# Step 1: Find the index of the first '[' character after encountering ':'
for i in range(n):
    if s[i] == '[':
        f = True
    elif s[i] == ':':
        if f:
            ind = i
            break

# Reset the flag variable
f = False

# Step 2: Find the index of the last ']' character before encountering ':'
for i in range(n - 1, -1, -1):
    if s[i] == ']':
        f = True
    elif s[i] == ':':
        if f:
            bind = i
            break

# Check conditions to determine if it's possible to obtain an accordion
if ind == -1 or bind == -1:
    # Print -1 if '[' or ']' characters were not found
    print(-1)
elif ind >= bind:
    # Print -1 if the order of '[' and ']' characters is incorrect
    print(-1)
else:
    # Initialize the length of the accordion to 4 (opening and closing brackets, and two colons)
    ans = 4
    # Step 3: Count the number of '|' characters between '[' and ']' indices (inclusive)
    for i in range(ind + 1, bind):
        if s[i] == '|':
            ans += 1
    # Print the calculated length of the resulting accordion
    print(ans)
```

-------

Anton has the integer x. He is interested what positive integer, which doesn't exceed x, has the maximum sum of digits.

Your task is to help Anton and to find the integer that interests him. If there are several such integers, determine the biggest of them. 


-----Input-----

The first line contains the positive integer x (1 ≤ x ≤ 10^18) — the integer which Anton has. 


-----Output-----

Print the positive integer which doesn't exceed x and has the maximum sum of digits. If there are several such integers, print the biggest of them. Printed integer must not contain leading zeros.


-----Examples-----
Input
100

Output
99

Input
48

Output
48

Input
521

Output
499

## Let's think step by step and generate code to solve the problem.

```python
# Take user input as a list of integers representing the digits of the given positive integer x
num = list(map(int, input()))

# Initialize a variable 'best' to store the current best candidate for the maximum sum of digits
best = num[:]

# Step 1: Iterate over the digits in reverse order
for i in range(-1, -len(num) - 1, -1):
    # If the current digit is 0, continue to the next digit
    if num[i] == 0:
        continue
    
    # Decrease the current digit by 1
    num[i] -= 1

    # Step 2: Set all digits to the right of the current digit to 9
    for j in range(i + 1, 0):
        num[j] = 9
    
    # Step 3: Compare the sum of the current number with the sum of the best number
    if sum(num) > sum(best):
        # Update 'best' if the current number has a greater sum
        best = num[:]

# Convert the list of digits to a string, remove leading zeros, and print the result
s = ''.join(map(str, best)).lstrip('0')
print(s)
```

-------

Apart from having lots of holidays throughout the year, residents of Berland also have whole lucky years. Year is considered lucky if it has no more than 1 non-zero digit in its number. So years 100, 40000, 5 are lucky and 12, 3001 and 12345 are not.

You are given current year in Berland. Your task is to find how long will residents of Berland wait till the next lucky year.


-----Input-----

The first line contains integer number n (1 ≤ n ≤ 10^9) — current year in Berland.


-----Output-----

Output amount of years from the current year to the next lucky one.


-----Examples-----
Input
4

Output
1

Input
201

Output
99

Input
4000

Output
1000



-----Note-----

In the first example next lucky year is 5. In the second one — 300. In the third — 5000.

## Let's think step by step and generate code to solve the problem.

```python
def main():
    # Take user input as a string representing the current year in Berland
    s = input()

    # Get the length of the input string (number of digits in the current year)
    n = len(s)

    # Step 1: Create a target lucky year 't' by incrementing the first digit by 1 and padding with zeros
    t = int(str(int(s[0]) + 1) + '0' * (n - 1))

    # Step 2: Calculate the number of years from the current year to the next lucky one
    result = t - int(s)

    # Print the result
    print(result)

# Call the main function
main()
```
"""
        

        if type(self.data) == XCodeDataset:
            prompt = """
Problem Description:
The Hat is a game of speedy explanation/guessing words (similar to Alias). It's fun. Try it! In this problem, we are talking about a variant of the game when the players are sitting at the table and everyone plays individually (i.e. not teams, but individual gamers play).$$$n$$$ people gathered in a room with $$$m$$$ tables ($$$n \ge 2m$$$). They want to play the Hat $$$k$$$ times. Thus, $$$k$$$ games will be played at each table. Each player will play in $$$k$$$ games.To do this, they are distributed among the tables for each game. During each game, one player plays at exactly one table. A player can play at different tables.Players want to have the most "fair" schedule of games. For this reason, they are looking for a schedule (table distribution for each game) such that:  At any table in each game there are either $$$\lfloor\frac{n}{m}\rfloor$$$ people or $$$\lceil\frac{n}{m}\rceil$$$ people (that is, either $$$n/m$$$ rounded down, or $$$n/m$$$ rounded up). Different numbers of people can play different games at the same table. Let's calculate for each player the value $$$b_i$$$ — the number of times the $$$i$$$-th player played at a table with $$$\lceil\frac{n}{m}\rceil$$$ persons ($$$n/m$$$ rounded up). Any two values of $$$b_i$$$must differ by no more than $$$1$$$. In other words, for any two players $$$i$$$ and $$$j$$$, it must be true $$$|b_i - b_j| \le 1$$$. For example, if $$$n=5$$$, $$$m=2$$$ and $$$k=2$$$, then at the request of the first item either two players or three players should play at each table. Consider the following schedules:  First game: $$$1, 2, 3$$$ are played at the first table, and $$$4, 5$$$ at the second one. The second game: at the first table they play $$$5, 1$$$, and at the second  — $$$2, 3, 4$$$. This schedule is not "fair" since $$$b_2=2$$$ (the second player played twice at a big table) and $$$b_5=0$$$ (the fifth player did not play at a big table). First game: $$$1, 2, 3$$$ are played at the first table, and $$$4, 5$$$ at the second one. The second game: at the first table they play $$$4, 5, 2$$$, and at the second one  — $$$1, 3$$$. This schedule is "fair": $$$b=[1,2,1,1,1]$$$ (any two values of $$$b_i$$$ differ by no more than $$$1$$$). Find any "fair" game schedule for $$$n$$$ people if they play on the $$$m$$$ tables of $$$k$$$ games.
Input Specification:
The first line of the input contains an integer $$$t$$$ ($$$1 \le t \le 10^4$$$) — the number of test cases in the test. Each test case consists of one line that contains three integers $$$n$$$, $$$m$$$ and $$$k$$$ ($$$2 \le n \le 2\cdot10^5$$$, $$$1 \le m \le \lfloor\frac{n}{2}\rfloor$$$, $$$1 \le k \le 10^5$$$) — the number of people, tables and games, respectively. It is guaranteed that the sum of $$$nk$$$ ($$$n$$$ multiplied by $$$k$$$) over all test cases does not exceed $$$2\cdot10^5$$$.
Output Specification:
For each test case print a required schedule  — a sequence of $$$k$$$ blocks of $$$m$$$ lines. Each block corresponds to one game, a line in a block corresponds to one table. In each line print the number of players at the table and the indices of the players (numbers from $$$1$$$ to $$$n$$$) who should play at this table. If there are several required schedules, then output any of them. We can show that a valid solution always exists. You can output additional blank lines to separate responses to different sets of inputs.
Sample Inputs: ['3\n5 2 2\n8 3 1\n2 1 3']
Sample Outputs: ['3 1 2 3\n2 4 5\n3 4 5 2\n2 1 3\n\n2 6 2\n3 3 5 1\n3 4 7 8\n\n2 2 1\n2 2 1\n2 2 1']
Note: 
Take input from: standard input
Give output to: standard output
Time Limit: 2 seconds
Memory Limit: 256 megabytes
Note: If you are writing a function then after the function definition take input from using `input()` function, call the function with specified parameters and finally print the output of the function.

## Let's think step by step and generate code to solve the problem.

```python
# Read the number of test cases
t = int(input())

# Iterate over each test case
for _ in range(t):
    # Read n, m, and k for the current test case
    n, m, k = map(int, input().split())
    
    # Initialize a list to store groups of players for each game
    groups = []
    
    # Initialize an array containing player indices
    arr = [(i + 1) for i in range(n)]
    
    z = 0
    
    # Check if the number of players is not divisible by the number of tables
    if n % m != 0:
        # Determine the size of the larger group
        larger = (n // m) + 1
        
        # Distribute players to larger groups until the number of players is divisible by the number of tables
        while n % m != 0:
            groups.append(larger)
            n -= larger
            m -= 1
            z += larger
    
    # Calculate the size of smaller groups
    a = n // m
    
    # Create groups with the calculated sizes
    for _ in range(m):
        groups.append(a)
    
    # Iterate over each game
    while k:
        curr = 0
        
        # Print the schedule for the current game
        for i in groups:
            print(i, end=" ")
            j = i
            
            # Print player indices for the current table
            while j:
                print(arr[curr], end=" ")
                curr += 1
                j -= 1
            
            print()
        
        # Rotate the array of player indices to simulate the rotation of players
        arr = arr[z:] + arr[:z]
        k -= 1
    
    # Print a blank line to separate responses for different sets of inputs
    print()

```
    
-------

Problem Description:
You are given a permutation $$$a_1,a_2,\ldots,a_n$$$ of integers from $$$0$$$ to $$$n - 1$$$. Your task is to find how many permutations $$$b_1,b_2,\ldots,b_n$$$ are similar to permutation $$$a$$$. Two permutations $$$a$$$ and $$$b$$$ of size $$$n$$$ are considered similar if for all intervals $$$[l,r]$$$ ($$$1 \le l \le r \le n$$$), the following condition is satisfied: $$$$$$\operatorname{MEX}([a_l,a_{l+1},\ldots,a_r])=\operatorname{MEX}([b_l,b_{l+1},\ldots,b_r]),$$$$$$ where the $$$\operatorname{MEX}$$$ of a collection of integers $$$c_1,c_2,\ldots,c_k$$$ is defined as the smallest non-negative integer $$$x$$$ which does not occur in collection $$$c$$$. For example, $$$\operatorname{MEX}([1,2,3,4,5])=0$$$, and $$$\operatorname{MEX}([0,1,2,4,5])=3$$$.Since the total number of such permutations can be very large, you will have to print its remainder modulo $$$10^9+7$$$.In this problem, a permutation of size $$$n$$$ is an array consisting of $$$n$$$ distinct integers from $$$0$$$ to $$$n-1$$$ in arbitrary order. For example, $$$[1,0,2,4,3]$$$ is a permutation, while $$$[0,1,1]$$$ is not, since $$$1$$$ appears twice in the array. $$$[0,1,3]$$$ is also not a permutation, since $$$n=3$$$ and there is a $$$3$$$ in the array.
Input Specification:
Each test contains multiple test cases. The first line of input contains one integer $$$t$$$ ($$$1 \le t \le 10^4$$$) — the number of test cases. The following lines contain the descriptions of the test cases. The first line of each test case contains a single integer $$$n$$$ ($$$1 \le n \le 10^5$$$) — the size of permutation $$$a$$$. The second line of each test case contains $$$n$$$ distinct integers $$$a_1,a_2,\ldots,a_n$$$ ($$$0 \le a_i \lt n$$$) — the elements of permutation $$$a$$$. It is guaranteed that the sum of $$$n$$$ across all test cases does not exceed $$$10^5$$$.
Output Specification:
For each test case, print a single integer, the number of permutations similar to permutation $$$a$$$, taken modulo $$$10^9+7$$$.
Sample Inputs: ['5\n\n5\n\n4 0 3 2 1\n\n1\n\n0\n\n4\n\n0 1 2 3\n\n6\n\n1 2 4 0 5 3\n\n8\n\n1 3 7 2 5 0 6 4']
Sample Outputs: ['2\n1\n1\n4\n72']
Note: NoteFor the first test case, the only permutations similar to $$$a=[4,0,3,2,1]$$$ are $$$[4,0,3,2,1]$$$ and $$$[4,0,2,3,1]$$$.For the second and third test cases, the given permutations are only similar to themselves.For the fourth test case, there are $$$4$$$ permutations similar to $$$a=[1,2,4,0,5,3]$$$:   $$$[1,2,4,0,5,3]$$$;  $$$[1,2,5,0,4,3]$$$;  $$$[1,4,2,0,5,3]$$$;  $$$[1,5,2,0,4,3]$$$. 
Take input from: standard input
Give output to: standard output
Time Limit: 1 second
Memory Limit: 256 megabytes
Note: If you are writing a function then after the function definition take input from using `input()` function, call the function with specified parameters and finally print the output of the function.

## Let's think step by step and generate code to solve the problem.

```python
# Iterate over each line of input starting from the third line (skipping the first two lines)
for s in [*open(0)][2::2]:
    r = 0  # Initialize a variable 'r' to store the maximum value of j
    k = 1  # Initialize a variable 'k' to store the result, initialized to 1
    
    # Iterate over pairs of elements and their indices, sorted by the element value
    for i, j in sorted(zip(map(int, a := s.split()), range(n := len(a)))):
        # Update 'k' based on conditions: (k, k * (r - n - i + 1) % (10**9+7))[n < j < r]
        k = (k, k * (r - n - i + 1) % (10**9+7))[n < j < r]
        n = min(n, j)  # Update 'n' to store the minimum index encountered so far
        r = max(r, j)  # Update 'r' to store the maximum index encountered so far
    
    # Print the final value of 'k' for the current test case
    print(k)

```

-------

Problem Description:
It is the hard version of the problem. The only difference is that in this version $$$1 \le n \le 300$$$.In the cinema seats can be represented as the table with $$$n$$$ rows and $$$m$$$ columns. The rows are numbered with integers from $$$1$$$ to $$$n$$$. The seats in each row are numbered with consecutive integers from left to right: in the $$$k$$$-th row from $$$m (k - 1) + 1$$$ to $$$m k$$$ for all rows $$$1 \le k \le n$$$. $$$1$$$$$$2$$$$$$\cdots$$$$$$m - 1$$$$$$m$$$$$$m + 1$$$$$$m + 2$$$$$$\cdots$$$$$$2 m - 1$$$$$$2 m$$$$$$2m + 1$$$$$$2m + 2$$$$$$\cdots$$$$$$3 m - 1$$$$$$3 m$$$$$$\vdots$$$$$$\vdots$$$$$$\ddots$$$$$$\vdots$$$$$$\vdots$$$$$$m (n - 1) + 1$$$$$$m (n - 1) + 2$$$$$$\cdots$$$$$$n m - 1$$$$$$n m$$$ The table with seats indices There are $$$nm$$$ people who want to go to the cinema to watch a new film. They are numbered with integers from $$$1$$$ to $$$nm$$$. You should give exactly one seat to each person.It is known, that in this cinema as lower seat index you have as better you can see everything happening on the screen. $$$i$$$-th person has the level of sight $$$a_i$$$. Let's define $$$s_i$$$ as the seat index, that will be given to $$$i$$$-th person. You want to give better places for people with lower sight levels, so for any two people $$$i$$$, $$$j$$$ such that $$$a_i &lt; a_j$$$ it should be satisfied that $$$s_i &lt; s_j$$$.After you will give seats to all people they will start coming to their seats. In the order from $$$1$$$ to $$$nm$$$, each person will enter the hall and sit in their seat. To get to their place, the person will go to their seat's row and start moving from the first seat in this row to theirs from left to right. While moving some places will be free, some will be occupied with people already seated. The inconvenience of the person is equal to the number of occupied seats he or she will go through.Let's consider an example: $$$m = 5$$$, the person has the seat $$$4$$$ in the first row, the seats $$$1$$$, $$$3$$$, $$$5$$$ in the first row are already occupied, the seats $$$2$$$ and $$$4$$$ are free. The inconvenience of this person will be $$$2$$$, because he will go through occupied seats $$$1$$$ and $$$3$$$.Find the minimal total inconvenience (the sum of inconveniences of all people), that is possible to have by giving places for all people (all conditions should be satisfied).
Input Specification:
The input consists of multiple test cases. The first line contains a single integer $$$t$$$ ($$$1 \le t \le 100$$$) — the number of test cases. Description of the test cases follows. The first line of each test case contains two integers $$$n$$$ and $$$m$$$ ($$$1 \le n, m \le 300$$$) — the number of rows and places in each row respectively. The second line of each test case contains $$$n \cdot m$$$ integers $$$a_1, a_2, \ldots, a_{n \cdot m}$$$ ($$$1 \le a_i \le 10^9$$$), where $$$a_i$$$ is the sight level of $$$i$$$-th person. It's guaranteed that the sum of $$$n \cdot m$$$ over all test cases does not exceed $$$10^5$$$.
Output Specification:
For each test case print a single integer — the minimal total inconvenience that can be achieved.
Sample Inputs: ['7\n1 2\n1 2\n3 2\n1 1 2 2 3 3\n3 3\n3 4 4 1 1 1 1 1 2\n2 2\n1 1 2 1\n4 2\n50 50 50 50 3 50 50 50\n4 2\n6 6 6 6 2 2 9 6\n2 9\n1 3 3 3 3 3 1 1 3 1 3 1 1 3 3 1 1 3']
Sample Outputs: ['1\n0\n4\n0\n0\n0\n1']
Note: NoteIn the first test case, there is a single way to give seats: the first person sits in the first place and the second person — in the second. The total inconvenience is $$$1$$$.In the second test case the optimal seating looks like this:   In the third test case the optimal seating looks like this:   The number in a cell is the person's index that sits on this place.
Take input from: standard input
Give output to: standard output
Time Limit: 1 second
Memory Limit: 256 megabytes
Note: If you are writing a function then after the function definition take input from using `input()` function, call the function with specified parameters and finally print the output of the function.

## Let's think step by step and generate code to solve the problem.

```python
import sys
from bisect import bisect_left
from collections import defaultdict as dd

# Redefine input function for convenience
input = lambda: sys.stdin.readline().rstrip()

def solve():
    ans = 0
    
    # Read input values for the current test case
    N, M = map(int, input().split())
    A = list(map(int, input().split()))
    Asort = sorted(A)

    # Create dictionaries to store column numbers, counts, and sets for efficient lookup
    colnum = dd(lambda: dd(lambda: -1))
    colnumcnt = dd(lambda: dd(lambda: 0))
    numcol = dd(set)
    
    # Populate dictionaries based on sorted sight levels
    for i in range(N):
        for j in range(M):
            a = Asort[M * i + j]
            colnum[i][a] = j
            numcol[a].add(i)
            colnumcnt[i][a] += 1

    # Initialize a list to represent occupied seats in each row
    q = [[] for _ in range(N)]
    
    # Iterate over sight levels to assign seats and calculate inconveniences
    for a in A:
        temp = sorted(numcol[a])
        for i in temp:
            if colnumcnt[i][a] <= 0:
                continue
            pos = bisect_left(q[i], a)
            ans += pos
            colnum[i][a] -= 1
            colnumcnt[i][a] -= 1
            if colnumcnt[i][a] == 0:
                numcol[a].remove(i)
            q[i].insert(pos, a)
            break   

    # Print the final result for the current test case
    print(ans)
    return

# Read the number of test cases
T = int(input())

# Iterate over each test case
for i in range(1, T + 1):
    solve()

```
"""


        if type(self.data) == CodeContestDataset:
            prompt = """
Three little pigs from all over the world are meeting for a convention! Every minute, a triple of 3 new pigs arrives on the convention floor. After the n-th minute, the convention ends.

The big bad wolf has learned about this convention, and he has an attack plan. At some minute in the convention, he will arrive and eat exactly x pigs. Then he will get away.

The wolf wants Gregor to help him figure out the number of possible attack plans that involve eating exactly x pigs for various values of x (1 ≤ x ≤ 3n). Two attack plans are considered different, if they occur at different times or if the sets of little pigs to eat are different.

Note that all queries are independent, that is, the wolf does not eat the little pigs, he only makes plans!

Input

The first line of input contains two integers n and q (1 ≤ n ≤ 10^6, 1 ≤ q ≤ 2⋅ 10^5), the number of minutes the convention lasts and the number of queries the wolf asks.

Each of the next q lines contains a single integer x_i (1 ≤ x_i ≤ 3n), the number of pigs the wolf will eat in the i-th query.

Output

You should print q lines, with line i representing the number of attack plans if the wolf wants to eat x_i pigs. Since each query answer can be large, output each answer modulo 10^9+7.

Examples

Input


2 3
1
5
6


Output


9
6
1


Input


5 4
2
4
6
8


Output


225
2001
6014
6939

Note

In the example test, n=2. Thus, there are 3 pigs at minute 1, and 6 pigs at minute 2. There are three queries: x=1, x=5, and x=6.

If the wolf wants to eat 1 pig, he can do so in 3+6=9 possible attack plans, depending on whether he arrives at minute 1 or 2.

If the wolf wants to eat 5 pigs, the wolf cannot arrive at minute 1, since there aren't enough pigs at that time. Therefore, the wolf has to arrive at minute 2, and there are 6 possible attack plans.

If the wolf wants to eat 6 pigs, his only plan is to arrive at the end of the convention and devour everybody.

Remember to output your answers modulo 10^9+7!

## Let's think step by step and generate code to solve the problem.

```python
def inverses(n, P):
    inv = [1] * (n + 1)
    for i in range(2, n + 1):
        inv[i] = inv[P % i] * (P - P // i) % P
    return inv

mod = 10**9 + 7

def init():
    fac[0] = ifac[0] = 1
    inv = inverses(N, mod)
    for i in range(1, N):
        fac[i] = (fac[i - 1] * i) % mod
        ifac[i] = (ifac[i - 1] * inv[i]) % mod

def comb(n, k):
    return (fac[n] * ifac[n - k] * ifac[k]) % mod

N = 3 * 10**6 + 10

fac = [0] * N
ifac = [0] * N

init()

def main():
    n, Q = map(int, input().split())
    sz = 3 * (n + 1)

    # Create a list to store coefficients of polynomial p(x)
    p = [0] * (sz + 1)

    # Initialize coefficients of p(x) using binomial coefficients
    for i in range(1, sz + 1):
        p[i] = comb(sz, i)

    # Backward iteration to calculate coefficients of p(x-1) and p(x-2)
    for i in range(sz, 2, -1):
        p[i - 1] = ((p[i - 1] - 3 * p[i]) % mod + mod) % mod
        p[i - 2] = ((p[i - 2] - 3 * p[i]) % mod + mod) % mod

    # Remove extra elements at the beginning of p
    p = p[3:]

    # Answer queries based on calculated coefficients
    for _ in range(Q):
        x = int(input())
        print(p[x])

# Call the main function
main()
```

-------

This is the easy version of the problem. The only difference from the hard version is that in this version all coordinates are even.

There are n fence-posts at distinct coordinates on a plane. It is guaranteed that no three fence posts lie on the same line.

There are an infinite number of cows on the plane, one at every point with integer coordinates.

Gregor is a member of the Illuminati, and wants to build a triangular fence, connecting 3 distinct existing fence posts. A cow strictly inside the fence is said to be enclosed. If there are an odd number of enclosed cows and the area of the fence is an integer, the fence is said to be interesting.

Find the number of interesting fences.

Input

The first line contains the integer n (3 ≤ n ≤ 6000), the number of fence posts which Gregor can choose to form the vertices of a fence.

Each of the next n line contains two integers x and y (0 ≤ x,y ≤ 10^7, x and y are even), where (x,y) is the coordinate of a fence post. All fence posts lie at distinct coordinates. No three fence posts are on the same line.

Output

Print a single integer, the number of interesting fences. Two fences are considered different if they are constructed with a different set of three fence posts.

Examples

Input


3
0 0
2 0
0 4


Output


1


Input


5
0 0
2 16
30 14
4 6
2 10


Output


3

Note

In the first example, there is only 1 fence. That fence is interesting since its area is 4 and there is 1 enclosed cow, marked in red.

In the second example, there are 3 interesting fences. 

  * (0,0) — (30,14) — (2,10) 
  * (2,16) — (30,14) — (2,10) 
  * (30,14) — (4,6) — (2,10) 

## Let's think step by step and generate code to solve the problem.

```python
def main():
    # Read the number of fence posts
    n = int(input())

    # Array to store the count of fence posts based on parity of coordinates
    cnt = [[0, 0], [0, 0]]

    # Loop to read the coordinates of each fence post
    for _ in range(n):
        x, y = map(int, input().split())

        # Divide coordinates by 2 to handle even coordinates
        x >>= 1
        y >>= 1

        # Update the count based on the parity of coordinates
        cnt[x & 1][y & 1] += 1

    # Variable to store the number of interesting fences
    ans = 0

    # Loop to iterate over all combinations of parity for x and y coordinates
    for i in range(2):
        for j in range(2):
            k = cnt[i][j]

            # Calculate the number of interesting fences using combinations
            ans += 1 * k * (k - 1) // 2 * (k - 2) // 3 + 1 * k * (k - 1) // 2 * (n - k)

    # Print the result
    print(ans)

# Call the main function
main()
```

-------

Gregor is learning about RSA cryptography, and although he doesn't understand how RSA works, he is now fascinated with prime numbers and factoring them.

Gregor's favorite prime number is P. Gregor wants to find two bases of P. Formally, Gregor is looking for two integers a and b which satisfy both of the following properties.

  * P mod a = P mod b, where x mod y denotes the remainder when x is divided by y, and 
  * 2 ≤ a < b ≤ P. 



Help Gregor find two bases of his favorite prime number!

Input

Each test contains multiple test cases. The first line contains the number of test cases t (1 ≤ t ≤ 1000).

Each subsequent line contains the integer P (5 ≤ P ≤ {10}^9), with P guaranteed to be prime.

Output

Your output should consist of t lines. Each line should consist of two integers a and b (2 ≤ a < b ≤ P). If there are multiple possible solutions, print any.

Example

Input


2
17
5


Output


3 5
2 4

Note

The first query is P=17. a=3 and b=5 are valid bases in this case, because 17 mod 3 = 17 mod 5 = 2. There are other pairs which work as well.

In the second query, with P=5, the only solution is a=2 and b=4.

## Let's think step by step and generate code to solve the problem.

def main():
    # Read the number of test cases
    t = int(input())

    # List to store prime numbers for each test case
    primes = [int(input()) for _ in range(t)]

    # Iterate over each test case to find bases
    for prime in primes:
        # Print bases a and b for each test case
        print(f"2 {prime - 1}")

# Call the main function
main()

"""
        
        
        input_for_planning = [
            {
                "role": "user",
                "content": f"{prompt}\n{self.data.get_prompt(item)}\n## Let's think step by step and generate {self.language} code to solve the problem.\n# ----------------\nImportant: Your response must contain only the {self.language} code to solve this problem inside ``` block.",
            },
        ]
        return self.gpt_chat(
            processed_input=input_for_planning
        )

