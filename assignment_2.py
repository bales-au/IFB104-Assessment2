
#-----Statement of Authorship----------------------------------------#
#
#  This is an individual assessment item for QUT's teaching unit
#  IFB104, "Building IT Systems", Semester 1, 2023.  By submitting
#  this code I agree that it represents my own work.  I am aware of
#  the University rule that a student must not act in a manner
#  which constitutes academic dishonesty as stated and explained
#  in QUT's Manual of Policies and Procedures, Section C/5.3
#  "Academic Integrity" and Section E/2.1 "Student Code of Conduct".
#
#  Put your student number here as an integer and your name as a
#  character string:
#
student_number = 11537400
student_name   = "Bailey Watts"
#
#  NB: Files submitted without a completed copy of this statement
#  will not be marked.  All files submitted will be subjected to
#  software plagiarism analysis using the MoSS system
#  (http://theory.stanford.edu/~aiken/moss/).
#
#--------------------------------------------------------------------#



#-----Assessment Task 2 Description----------------------------------#
#
#  In this assessment task you will combine your knowledge of Python
#  programming, HTML-style mark-up languages, pattern matching,
#  database management, and Graphical User Interface design to produce
#  a robust, interactive "app" that allows its user to view and save
#  data from multiple online sources.
#
#  See the client's briefings accompanying this file for full
#  details.
#
#  Note that this assessable assignment is in multiple parts,
#  simulating incremental release of instructions by a paying
#  "client".  This single template file will be used for all parts,
#  together with some non-Python support files.
#
#--------------------------------------------------------------------#



#-----Set up---------------------------------------------------------#
#
# This section imports standard Python 3 modules sufficient to
# complete this assignment.  Don't change any of the code in this
# section, but you are free to import other Python 3 modules
# to support your solution, provided they are standard ones that
# are already supplied by default as part of a normal Python/IDLE
# installation.
#
# However, you may NOT use any Python modules that need to be
# downloaded and installed separately, such as "Beautiful Soup" or
# "Pillow", because the markers will not have access to such modules
# and will not be able to run your code.  Only modules that are part
# of a standard Python 3 installation may be used.

# A function for exiting the program immediately (renamed
# because "exit" is already a standard Python function).
from sys import exit as abort

# A function for opening a web document given its URL.
# [You WILL need to use this function in your solution,
# either directly or via the "download" function below.]
from urllib.request import urlopen

# Some standard Tkinter functions.  [You WILL need to use
# SOME of these functions in your solution.]  You may also
# import other widgets from the "tkinter" module, provided they
# are standard ones and don't need to be downloaded and installed
# separately.  (NB: Although you can import individual widgets
# from the "tkinter.tkk" module, DON'T import ALL of them
# using a "*" wildcard because the "tkinter.tkk" module
# includes alternative versions of standard widgets
# like "Label" which leads to confusion.  If you want to use
# a widget from the tkinter.ttk module name it explicitly,
# as is done below for the progress bar widget.)
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar

# Functions for finding occurrences of a pattern defined
# via a regular expression.  [You do not necessarily need to
# use these functions in your solution, because the problem
# may be solvable with the string "find" function, but it will
# be difficult to produce a concise and robust solution
# without using regular expressions.]
from re import *

# A function for displaying a web document in the host
# operating system's default web browser (renamed to
# distinguish it from the built-in "open" function for
# opening local files).  [You WILL need to use this function
# in your solution.]
from webbrowser import open as urldisplay

# All the standard SQLite database functions.  [You WILL need
# to use some of these in your solution.]
from sqlite3 import *

#
#--------------------------------------------------------------------#



#-----Validity Check-------------------------------------------------#
#
# This section confirms that the student has declared their
# authorship.  You must NOT change any of the code below.
#

if not isinstance(student_number, int):
    print('\nUnable to run: No student number supplied',
          '(must be an integer)\n')
    abort()
if not isinstance(student_name, str):
    print('\nUnable to run: No student name supplied',
          '(must be a character string)\n')
    abort()

#
#--------------------------------------------------------------------#



#-----Supplied Function----------------------------------------------#
#
# Below is a function you can use in your solution if you find it
# helpful.  You are not required to use this function, but it may
# save you some effort.  Feel free to modify the function or copy
# parts of it into your own code.
#

# A function to download and save a web document.  The function
# returns the downloaded document as a character string and
# optionally saves it as a local file.  If the attempted download
# fails, an error message is written to the shell window and the
# special value None is returned.  However, the root cause of the
# problem is not always easy to diagnose, depending on the quality
# of the response returned by the web server, so the error
# messages generated by the function below are indicative only.
#
# Parameters:
# * url - The address of the web page you want to download.
# * target_filename - Name of the file to be saved (if any).
# * filename_extension - Extension for the target file, usually
#      "html" for an HTML document or "xhtml" for an XML
#      document.
# * save_file - A file is saved only if this is True. WARNING:
#      The function will silently overwrite the target file
#      if it already exists!
# * char_set - The character set used by the web page, which is
#      usually Unicode UTF-8, although some web pages use other
#      character sets.
# * incognito - If this parameter is True the Python program will
#      try to hide its identity from the web server. This can
#      sometimes be used to prevent the server from blocking access
#      to Python programs. However we discourage using this
#      option as it is both unreliable and unethical to
#      override the wishes of the web document provider!
#
def download(url = 'http://www.wikipedia.org/',
             target_filename = 'downloaded_document',
             filename_extension = 'html',
             save_file = True,
             char_set = 'UTF-8',
             incognito = False):

    # Import the function for opening online documents and
    # the class for creating requests
    from urllib.request import urlopen, Request

    # Import an exception sometimes raised when a web server
    # denies access to a document
    from urllib.error import HTTPError

    # Import an exception raised when a web document cannot
    # be downloaded due to some communication error
    from urllib.error import URLError

    # Open the web document for reading (and make a "best
    # guess" about why if the attempt fails, which may or
    # may not be the correct explanation depending on how
    # well behaved the web server is!)
    try:
        if incognito:
            # Pretend to be a web browser instead of
            # a Python script (NOT RELIABLE OR RECOMMENDED!)
            request = Request(url)
            request.add_header('User-Agent',
                               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
                               'AppleWebKit/537.36 (KHTML, like Gecko) ' +
                               'Chrome/42.0.2311.135 Safari/537.36 Edge/12.246')
            print("Warning - Request does not reveal client's true identity.")
            print("          This is both unreliable and unethical!")
            print("          Proceed at your own risk!\n")
        else:
            # Behave ethically
            request = url
        web_page = urlopen(request)
    except ValueError as message: # probably a syntax error
        print("\nCannot find requested document '" + url + "'")
        print("Error message was:", message, "\n")
        return None
    except HTTPError as message: # possibly an authorisation problem
        print("\nAccess denied to document at URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None
    except URLError as message: # probably the wrong server address
        print("\nCannot access web server at URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None
    except Exception as message: # something entirely unexpected
        print("\nSomething went wrong when trying to download " + \
              "the document at URL '" + str(url) + "'")
        print("Error message was:", message, "\n")
        return None

    # Read the contents as a character string
    try:
        web_page_contents = web_page.read().decode(char_set)
    except UnicodeDecodeError as message:
        print("\nUnable to decode document from URL '" + \
              url + "' as '" + char_set + "' characters")
        print("Error message was:", message, "\n")
        return None
    except Exception as message:
        print("\nSomething went wrong when trying to decode " + \
              "the document from URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None

    # Optionally write the contents to a local text file
    # (overwriting the file if it already exists!)
    if save_file:
        try:
            text_file = open(target_filename + '.' + filename_extension,
                             'w', encoding = char_set)
            text_file.write(web_page_contents)
            text_file.close()
        except Exception as message:
            print("\nUnable to write to file '" + \
                  target_filename + "'")
            print("Error message was:", message, "\n")

    # Return the downloaded document to the caller
    return web_page_contents

#
#--------------------------------------------------------------------#



#-----Student's Solution---------------------------------------------#
#
# Put your solution below.
#

# Create the main window
task_2_main_window = Tk()

# Your code goes here

# Define the root window's title
task_2_main_window.title('System Link Reviews GUI')

### Define window size
##task_2_main_window.geometry('500x900')

task_2_main_window.configure(bg='#36393F')

connection = connect('media_reviews.db')
cursor = connection.cursor()


# Declate as global variables
song = ""  
artist = ""  
show = ""
duration = ""
game = ""
release = ""

# Import an image to display in the window
media_logo = PhotoImage(file = 'media.png')
media_logo = media_logo.subsample(5) # Resize image

image = Label(task_2_main_window, image = media_logo)
image.configure(bg='#36393F')
image.grid(row=0, column=0, sticky=W+E)

title = Label(task_2_main_window, text='System Link Reviews', font=('Arial', 30), fg="white")
title.configure(bg='#36393F')
title.grid(row=1, column=0, sticky=W+E, pady=30)

# Create a text label for the following optionmenu widget
entertainment_options = Label(task_2_main_window, text = 'Entertainment Options:', font=('Arial', 18), fg="white")
entertainment_options.configure(bg='#36393F')
entertainment_options.grid(row=2, column=0, sticky=W+E)

# Create an optionmenu widget 
options = ["Radio - Triple J", "Television - 9Now", "Video Games - Steam"]

selected_option = StringVar(task_2_main_window)
selected_option.set("Select an option...")



def option_selected(*args):
    if selected_option.get() == "Radio - Triple J":
        review_status.delete("1.0", "end")
        review_status.insert("1.0", "Entertainment: 'Radio - Triple J' selected.".center(0))
    elif selected_option.get() == "Television - 9Now":
        review_status.delete("1.0", "end")
        review_status.insert("1.0", "Entertainment: 'Television - 9Now' selected.".center(0))
    elif selected_option.get() == "Video Games - Steam":
        review_status.delete("1.0", "end")
        review_status.insert("1.0", "Entertainment: 'Video Games - Steam' selected.".center(0))

selected_option.trace("w", option_selected)  # Call option_selected when option changes

option_menu = OptionMenu(task_2_main_window, selected_option, *options)
option_menu.config(width=50,bg='#36393F', fg="white")
option_menu.grid(row=3, column=0, sticky=W+E, padx=30, pady=5)


# Give functionality to the show details button
def open_website():
    selected_option_value = selected_option.get()
    if selected_option_value == "Select an option...":
        review_status.delete("1.0", "end")
        review_status.tag_configure("error", foreground="red")
        review_status.insert("1.0", "ERROR: Entertainment option not selected.", "error")
    elif selected_option_value == "Radio - Triple J":
        urldisplay("https://www.abc.net.au/triplej/featured-music")
        review_status.delete("1.0", "end")
        review_status.insert("1.0", 'Showing song details in your web browswer from: https://www.abc.net.au/triplej/featured-music')
    elif selected_option_value == "Television - 9Now":
        urldisplay("https://www.9now.com.au/live/channel-9")
        review_status.delete("1.0", "end")
        review_status.insert("1.0", 'Showing streamed TV show details in your web browswer from: https://www.9now.com.au/live/channel-9')
    elif selected_option_value == "Video Games - Steam":
        urldisplay("https://store.steampowered.com/explore/upcoming/")
        review_status.delete("1.0", "end")
        review_status.insert("1.0", 'Showing upcoming game details in your web browswer from: https://store.steampowered.com/explore/upcoming/')


# Give functionality to the show details button
def show_details():
    global song, artist, show, duration, game, release
    selected_option_value = selected_option.get()
    if selected_option_value == "Select an option...":
        review_status.delete("1.0", "end")
        review_status.tag_configure("error", foreground="red")
        review_status.insert("1.0", "ERROR: Entertainment option not selected.", "error")
    elif selected_option_value == "Radio - Triple J":
        triplej_page = urlopen("https://www.abc.net.au/triplej/featured-music")
        j_byte = triplej_page.read()
        j_html = j_byte.decode('UTF-8')
        song = search('data-component="KeyboardFocus">([A-Za-z 0-9]+)', j_html)
        song = song.group(1)
        artist = search('"secondaryTitle":"([A-Za-z 0-9]+)"', j_html)
        artist = artist.group(1)
        review_status.delete("1.0", "end")
        review_status.insert("1.0", f'"{song}" performed by {artist} selected for review.')
    elif selected_option_value == "Television - 9Now":
        nine_page = urlopen("https://www.9now.com.au/live/channel-9")
        nine_byte = nine_page.read()
        nine_html = nine_byte.decode('UTF-8')
        show = search('itemProp="channel/title">([A-Za-z : 0-9]+)', nine_html)
        show = show.group(1)
        duration = search('dateTime="([A-Za-z 0-9]+)', nine_html)
        duration = duration.group(1)
        review_status.delete("1.0", "end")
        review_status.insert("1.0", f'"{show}" (duration: {duration}) on 9Now selected for review.')
    elif selected_option_value == "Video Games - Steam":
        steam_page = urlopen("https://store.steampowered.com/explore/upcoming/")
        steam_byte = steam_page.read()
        steam_html = steam_byte.decode('UTF-8')
        game = search('<div class="tab_item_name">([A-Za-z : 0-9]+)', steam_html)
        game = game.group(1)
        release = search('<div class="release_date">([A-Za-z : 0-9]+)', steam_html)
        release = release.group(1)
        review_status.delete("1.0", "end")
        review_status.insert("1.0", f'"{game}" (Release Date: {release}) on Steam selected for review.')



# Create two buttons next to eachother
buttonframe = Frame(task_2_main_window)
buttonframe.columnconfigure(0, weight=1)
buttonframe.columnconfigure(1, weight=1)

btn1 = Button(buttonframe, text='Show Summary', font = ('Arial', 16),fg="white", command=show_details)
btn1.configure(bg='#36393F')
btn1.grid(row=0, column=0, sticky=W+E)

btn2 = Button(buttonframe, text='Show Details', font = ('Arial', 16),fg="white", command=open_website)
btn2.configure(bg='#36393F')
btn2.grid(row=0, column=1, sticky=W+E)
buttonframe.grid(row=4, column=0, sticky=W+E,padx=30, pady=5)

# Status Label
status = Label(task_2_main_window, text = 'Review Status:',font = ('Arial', 18), fg="white")
status.configure(bg='#36393F')
status.grid(row=5, column=0, sticky=W+E, padx=5, pady=(50, 20))

# Create status 
review_status = Text(task_2_main_window, width = 40, height = 5, wrap = WORD, font=("Arial", 16), fg="white", bg='#36393F')
initial_status = "Awaiting Submission... "
review_status.insert("1.0", initial_status.center(0))
review_status.grid(row=6, column=0, sticky=W+E, padx=30, pady=0)

# Your Rating Label
your_rating = Label(task_2_main_window, text = 'Your Rating:',font = ('Arial', 18), fg="white")
your_rating.configure(bg='#36393F')
your_rating.grid(row=9, column=0, sticky=W+E, padx=5, pady=(40,0))

# Star rating
rating_scale = Scale(task_2_main_window, to=5, orient=HORIZONTAL, highlightthickness=0, length=200, showvalue=1, fg="white")
rating_scale.configure(bg='#36393F')
rating_scale.grid(row=10, column=0, sticky=W+E, padx=150, pady=5)

# User input out of 5 stars
user_rating = Label(task_2_main_window, text='(1 out of 5 stars)', font=('Arial', 10), fg="white")
user_rating.configure(bg='#36393F')
user_rating.grid(row=11, column=0, sticky=W+E, padx=5, pady=5)

rating_value = 0

# Function to update label text
def update_user_rating(value):
    global rating_value
    rating_value = value
    user_rating.config(text=f'({value} out of 5 stars)')

# Set the function to be called each time the scale input changes
rating_scale.config(command=lambda value: update_user_rating(value))




# Function to handle the submit button
def submit_review():
    global song, artist
    selected_option_value = selected_option.get()
    review_status_value = review_status.get("1.0", "end").strip()  # Remove leading/trailing whitespace
    if selected_option_value == "Select an option...":
        review_status.delete("1.0", "end")
        review_status.tag_configure("error", foreground="red")
        review_status.insert("1.0", "ERROR: Entertainment option not selected.", "error")
        
    elif review_status_value == "Entertainment: 'Radio - Triple J' selected.":
        review_status.delete("1.0", "end")
        review_status.tag_configure("error", foreground="red")
        review_status.insert("1.0", "ERROR: Entertainment summary not received.", "error")
    elif review_status_value == "Entertainment: 'Television - 9Now' selected.":
        review_status.delete("1.0", "end")
        review_status.tag_configure("error", foreground="red")
        review_status.insert("1.0", "ERROR: Entertainment summary not received.", "error")
    elif review_status_value == "Entertainment: 'Video Games - Steam' selected.":
        review_status.delete("1.0", "end")
        review_status.tag_configure("error", foreground="red")
        review_status.insert("1.0", "ERROR: Entertainment summary not received.", "error")

        # Review completion for Triple J selection
    elif review_status_value == f'"{song}" performed by {artist} selected for review.':
        review_status.delete("1.0", "end")
        review_status.tag_configure("success", foreground="green")
        review_status.insert("1.0", "Review submitted! You gave " + f"{rating_value} out of 5 stars" + " to " + f'"{song}" by {artist}.', "success")

        try:
            cursor.execute("INSERT INTO reviews (review, event_source, event_summary, url) VALUES (?, ?, ?, ?)",
                            (rating_value, "Radio - Triple J", f"{song} by {artist}", "https://www.abc.net.au/triplej/featured-music"))
            connection.commit()
        except Exception as e:
            review_status.delete("1.0", "end")
            review_status.tag_configure("error", foreground="red")
            review_status.insert("1.0", "ERROR: Cannot find the file media_reviews.db.", "error")

        # Log the error or display an error message


        # Review completion for 9Now slection
    elif review_status_value == f'"{show}" (duration: {duration}) on 9Now selected for review.':
        review_status.delete("1.0", "end")
        review_status.tag_configure("success", foreground="green")
        review_status.insert("1.0", "Review submitted! You gave " + f"{rating_value} out of 5 stars" + " to " + f'"{show}" (duration: {duration}) on 9Now.', "success")
        try:
            cursor.execute("INSERT INTO reviews (review, event_source, event_summary, url) VALUES (?, ?, ?, ?)",
                            (rating_value, "Television - 9Now", f"{show} (duration: {duration})", "https://www.9now.com.au/live/channel-9"))
            connection.commit()
        except Exception as e:
            review_status.delete("1.0", "end")
            review_status.tag_configure("error", foreground="red")
            review_status.insert("1.0", "ERROR: Cannot find the file media_reviews.db.", "error")
            
        # Review completion for Steam selection
    elif review_status_value == f'"{game}" (Release Date: {release}) on Steam selected for review.':
        review_status.delete("1.0", "end")
        review_status.tag_configure("success", foreground="green")
        review_status.insert("1.0", "Review submitted! You gave " + f"{rating_value} out of 5 stars for " + f'"{game}" (Release Date: {release}) on Steam.', "success")
        try:
            cursor.execute("INSERT INTO reviews (review, event_source, event_summary, url) VALUES (?, ?, ?, ?)",
                            (rating_value, "Video Games - Steam", f"{game} (release date: {release})", "https://store.steampowered.com/explore/upcoming/"))
            connection.commit()
        except Exception as e:
            review_status.delete("1.0", "end")
            review_status.tag_configure("error", foreground="red")
            review_status.insert("1.0", "ERROR: Cannot find the file media_reviews.db.", "error")


    elif review_status_value == 'ERROR: Entertainment summary not received.':
        review_status.delete("1.0", "end")
        review_status.tag_configure("error", foreground="red")
        review_status.insert("1.0", "ERROR: Entertainment summary not received.", "error")
        
    elif selected_option_value == "Radio - Triple J":
        review_status.delete("1.0", "end")
        review_status.tag_configure("success", foreground="green")
        review_status.insert("1.0", "Review submitted! You gave " + f"{rating_value} out of 5 stars" + " to " + f'"{song}" by {artist}.', "success")
        try:
            cursor.execute("INSERT INTO reviews (review, event_source, event_summary, url) VALUES (?, ?, ?, ?)",
                            (rating_value, "Radio - Triple J", f"{song} by {artist}", "https://www.abc.net.au/triplej/featured-music"))
            connection.commit()
        except Exception as e:
            review_status.delete("1.0", "end")
            review_status.tag_configure("error", foreground="red")
            review_status.insert("1.0", "ERROR: Cannot find the file media_reviews.db.", "error")
            
    elif selected_option_value == "Television - 9Now":
        review_status.delete("1.0", "end")
        review_status.tag_configure("success", foreground="green")
        review_status.insert("1.0", "Review submitted! You gave " + f"{rating_value} out of 5 stars" + " to " + f'"{show}" (duration: {duration}) on 9Now.', "success")
        try:
            cursor.execute("INSERT INTO reviews (review, event_source, event_summary, url) VALUES (?, ?, ?, ?)",
                            (rating_value, "Television - 9Now", f"{show} (duration: {duration})", "https://www.9now.com.au/live/channel-9"))
            connection.commit()
        except Exception as e:
            review_status.delete("1.0", "end")
            review_status.tag_configure("error", foreground="red")
            review_status.insert("1.0", "ERROR: Cannot find the file media_reviews.db.", "error")
            
    elif selected_option_value == "Video Games - Steam":
        review_status.delete("1.0", "end")
        review_status.tag_configure("success", foreground="green")
        review_status.insert("1.0", "Review submitted! You gave " + f"{rating_value} out of 5 stars for " + f'"{game}" (Release Date: {release}) on Steam.', "success")
        try:
            cursor.execute("INSERT INTO reviews (review, event_source, event_summary, url) VALUES (?, ?, ?, ?)",
                            (rating_value, "Video Games - Steam", f"{game} (release date: {release})", "https://store.steampowered.com/explore/upcoming/"))
            connection.commit()
        except Exception as e:
            review_status.delete("1.0", "end")
            review_status.tag_configure("error", foreground="red")
            review_status.insert("1.0", "ERROR: Cannot find the file media_reviews.db.", "error")
            
# Submit button
submit_button = Button(task_2_main_window, text='Submit', font = ('Arial', 18), fg="white", command=submit_review)
submit_button.configure(bg='#36393F')
submit_button.grid(row=12, column=0, sticky=W+E, padx=200, pady=70)


connection.commit()

# Start the event loop to detect user inputs
task_2_main_window.mainloop()
