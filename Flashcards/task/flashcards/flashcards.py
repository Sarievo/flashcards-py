import argparse


class Cards:
    def __init__(self):
        self.cards = {}
        self.definitions = {}
        self.errors = {}
        self.log = []

    def log_print(self, s=""):
        print(s)
        self.log.append(s)

    def log_input(self, s):
        user_input = input(f"{s}\n")
        self.log.append(s)
        self.log.append(user_input)
        return user_input

    def add(self):
        term = self.log_input("The card:")
        while term in self.cards:
            term = self.log_input(f"The card \"{term}\" already exists. Try again:")
        definition = self.log_input("The definition for card:")
        while definition in self.definitions:
            definition = self.log_input(f"The definition \"{definition}\" already exists. Try again:")
        self.cards[term], self.definitions[definition] = definition, term
        self.log_print(f"The pair ({term}:{definition}) has been added.")

    def remove(self):
        term = self.log_input("Which card?")
        if term in self.cards:
            definition = self.cards[term]
            del self.cards[term]
            del self.definitions[definition]
            self.log_print("The card has been removed.")
        else:
            self.log_print(f"Can't remove \"{term}\": there is no such card.")

    def import_cards(self, path=None):
        file_path = self.log_input("File name:") if path is None else path
        try:
            with open(file_path, 'r') as file:
                for line in file.readlines():
                    term, definition = line.strip().split(':', maxsplit=1)
                    self.cards[term], self.definitions[definition] = definition, term
                self.log_print(f"{len(self.cards)} cards have been loaded.")
        except FileNotFoundError:
            self.log_print("File not found.")

    def export_cards(self, path=None):
        file_path = self.log_input("File name:") if path is None else path
        with open(file_path, "w", encoding="utf-8") as file:
            for term, definition in self.cards.items():
                file.write(f"{term}:{definition}\n")
            self.log_print(f"{len(self.cards)} cards have been saved.")

    def ask(self):
        n_times = int(self.log_input("How many times to ask?"))
        times = 0
        while times < n_times:
            for term, definition in self.cards.items():
                if times >= n_times:
                    break
                answer = self.log_input(f"Print the definition of \"{term}\"")
                if answer == definition:
                    self.log_print("Correct!")
                else:
                    if term in self.errors:
                        self.errors[term] += 1
                    else:
                        self.errors[term] = 1
                    self.log_print(f"Wrong. The right answer is \"{definition}\"" +
                                   (f", but your definition is correct for \"{self.definitions[answer]}\"."
                                    if answer in self.definitions else "."))
                times += 1

    def log_to_file(self):
        file_path = self.log_input("File name:")
        with open(file_path, "w", encoding="utf-8") as file:
            for line in self.log:
                file.write(f"{line}\n")
        self.log_print("The log has been saved.")

    def get_hardest(self):
        max_error = 0
        for term, err in self.errors.items():
            max_error = max(max_error, err)
        if max_error > 0:
            err_terms = []
            for term, err in self.errors.items():
                if err == max_error:
                    err_terms.append(term)
            if len(err_terms) == 1:
                self.log_print(f"The hardest card is \"{err_terms[0]}\". You have {max_error} errors answering it.")
            else:
                string = ", ".join(f"\"{term}\"" for term in err_terms)
                self.log_print(f"The hardest card is {string}. You have {max_error} errors answering them.")
        else:
            self.log_print("There are no cards with errors.")

    def reset_stats(self):
        self.errors = {}
        self.log_print("Card statistics have been reset.")


parser = argparse.ArgumentParser("Flashcards")
parser.add_argument("--import_from", default=False)
parser.add_argument("--export_to", default=False)
args = parser.parse_args()


cards = Cards()
if args.import_from:
    cards.import_cards(args.import_from)
while 1:
    action = cards.log_input(
        "Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):").strip().lower()
    if action == "add":
        cards.add()
    elif action == "remove":
        cards.remove()
    elif action == "import":
        cards.import_cards()
    elif action == "export":
        cards.export_cards()
    elif action == "ask":
        cards.ask()
    elif action == "exit":
        print("Bye bye")
        if args.export_to:
            cards.export_cards(args.export_to)
        break
    elif action == "log":
        cards.log_to_file()
    elif action == "hardest card":
        cards.get_hardest()
    elif action == "reset stats":
        cards.reset_stats()
    cards.log_print()
