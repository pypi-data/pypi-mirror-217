import pandas as pd
from wordcloud import WordCloud
from nltk import FreqDist
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt


def return_vectorizer(grouped_text):
    """
    The function iterates over key-value pairs in a dictionary, initializes and fits CountVectorizer objects to reviews for each group, and stores the vectorizers in a dictionary.

    Parameters:
    - grouped_text: Dictionary of grouped text data.

    Returns:
    A vectorised list of each group.
    """
    vectorised_group = {}
    for key, reviews in grouped_text.items():
        vectorizer = CountVectorizer()
        vectorizer.fit_transform([reviews])
        vectorised_group[key] = vectorizer
    return vectorised_group


def return_dtm(vectorised_group, grouped_text):
    """
    This function creates a Document-Term Matrix (DTM) for each group using CountVectorizers.

    Parameters:
    - vectorised_group: A vectorised list of each group.
    - grouped_text: Dictionary of grouped text data.

    Returns:
    A dictionary containing Document-Term Matrices (DTMs) for each group.
    """
    dtm_by_group = {}
    for key, vectorizer in vectorised_group.items():
        dtm = vectorizer.transform([grouped_text[key]])
        dtm_by_group[key] = pd.DataFrame(dtm.toarray(), columns=vectorizer.get_feature_names_out())
    return dtm_by_group


def return_word_counts(dtm_by_group):
    """
    The function calculates the sum of word counts for each term in the Document-Term Matrices (DTMs).

    Parameters:
    - dtm_by_group: A  dictionary containing Document-Term Matrices (DTMs) for each group.

    Returns:
    A dictionary that contains the sum of word counts for each term in the Document-Term Matrices (DTMs).
    """
    word_counts_grouped = {}
    for key, dtm in dtm_by_group.items():
        word_counts = dtm.sum(axis=0)
        word_counts_grouped[key] = word_counts
    return word_counts_grouped


def return_sorted_words(word_counts_grouped):
    """
    Word counts are sorted in descending order for each group.

    Parameters:
    - word_counts_grouped: A dictionary that contains the sum of word counts for each term in the Document-Term Matrices (DTMs).

    Returns:
    A dictionary where the word counts for different groups are sorted in descending order. 
    """
    sorted_words_grouped = {}
    for key, word_counts in word_counts_grouped.items():
        sorted_words = word_counts.sort_values(ascending=False)
        sorted_words_grouped[key] = sorted_words
    return sorted_words_grouped


def create_sorted_words(grouped_text):
    """
    This function combines all the text within each group, vectorizes the text data, creates a Document-Term Matrix (DTM), and returns the word count.

    Parameters:
    - grouped_text: The df grouped by one or more columns. Example: grouped = df.groupby('columnName')['textColumn']

    Returns:
    A sorted list of words and their respective counts for each group.
    """
    grouped_text = grouped_text.apply(lambda x: ' '.join(x))
    vectorised_group = return_vectorizer(grouped_text)
    dtm_by_group = return_dtm(vectorised_group, grouped_text)
    word_counts_grouped = return_word_counts(dtm_by_group)
    return return_sorted_words(word_counts_grouped) 


# Create word clouds


def create_frequency_dictionary(sorted_words_grouped):
    """
    The function creates a list of frequency distributions for each key-value pair in a dictionary, where the values are sorted word counts.

    Parameters:
    - sorted_words_grouped: A sorted list of words and their respective counts for each group.

    Returns:
    A list of frequency distributions for each key-value pair in the input dictionary.
    """
    frequency_dictionary_list = []
    for key, item in sorted_words_grouped.items():
        entry = {key: FreqDist(sorted_words_grouped[key].to_dict())}
        frequency_dictionary_list.append(entry)
    return frequency_dictionary_list


def normalise_frequency_dictionary(frequency_dictionary_list):
    """
    The function takes a list of frequency dictionaries and normalizes the values within each dictionary.

    Parameters:
    - frequency_dictionary_list: A list of frequency distributions for each key-value pair in the input dictionary.

    Returns:
    A list of normalized dictionaries.    
    """
    normalised_dictionary_list = []
    for item in frequency_dictionary_list:
        origin_key = list(item.keys())[0]
        total = sum(item[origin_key].values())
        normalised_dictionary = {key: val / total for key, val in item[origin_key].items()}
        normalised_dictionary_list.append({origin_key: normalised_dictionary})
    return normalised_dictionary_list


def create_average_dictionary(normalised_dictionary_list):
    """
    The function iterates over a list of normalized dictionaries, extracts the keys from each dictionary into a "woordenboek".
    Including the averages for each word based on the accumulated counts and totals.

    Parameters:
    - normalised_dictionary_list: A list of normalized dictionaries.

    Returns:
    A dictionary containing the averages for each word.
    """
    word_counts = {}
    word_totals = {}

    for freq_list in normalised_dictionary_list:
        doc_freq = list(freq_list.values())[0]

        for word, value in doc_freq.items():
            # Accumulate the counts and totals for each word
            if word in word_counts:
                word_counts[word] += 1
                word_totals[word] += value
            else:
                word_counts[word] = 1
                word_totals[word] = value

    average_dictionary = {}

    # Calculate the averages for each word
    for word, count in word_counts.items():
        average = word_totals[word] / count
        average_dictionary[word] = average
        
    return average_dictionary


def create_count_differences(average_dictionary, normalised_dictionary_list, threshold=0.001):
    """
    The function calculates the highest value and its corresponding dictionary for each word in the "woordenboek".
    If the value of a word is smaller than the threshold, it adds the word and its highest value to the dictionary

    Parameters:
    - average_dictionary: A dictionary containing the averages for each word.
    - normalised_dictionary_list: A list of normalized dictionaries.
    - threshold: A limit on the frequency of words.

    Returns:
    The highest value of each word from the combined vocabulary, along with the corresponding group or category where the word appears most frequently.
    """
    count_differences = {}

    for word in average_dictionary:
        highest_value = float('-inf')
        dictionary_with_highest_value = None
        
        for item in normalised_dictionary_list:
            origin_key = list(item.keys())[0]
            value = item[origin_key].get(word, 0)

            if value > highest_value:
                highest_value = value
                dictionary_with_highest_value = origin_key
                
        if average_dictionary[word] < threshold:
            if dictionary_with_highest_value not in count_differences:
                count_differences[dictionary_with_highest_value] = {}
            count_differences[dictionary_with_highest_value][word] = highest_value
    return count_differences


def display_word_clouds(count_differences, save_jpg=False):
    """
    Create a unique wordcloud for each group.

    Parameters:
    - count_differences: The highest value of each word from the combined vocabulary, along with the corresponding group or category where the word appears most frequently.
    - save_jpg: If 'true' the images are saved to jpg's.

    Returns:
    Wordclouds
    """
    for group in sorted(count_differences):
        plot_wordcloud(count_differences, group, f'{group}.jpg', save_jpg)


def create_word_clouds(sorted_words, save_jpg=False, threshold=0.001):
    """
    Combines several functionalities to generate word clouds.

    Parameters:
    - sorted_words: The highest value of each word from the combined vocabulary, along with the corresponding group or category where the word appears most frequently.
    - save_jpg: If 'true' the images are saved to jpg's.
    - threshold: A limit on the frequency of words.

    Returns:
    Void
    """
    frequency_dictionary_list = create_frequency_dictionary(sorted_words)
    normalised_dictionary_list = normalise_frequency_dictionary(frequency_dictionary_list)
    average_dictionary = create_average_dictionary(normalised_dictionary_list)
    count_differences = create_count_differences(average_dictionary, normalised_dictionary_list, threshold)
    display_word_clouds(count_differences, save_jpg)


def plot_wordcloud(count_differences, group, image_name, save_jpg=False):
    """
    Generates and displays a word cloud based on the frequencies of words for a specific group.
    
    Parameters:
    - count_differences: The highest value of each word from the combined vocabulary, along with the corresponding group or category where the word appears most frequently.
    - group: A group the data was initially grouped by.
    - image_name: The name by which the image will be saved.
    - save_jpg: If 'true' the images are saved to jpg's.

    Returns:
    A wordcloud
    """
    plt.figure(figsize=(10, 10))

    wc = WordCloud(
        background_color="black",
        collocations=False,
        max_words=50,
        max_font_size=1500,
        min_font_size=20,
        width=1200,
        height=600,
        colormap=None,
    ).generate_from_frequencies(count_differences[group])
    
    plt.imshow(wc, interpolation='bilinear')
    plt.title(f"Wordcloud of {group}")
    plt.axis("off")
    
    if save_jpg:
        plt.savefig(f"wordclouds/{image_name}")

    plt.tight_layout(pad=1)
    plt.show()
