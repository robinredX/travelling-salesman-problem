# antcolonyapproach.py

The function antcolonyapproach accepts filename (e.g. "data.txt") as input

## Installation Requirements

Python 3

### Usage

```python3
import antcolonyapproach
file = antcolonyapproach.antcolonyapproach("data.txt") # Replace data.txt with filename
file.algo()
```
### Note

The algorithm selects any random nodes as first since that is what required for Ant Colony Approach. 
I shall look into modifying this code to always start from node 1 soon.

Please remember that this code is not final yet. I need to lookinto Value Error problem. For now, I passed that error and it works fine, but it may not find very good solution because of it. I shall update it soon.
