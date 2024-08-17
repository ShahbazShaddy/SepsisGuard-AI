import math
from collections import defaultdict

class BayesianFilter:
    def __init__(self):
        # Initialize word probabilities and class probabilities
        self.word_probs = defaultdict(lambda: {'Positive': 0, 'Negative': 0})
        self.class_probs = {'Positive': 0, 'Negative': 0}
        self.total_count = {'Positive': 0, 'Negative': 0}

    def train(self, text, label):
        """
        Train the Bayesian filter with labeled text.
        
        :param text: The text to train on
        :param label: The label ('Positive' or 'Negative')
        """
        words = text.split()
        self.class_probs[label] += 1
        for word in words:
            self.word_probs[word][label] += 1
            self.total_count[label] += 1

    def calculate_prob(self, text):
        """
        Calculate the probability that the text is 'Positive' or 'Negative'.
        
        :param text: The text to classify
        :return: The predicted label ('Positive' or 'Negative')
        """
        words = text.split()
        positive_prob = math.log(self.class_probs['Positive'])
        negative_prob = math.log(self.class_probs['Negative'])

        for word in words:
            positive_prob += math.log((self.word_probs[word]['Positive'] + 1) / (self.total_count['Positive'] + len(self.word_probs)))
            negative_prob += math.log((self.word_probs[word]['Negative'] + 1) / (self.total_count['Negative'] + len(self.word_probs)))

        return 'Positive' if positive_prob > negative_prob else 'Negative'
