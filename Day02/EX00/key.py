class Key:
    def __init__(self):
        self.passphrase = "zax2rulez"

    def __len__(self):
        return 1337

    def __getitem__(self, index):
        return 3

    def __gt__(self, other):
        return True

    def __str__(self):
        return "GeneralTsoKeycard"
