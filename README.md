# TOPSIS

TOPSIS (Technique for Order Preference by Similarity to Ideal Solution) is a multi-criteria decision-making method used to rank alternatives based on their closeness to the ideal solution. It evaluates options by comparing their distance from the best and worst possible values of each criterion. The alternative closest to the ideal and farthest from the negative ideal is ranked highest.

## Installation - USER MANUAL

Topsis-Pooja-102303845 requires Python3 to run.

**Other dependencies that come installed with this package are :-**
pandas
numpy

Package listed on PyPI:- (https://pypi.org/project/Topsis-Pooja-102303845/)\
Use the following command to install this package:-

```bash
pip install Topsis-Pooja-102303845
```

## Steps Involved in TOPSIS

- **Construct the Decision Matrix**  
  List all alternatives and their values for each criterion.

- **Normalize the Decision Matrix**  
  Convert different units into comparable, dimensionless values.

- **Apply Weights to Criteria**  
  Assign importance to each criterion based on its relevance.

- **Determine Ideal Solutions**
  - Positive Ideal Solution (best values)
  - Negative Ideal Solution (worst values)

- **Calculate Separation Measures**  
  Find the distance of each alternative from both ideal solutions.

- **Calculate Relative Closeness**  
  Compute a score that shows how close each alternative is to the ideal solution.

- **Rank the Alternatives**  
  Higher score → better rank.

## Usage

Run the following command in command prompt:

```bash
topsis <inputFile> <weights> <impacts> <outputFile>
```

Example:

```bash
topsis sample.csv "1,1,1,1" "+,+,-,+" result.csv
```

