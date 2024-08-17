from bayesian_filter import BayesianFilter

def train_bayesian_filter():
    """
    Train the Bayesian filter with data related to sepsis detection.
    :return: Trained BayesianFilter object
    """
    bayesian_filter = BayesianFilter()

    # Train the filter with comprehensive data
    # Positive Cases
    bayesian_filter.train("**SEPSIS ALERT**", "Positive")
    bayesian_filter.train("the patient meets one criterion for sepsis", "Positive")
    bayesian_filter.train("Strongly recommend immediate medical intervention to address potential sepsis", "Positive")
    bayesian_filter.train("Patient presents with a significantly high heart rate and fever. Immediate sepsis evaluation required.", "Positive")
    bayesian_filter.train("Temperature exceeds 39 °C, combined with an elevated WBC count. Urgent medical assessment advised.", "Positive")
    bayesian_filter.train("Patient's respiratory rate is high along with an abnormal WBC count. Strongly recommend sepsis screening.", "Positive")
    bayesian_filter.train("The patient's vital signs indicate a severe infection risk. Immediate medical attention is necessary.", "Positive")
    bayesian_filter.train("Patient's WBC count is critically high. Immediate medical intervention is required.", "Positive")
    bayesian_filter.train("Patient shows multiple signs of sepsis. Urgent medical attention is needed.", "Positive")
    bayesian_filter.train("Patient's vital signs indicate a potential sepsis risk. Recommend immediate evaluation.", "Positive")
    bayesian_filter.train("Patient’s temperature is just above the normal threshold. Monitor closely for sepsis symptoms.", "Positive")
    bayesian_filter.train("Heart rate is slightly above the normal range, indicating a potential risk for sepsis. Further evaluation needed.", "Positive")
    
    # Negative Cases
    bayesian_filter.train("does not meet any of the criteria for sepsis", "Negative")
    bayesian_filter.train("SEPSIS ALERT. Strongly recommend early intervention.", "Positive")
    bayesian_filter.train("No signs of sepsis. Patient's vital signs are within normal range.", "Negative")
    bayesian_filter.train("No intervention needed. Patient is stable.", "Negative")
    bayesian_filter.train("Normal temperature, heart rate, and respiratory rate. No sepsis alert triggered.", "Negative")
    bayesian_filter.train("Patient's heart rate and temperature are within normal limits. No sepsis alert.", "Negative")
    bayesian_filter.train("Patient's respiratory rate is elevated. Recommend further monitoring for sepsis.", "Positive")
    bayesian_filter.train("Patient's WBC count is within normal range. No sepsis detected.", "Negative")
    bayesian_filter.train("Patient’s temperature, heart rate, and WBC count are all within normal ranges. No sepsis risk detected.", "Negative")
    bayesian_filter.train("Vital signs are stable and do not meet sepsis criteria. No immediate intervention needed.", "Negative")
    bayesian_filter.train("Temperature is slightly elevated but not above the sepsis threshold. Continue to monitor.", "Negative")
    bayesian_filter.train("Heart rate is just below the sepsis threshold. No sepsis alert required at this time.", "Negative")
    bayesian_filter.train("Patient with a known fever due to an ongoing non-infectious condition. No sepsis risk identified.", "Negative")
    bayesian_filter.train("Chronic respiratory issues causing elevated respiratory rate. No signs of sepsis present.", "Negative")
    bayesian_filter.train("Patient has a chronic condition affecting WBC count. Current levels do not indicate sepsis.", "Negative")

    return bayesian_filter
