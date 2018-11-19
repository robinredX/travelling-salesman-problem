# antcolonyapproach.py

The function antcolonyapproach accepts filename (e.g. "data.txt") as input

## Installation Requirements

Python 3

### Usage

```python3
import antcolonyapproach
file = antcolonyapproach.antcolonyapproach("data.txt") # Replace data.txt with filename
file.algo() # run file
```
### Note

The algorithm selects any random node as first node of Optimal Tour since that is what required for Ant Colony Approach to find optimal solution. But I shall look into modifying this soon.
Please remember that this code is not final yet. I need to look into the Value Error and ZeroDivisonError problem. For now, I passed these errors and the programme fine. However, it may not find very good solution because of this adjustment. I shall update it soon.
