# Progress bar class. Easily copy this class or import it and have a progress
#   bar in your project!

# For a documentation, see my GitHub branch.

class ProgressBar():
    def __init__(self, width, min_amount=0, max_amount=99):
        self.width = width - 10
        self.step = min_amount
        self.max_amount = max_amount

    def draw (self):
        percentage = self.step / self.max_amount
        bar = " {:5.1f}% ".format(percentage * 100)
        bar += "["
        bar += "=" * (int(self.width * percentage))
        bar += " " * ((self.width - 1) - int(self.width * percentage))
        bar += "]"
        print(bar,end="\r")
        #print(" {:5.1f}% [".format(percentage * 100) + "=" * (int(self.width * percentage)) + " " * ((self.width - 1) - int(self.width * percentage)) + "]", end="\r")

    def update (self, amount=1):
        self.step += amount
        self.draw()

    def set (self, amount):
        self.step = amount
        self.draw()

    def end (self, clean=False,ending_character = "\n"):
        if clean:
            print(" " * (self.width + 10), end=ending_character)
        print("",end="\n")
