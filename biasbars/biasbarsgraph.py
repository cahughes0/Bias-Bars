import sys
import json
import matplotlib.pyplot as plt

LABELS = ["Low Reviews", "Medium Reviews", "High Reviews"]

WOMEN_KEY = "W"
MEN_KEY = "M"


def convert_rating_to_index(rating):
    """
    This function is complete. It is a helper function used to create the dictionary.
    """
    if rating < 2.5:
        return 0
    if 2.5 <= rating <= 3.5:
        return 1
    return 2


def add_data_for_word(word_data, word, gender, rating):
    """
    This function is complete. Updates the word_data dictionary to log an occurence of the
    specified word in a review with the given rating about a professor
    of the specified gender.

    Input:
        word_data (dictionary): dict holding word frequency data
        word (string): the word for which frequency data is being updated
        gender (string): the gender label for the specified comment in which
                         this word was seen
        rating (float): the numerical rating of the review in which this word
                         was seen
    """
    if word not in word_data:
        word_data[word] = {WOMEN_KEY: [0, 0, 0], MEN_KEY: [0, 0, 0]}

    inner_list_index = convert_rating_to_index(rating)
    word_data[word][gender][inner_list_index] += 1


def read_file(filename):
    """
    This function is complete. Reads the information from the specified file and builds a new
    word_data dictionary with the data found in the file. Returns the
    newly created dictionary.

    Input:
        word_data (dictionary): dictionary holding word frequency data
        filename (str): name of the file holding new professor review data
    """
    word_data = {}
    with open(filename, "r") as f:
        lines = f.readlines()
        lines = lines[1:]
        for line in lines:
            review_data = line.split(",")
            rating = float(review_data[0])
            gender_label = review_data[1]
            comment = review_data[2]
            words = comment.split()
            for word in words:
                add_data_for_word(word_data, word, gender_label, rating)
    return word_data


def plot_word(word_data, word, max_frequency):
    """
    This function takes in the word_data dictionary, the word, and the max_frequency.
    Your job is to use the dictionary and the word to plot the frequencies for this word
    use in low, medium, and high reviews for male and female professors.

    You do not need to use the max_frequency parameter. That is used in the provided code.
    """

    plot1 = plt.figure(1)
    # list of x values to use


    # we offset by a small amount so that the bars appear next to each other
    x_vals = [0, 1, 2]
    x_vals_women = [x - 0.2 for x in x_vals]
    x_vals_men = [x + 0.2 for x in x_vals]

    y_vals_women = [0, 0, 0]
    y_vals_men = [0, 0, 0]
    y_vals_women = word_data[word]['W']
    y_vals_men = word_data[word]['M']

    plt.title(word + ' in Professor Reviews')

    plt.bar(x_vals_women, y_vals_women, 0.4, label='Women')
    plt.bar(x_vals_men, y_vals_men, 0.4, label='Men')

    plt.ylim((0, max_frequency * 1.3))  # sets the maximum y value for the plot
    plt.xticks(x_vals, LABELS)  # sets the x values to be words for each review category
    plt.legend()
    plt.show()



def convert_counts_to_frequencies(word_data):
    """
    This function is complete. It converts a dictionary
    of word counts into a dictionary of word frequencies by
    dividing each count for a given gender by the total number
    of words found in reviews about professors of that gender.
    """
    K = 1000000
    total_words_men = sum([sum(counts[MEN_KEY]) for word, counts in word_data.items()])
    total_words_women = sum([sum(counts[WOMEN_KEY]) for word, counts in word_data.items()])
    for word in word_data:
        gender_data = word_data[word]
        for i in range(3):
            gender_data[MEN_KEY][i] *= K / total_words_men
            gender_data[WOMEN_KEY][i] *= K / total_words_women


def main():
    args = sys.argv[1:]
    word_data = read_file('full-data.txt')
    convert_counts_to_frequencies(word_data)
    word = args[0]
    print(word_data[word])
    gender_data = word_data[word]  # grab the inner dictionary
    max_frequency = max(max(gender_data['W']), max(gender_data['M']))
    plot_word(word_data, word, max_frequency)


if __name__ == "__main__":
    main()