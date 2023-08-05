# Wordiff
-----
Wordiff is designed to identify the most distinctive words when comparing text across different groups. Each word will only appear in one group's wordcloud. It generates unique word clouds for each group, enabling the exploration of the distinct words used in each group individually.

## Example
----
In the example provided below, a DataFrame is grouped by branch, and the review column is selected to identify the differences in words used across each branch. The words are sorted (and can be analyzed), generating a list of the most frequently used words for each group. This list is then utilized to create unique word clouds for each group, in this case, for each branch.

In this example, the word cloud images will not be saved (save_jpg = False), and the threshold is manually set. It is advisable to experiment with different threshold values, and it is recommended to create a column where all stopwords are removed for more accurate results.

```python
from wordiff import wordiff

grouped = df.groupby('Branch')['review']

sorted_words = wordiff.create_sorted_words(grouped)

wordiff.create_word_clouds(sorted_words, False, threshold=0.001)
```

## Installation
-----
If you have pip, you can download and install from the PyPI repository:
```
pip install wordiff
```

## Version
-----
0.0.1

## License
----
MIT

## Dependencies
-----
This package uses:
- pandas
- wordcloud: WordCloud
- nltk: FreqDist
- sklearn.feature_extraction.text: CountVectorizer
- atplotlib.pyplot: plt