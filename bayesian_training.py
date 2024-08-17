from bayesian_filter import BayesianFilter

def train_bayesian_filter():
    """
    Train the Bayesian filter with data related to sepsis detection.
    :return: Trained BayesianFilter object
    """
    bayesian_filter = BayesianFilter()

    # Train the filter with comprehensive data
    bayesian_filter.train("SEPSIS ALERT. Strongly recommend early intervention.", "Positive")
    bayesian_filter.train("Patient has a high temperature and fast heart rate. Recommend seeking immediate medical attention.", "Positive")
    bayesian_filter.train("Elevated temperature is the primary trigger for this alert. Advise to go to the emergency department.", "Positive")
    bayesian_filter.train("No signs of sepsis. Patient's vital signs are within normal range.", "Negative")
    bayesian_filter.train("No intervention needed. Patient is stable.", "Negative")
    bayesian_filter.train("Normal temperature, heart rate, and respiratory rate. No sepsis alert triggered.", "Negative")

    return bayesian_filter
