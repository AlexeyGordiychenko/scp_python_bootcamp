from user_input import user_input


class Measurements:
    """
    The purpose of this class is to gather and store measurements.
    """

    def __init__(self):
        """
        Initializes a new instance of the class with empty lists for
        respiration, heart rate, blushing level, and pupillary dilation.
        """
        self.respiration = []
        self.heart_rate = []
        self.blushing_level = []
        self.pupillary_dilation = []

    def measure(self):
        """
        Prompts a user for respiration, heart rate, blushing level, and
        pupillary dilation. Stores the values in the corresponding lists.
        """
        self.respiration.append(user_input(
            "Respiration (12-16 breaths per minute)", 12, 16))
        self.heart_rate.append(user_input(
            "Heart rate (60-100 beats per minute)", 60, 100))
        self.blushing_level.append(user_input(
            "Blushing level (1-6 levels)", 1, 6))
        self.pupillary_dilation.append(
            user_input("Pupillary dilation (2-8 mm)", 2, 8))
