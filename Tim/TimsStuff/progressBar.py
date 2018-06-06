# Progress bar class. Easily copy this class or import it and have a progress
#   bar in your project!

# For a documentation, see my GitHub branch.

class ProgressBar():
    # Init the class
    def __init__(self, width, min_amount=0, max_amount=99):
        self.width = width - 10
        self.step = min_amount
        self.max_amount = max_amount

    # Draw the progressbar
    def draw (self):
        percentage = self.step / self.max_amount
        bar = " {:5.1f}% ".format(percentage * 100)
        bar += "["
        bar += "=" * (int(self.width * percentage))
        bar += " " * ((self.width - 1) - int(self.width * percentage))
        bar += "]"
        print(bar,end="\r")
        if percentage >= 1:
            # We're done
            self.end()

    # Only update step with amount
    def update_only (self, amount=1):
        self.step += amount

    # Update step with amount and draw
    def update (self, amount=1):
        self.update_only(amount)
        self.draw()

    # Only sets step to amount
    def set_only (self, amount):
        self.step = amount

    # Sets step to amount and draws
    def set (self, amount):
        self.set_only(amount)
        self.draw()

    # End the program
    def end (self, clean=False, ending_character = "\n"):
        if clean:
            print(" " * (self.width + 10),end="\r")
        print("",end=ending_character)
