import re

__START = "\033[4m"
__END = "\033[24m"

END = "\033[0m"


def _parse_label(label):
    """Parses out the shortcut key of a given label and returns a 2-tuple
        in which the first value is the shortcut and the second is
        the label with shortcut key underlined using ANSI codes"""
    shortcut_pos = label.index("_")         # Shortcuts are annotated by prefixing with _
    label = label.replace("_", "")          # Remove the shortcut annotation
    shortcut = label[shortcut_pos].lower()  # Get the shortcut char
    # underline the shortcut letter using ANSII codes
    label = label[:shortcut_pos] + __START + label[shortcut_pos] + __END + label[shortcut_pos+1:]
    return shortcut, label

def print_heading(heading):
    """Prints a heading with a top and bottom border"""
    print("=" * (len(heading) + 4))
    print("  " + heading)
    print("-" * (len(heading) + 4))

def constrained_input(prompt, allowed_responses, fail_message):
    """Repeatedly prompts the user with the given prompt
        until they provide one of the allowed_responses.
        If the user provides an invalid response, the fail_message is printed"""

    # Input is always text, so we need to convert the given allowed responses to text too
    allowed_responses = [ str(x) for x in allowed_responses ]
    
    while True:

        response = input(prompt)

        if response in allowed_responses:
            return response
        else:
            print(fail_message)

def options(prompt, opts):
    """Prompts the user to select one of the options given in opts.
        Returns the value corresponding to the selected option.
        opts must be a sequence of (value, label) tuples, where label is what
        the user sees in the options prompt, and value is what is returned if
        that option is selected.
        """

    print(prompt)

    valid_selections = []
    for i, opt in enumerate(opts):
        print(str(i+1) + ". " + opt[1])
        valid_selections.append(str(i+1))

    while True:
        selection = input("Which do you choose? ")
        if selection in valid_selections:
            break
        else:
            print("That is not a valid selection.")
    
    return opts[int(selection)-1][0]  # Selection is a 1-based string



def dialog(heading, data):
    """Prompts the user with the sequence of prompts in the given data list.
        Each value in the data list may be a string, or a tuple.
        If it is a tuple, the first value will be the displayed prompt,
        and the second value must be a regular expression that the user must
        match before their input for that prompt is accepted."""
    print_heading(heading)

    responses = []
    for item in data:
        pattern = ""
        if isinstance(item, tuple):
            prompt, pattern = item
        else:
            prompt = item

        while True:
            response = input(prompt + ": ").strip()
            if not pattern or re.match(pattern, response):
                break
            print("Invalid input")
    
        responses.append(response)

    return responses

def table(headings, data):
    """Prints a formatted table with the given headings and data.
        Headings must be a sequence of strings, and data must be a 2D sequence
        in which each row represents one row of the table.
        Each data row must have the same length as headings"""

    def measure_row(row, widths, heights):
        """Determines the height of the given row (in terms of lines of text), and 
            adds that height to the given heights list.
            Also determines if the width of any column in the row is larger than
            the current width in the given widths list.  (The widths list must be
            a list of integers of the same length the row.)"""
        height = 1
        for col_idx, col in enumerate(row):
            col = str(col)  # In case we're dealing with a non-string datatype
            lines = col.split("\n")
            for line in lines:
                length = len(line)
                # Override the old width if this width is wider
                if length > widths[col_idx]:
                    widths[col_idx] = length
            # If this cell is higher than others in the row, override the old height
            if len(lines) > height:
                height = len(lines)
        heights.append(height)

    row_heights = []
    col_widths = []

    # Set the column widths to 0 as a starting point
    for _ in range(len(headings)):
        col_widths.append(0)

    table = [headings] + data
    for row in table:
        measure_row(row, col_widths, row_heights)

    # Table width is the sum of the column widths, 
    # plus the amount of space (3) between each column when we print
    table_width = sum(col_widths) + 3*(len(col_widths) - 1)

    # Calculate the lines of text we'll need to print the table
    strdata = []
    for row_idx, row in enumerate(table):
        row_height = row_heights[row_idx]
        
        for line_num in range(row_height):
            row_strdata = []
            for col_idx, col in enumerate(row):
                col = str(col)  # In case we're dealing with a non-string datatype
                # Each column in the row may have a number of lines equal to the row_height
                # Here's I'm just taking the inefficient approach of blindly splitting the 
                # cell data for each line of text, and then grabbing the line if there is one
                lines = col.split("\n")
                if len(lines) > line_num:  # Make sure we only take a line of text if there is one there
                    line = lines[line_num]
                    # Pad the cell's text with spaces up to the column width
                    row_strdata.append(line + " "*(col_widths[col_idx] - len(line)))
                else:
                    # Otherwise, just fill this cell with spaces
                    row_strdata.append(" "*col_widths[col_idx])
            strdata.append(row_strdata)

    # Merge the lines of text from above into text representing each row in the table
    row_strs = []
    row_str = ""
    line_idx = 0
    for row_idx in range(len(table)):
        row_str = ""
        for i in range(row_heights[row_idx]):        
            row_str += "   ".join(strdata[line_idx]) + "\n"
            line_idx += 1
        row_strs.append(row_str)
           
    # Finally, merge the rows into a single string to print
    tablestr = row_strs[0]                                       # Headings
    tablestr += "="*table_width + "\n"                           # Heading divider
    tablestr += ("-"*table_width + "\n").join(row_strs[1:])      # Row dividers
    tablestr += ("-"*table_width + "\n")                         # Bottom line
    print(tablestr)

def menu(heading, data):
    """Displays a menu to the user with the given heading.
        The menu data is a sequence of 2-tuples, each representing one menu item.  
        The first value in a tuple is the menu label, a string.  This string must have one _ charcter
        preceding the character in the menu label that is to be used as the shortcut key to open
        that menu item.
        The second value in a tuple may be a further 2-tuple, representing a submenu,
        or a function object, representing the function to be called when the menu item is opened."""

    print()
    print_heading(heading)
    
    actions = {}

    for item in data:
        shortcut, label = _parse_label(item[0])
        if hasattr(item[1], '__call__'):
            actions[shortcut] = item[1]
        else:
            actions[shortcut] = lambda L=label, i=item[1]: menu(L, i)
        print(label)

    print()

    while True:
    
        response = input("What now? ").lower()

        if response in actions.keys():
            actions[response]()
            break
        else:
            print("That is not an option.")
