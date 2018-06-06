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
progress_bar = ProgressBar(width)
```
The `width` argument is used to specify the number of characters the progress bar will be wide.  
*Optional arguments:*  
`min_amount=0`: Defined as the starting value of the progressbar (the number at which it will be empty)  
`max_amount=99`: Defined as the ending value of the progressbar (the number at which it will be full)

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
progress_bar.end()
```
End the progress bar by moving to the next line. Automatically called when the last progressbar is drawn and it is 100%.  
*Optional arguments:*  
`clean=False`: If set to `True`, will first clear the line before moving the cursor.  
`ending_character="\n"`: This is the character that is printed. By default, this is a newline so that the cursor moves on. It should be noted that it is called after the line is cleared, if that is specified.
