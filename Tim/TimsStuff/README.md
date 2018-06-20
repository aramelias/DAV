# TimsStuff Library
The TimsStuff Library is a place for common function that everyone can use. You
can simply add this map to the folder you want to export it with, and then import it.

## Setup
As said, you have to have the map in an accessible location for your script. The easiest way to do this is to simply place it in the same directory. Then, you can import it using:
```
import TimsStuff.<filename>
```
Replace filename by the name of the file you want to import from (excluding .py). You can also import a specific function in a file, like so:
```
from TimsStuff.<filename> import <class>
```

## The files
The TimsStuff Library contains many useful classes and functions. So far, these are them:

### progressBar.py
This file contains an easy to use progressbar, so you can easily show progress of your script. Import it using:
```
from TimsStuff.progressBar import ProgressBar
```
Then, you are ready to use it in your program. But first, you'll have to init it:
```
progress_bar = ProgressBar()
```
*Optional arguments:*  
`width=terminal_width`: The **total** width of your progress bar, including percentage and eventual preceding text. By default, this is the width of the terminal.  
`min_amount=0`: Defined as the starting value of the progressbar (the number at which it will be empty)  
`max_amount=99`: Defined as the ending value of the progressbar (the number at which it will be full)  
`refresh_rate=0.5`: The time (in seconds) the progress bar takes before drawing itself again. If you keep this in a 'slow' range (>= 0.5), the progress bar will slow your program down to the minimum.  
`preceding_text=""`: You can enter some text here that is first printed before the progress bar. There will be a space in between your text and the bar percentage.  
`ending_character=\n`: The character that will be printed once the progress bar is done. Newline by default, but you can leave this empty if you're dealing with multiple progressbars at once.

Once inited, you can use the progressbar by updating it's step value, which indicates how full it is. This is done by:
```
progress_bar.update()
```
This adds 1 to the inner step variable.  
*Optional arguments:*  
`amount=1`: Add the value given by amount instead to the inner step variable.
```
progress_bar.set(amount)
```
The `amount` argument specifies to what value the step counter should be set. Unlike `progress_bar.update()`, it sets the variable instead of changing it.
```
progress_bar.update_only()
```
Same as `progress_bar.update()`, except that the progress bar will not be printed yet. This allowes for multiple updates to occur within one refresh.  
*Optional arguments:*  
`amount=1`: Add the value given by amount instead to the inner step variable.
```
progress_bar.set_only()
```
Same as `progress_bar.set(amount)`, except that the progress bar will not be printed yet. This allowes for multiple updates to occur within one refresh.
```
progress_bar.draw()
```
Prints the progressbar on the terminal. Automatically called after running `progress_bar.update()` or `progress_bar.set(amount)`.
```
progress_bar.draw_timed()
```
Calls progress_bar.draw() once every x seconds, where x is specified as `refresh_rate` upon initialisation.
```
progress_bar.end()
```
End the progress bar by moving to the next line. Automatically called when the last progressbar is drawn and it is 100%.  
*Optional arguments:*  
`clean=False`: If set to `True`, will first clear the line before moving the cursor.  
`ending_character="\n"`: This is the character that is printed. By default, this is a newline so that the cursor moves on. It should be noted that it is called after the line is cleared, if that is specified.

Recently, progressBar.py has another class in it: a WaitIndicator. It is a framework to display animations, to indicate your program is busy. Unlike the progress bar, this time is indefinite. Import it using:
```
from TimsStuff.progressBar import WaitIndicator
```
Just like the progress bar, it can only be used once inited. Do so by calling:
```
wait_indicator = WaitIndicator(animation)
```
`animation` is the animation that will be displayed while waiting. See a bit below on how this works in specific.  
*Optional arguments:*  
`width=-1`: The width of the animation. By default, this is -1, which will use the default width specified by the animation.  
`preceding_text=""`: Text that will be drawn before the animation. Is not included in the length.  
`end_text=""`: Text that will be displayed when the animation is done. Will replace the entire line on which the animation and preceding_text are displayed, but will do nothing if empty.  
`refresh_rate=1`: The time (in seconds) that will elapse between two draws. This also determines the animation speed.  
`automatic=False`: If True, a thread is started when the indicator begins, eliminating the need to call `wait_indicator.draw()` all the time.

Once inited, you can use the WaitIndicator. These functions are available:
```
wait_indicator.draw()
```
Draws the wait_indicator. It should be noted that this function is for non-automatic use only (`automatic=False`), and will do nothing if it is automated. Additionally, the actually updating of the drawing will still happen once every `refresh_rate` seconds.
```
wait_indicator.update_preceding_text(new_text)
```
Changes the preceding text mid-run. The text is updated after a successful `draw()`.
```
wait_indicator.start()
```
Can be used to start the animation.
```
wait_indicator.run()
```
Even though it is accessible, it is a mainly useful function for the automatic version of the indicator. Should **never** be called when running automated. If you call it while the program is not automatic, it can be seen as an alias for `wait_indicator.draw()`
```
wait_indicator.stop()
```
Use this to stop the wait_indicator. If may take a slight while before it is stopped if called on automatic mode, because it waits until the thread is terminated. Note: if you try to resume the indicator after calling this function and it is automatic, you will get errors because threads aren't meant to be recalled.

There are some pre-existing animations present in the class. This is a list of them:  
- WaitIndicator.DotsAnimation: This displays (by default) three dots, each appearing after another. When all dots are there, the line is cleared and the animation will begin again.
- WaitIndicator.SpinAnimation: This displays (by default) one line, that spins around it's own central axis. The recommended `refresh_rate` for this animation is 0.2. Additionally, if you change the size, it will simply display more spinners.

Additionally, you can create your own animations. Do so by creating a class, that has at least these functions and arguments in those functions:
```
class DotsAnimation ():
    # INIT function. Size determines the length of the animation, and should always be optional.
    def __init__(self, size=3):

    # Return the next step in the animation
    def next_step (self):
```
For more ideas, see the progressBar.py source code, to take a look at DotsAnimation.

Animations are eventually added to the WaitIndicator on initialisation:
```
# Example init of WaitIndicator with a default animation:
wait_indicator = WaitIndicator(WaitIndicator.DotsAnimation)
# Example init of WaitIndicator with custom animation:
wait_indicator = WaitIndicator(custom_animation_class_name_without_brackets)
```

## Contact
If you encounter any bugs, feel free to let Tim know so he can fix them. But I'm assuming that's pretty self-explanatory.
