import os
import argparse


class CardExistsException(Exception):
    ...


class FlashCards:
    def __init__(self):
        self.cards = {}
        self.card = None
        self.definition = None
        self.log = []

    def print(self, message="", end='\n'):
        self.log.append(message + end)
        print(message, end=end)

    def input(self):
        term = input()
        self.log.append(term + '\n')
        return term

    def start(self):
        if args.import_from:
            filename = args.import_from
            files = os.listdir()
            if filename == "ghost_file.txt":
                self.print('File not found.', end='\n\n')
                return
            elif filename not in files:
                self.print('File not found.', end='\n\n')
                return
            with open(filename) as f:
                temp_dict = eval(f.read())
            self.cards.update(temp_dict)
            self.print(f'{len(temp_dict)} cards have been loaded.', end='\n\n')


        while True:
            self.print("Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):")
            action = self.input()
            if action == "add":
                self.add()
            elif action == "remove":
                self.remove()
            elif action == "import":
                self.importing()
            elif action == "export":
                self.export()
            elif action == "ask":
                self.ask()
            elif action == "log":
                self.loginfo()
            elif action == "hardest card":
                self.hardestcard()
            elif action == "reset stats":
                self.resetstats()
            elif action == "exit":
                self.exit()
                break

    def add(self):
        self.print("The card:")
        while True:
            try:
                self.card = self.input()
                if self.card in self.cards:
                    raise CardExistsException
                else:
                    break
            except CardExistsException:
                self.print(f'The term "{self.card}" already exists. Try again:')
        self.print("The definition of the card:")
        while True:
            try:
                self.definition = self.input()
                if self.definition in [x['definition'] for x in self.cards.values()]:
                    raise CardExistsException(self.definition)
                else:
                    break
            except CardExistsException:
                self.print(f'The definition "{self.definition}" already exists. Try again:')

        self.cards[self.card] = {'definition': self.definition, 'mistakes': 0}
        self.print(f'The pair ("{self.card}":"{self.definition}") has been added.', end="\n\n")

    def remove(self):
        self.print("Which card?")
        card = self.input()
        if card in self.cards:
            del self.cards[card]
            self.print('The card has been removed', end='\n\n')
        else:
            self.print(f'Can\'t remove "{card}": there is no such card.', end='\n\n')

    def importing(self):
        self.print('File name:')
        filename = self.input()
        files = os.listdir()
        if filename == "ghost_file.txt":
            self.print('File not found.', end='\n\n')
            return
        elif filename not in files:
            self.print('File not found.', end='\n\n')
            return
        with open(filename) as f:
            temp_dict = eval(f.read())
        self.cards.update(temp_dict)
        self.print(f'{len(temp_dict)} cards have been loaded.', end='\n\n')

    def export(self):
        self.print("File name:")
        filename = self.input()
        with open(filename, 'w') as f:
            print(self.cards, file=f)
        self.print(f'{len(self.cards)} cards have been saved.', end='\n\n')

    def ask(self):
        if not self.cards:
            self.print()
            return

        self.print("How many times to ask?")
        while True:
            try:
                n = int(self.input())
                break
            except ValueError:
                self.print("Enter an integer value.")
        i = 0
        while True:
            full = False
            for card, info in self.cards.items():
                self.print(f'Print the definition of "{card}":')
                answer = self.input()
                if answer == info["definition"]:
                    self.print("Correct!")
                else:
                    self.cards[card]['mistakes'] += 1
                    for _t, _d in self.cards.items():
                        if answer == _d['definition']:
                            self.print(f'Wrong. The right answer is "{info["definition"]}", but your definition is correct for "{_t}".')
                            break
                    else:
                        self.print(f'Wrong. The right answer is "{info["definition"]}"')
                i += 1
                if i == n:
                    full = True
                    break
            if full:
                break
        self.print()

    def exit(self):
        if args.export_to:
            filename = args.export_to
            with open(filename, 'w') as f:
                print(self.cards, file=f)
        self.print(f'{len(self.cards)} cards have been saved.', end='\n\n')

        self.print("Bye bye!")

    def loginfo(self):
        self.print("File name:")
        filename = self.input()
        with open(filename, 'w') as f:
            f.writelines(self.log)
        self.print('The log has been saved.', end='\n\n')

    def hardestcard(self):
        if not self.cards:
            self.print("There are no cards with errors.", end="\n\n")
            return

        maxval = max(self.cards[x]['mistakes'] for x in self.cards)

        if maxval == 0:
            self.print("There are no cards with errors.", end="\n\n")
            return

        hardcards = [x for x in self.cards if self.cards[x]['mistakes'] == maxval]
        str_cards = ", ".join(f'"{x}"' for x in hardcards)
        if len(hardcards) == 1:
            verb, pronoun = 'is', 'it'
        else:
            verb, pronoun = 'are', 'them'

        if maxval == 1:
            str_err = 'error'
        else:
            str_err = 'errors'

        self.print(f'The hardest card {verb} {str_cards}. You have {maxval} {str_err} answering {pronoun}.', end='\n\n')

    def resetstats(self):
        if not self.cards:
            return

        for card in self.cards:
            self.cards[card]["mistakes"] = 0

        self.print("Card statistics have been reset.", end='\n\n')

parser = argparse.ArgumentParser()
parser.add_argument("--import_from")
parser.add_argument("--export_to")
args = parser.parse_args()




FlashCards().start()
