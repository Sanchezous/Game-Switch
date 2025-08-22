import os, math, sys, subprocess, csv
import customtkinter as ctk
from PIL import Image# , ImageTk

dirMain = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Main directory (gets the parent directory of the current file)
dirAssets = os.path.join(dirMain, 'Assets') # Asset Directory
dirWindows = os.path.join(dirMain, 'Windows') # Window Directory
dirGameInfo = os.path.join(dirMain, 'GameInformation') # Game Information Directory
with open(os.path.join(dirGameInfo, 'AllGameInformation.csv'), newline='', encoding='utf-8') as file:       # Reads all game information from a CSV file (this makes it easy to edit outside of the program)
    arrAllGames = list(csv.reader(file)) # Extracts the CSV file into an array which is a list in python
with open(os.path.join(dirGameInfo, 'GameInstanceStatus.csv'), newline='', encoding='utf-8') as file:       
    allGameInstances = [[int(value) for value in row] for row in csv.reader(file)] # allInstances[0], borrowedInstances[1], ownedInstances[2], lendedInstances[3]
borrowedInstances, ownedInstances, lendedInstances = allGameInstances[0], allGameInstances[1], allGameInstances[2]
allInstances = ownedInstances + borrowedInstances  # Combines all instances into one list
class Listing(ctk.CTkFrame):
    allListings, ownedListings, borrowedListings, lendedListings= [], [], [], []
    def __init__(self, master, gameIndex, addOrInfo):
        super().__init__(master, width = 200, height = 200)
        self.grid_propagate(False)
        self.toggled, self.addOrInfo, self.gameIndex = False, addOrInfo, gameIndex
        self.widthCurrent = self.widthBase = 200
        self.widthFinal = self.widthBase * 2
        self.configure(width = self.widthBase)

        self.columnconfigure(0, weight = 1)   # Makes it so the image doesn't move on toggle
        self.rowconfigure((0, 1, 2), weight = 1) # Makes the rows automatially center

        self.image = ctk.CTkImage(Image.open(os.path.join(dirAssets, 'Game Assets', arrAllGames[gameIndex][0] + '.jpg')), size = (120, 120))
        self.lblImage = ctk.CTkLabel(self, image = self.image, text = '') # Image
        self.lblImage.grid(row = 0, column = 0, pady = (10, 0), padx = (40,0), rowspan = 3)

        self.lblTitle = ctk.CTkLabel(self, text = arrAllGames[gameIndex][2], font = ('Segoe UI', 16, 'bold'), justify = 'center', wraplength = 170)   # Title for both Image and Description
        self.lblTitle.grid(row = 3, column = 0, columnspan = 3, pady = (0, 5), padx = (5,5), sticky = 'ew')

        self.lblDesc = ctk.CTkLabel(self, text = arrAllGames[gameIndex][3], wraplength = 150, justify = 'left', font=('Hevetica',12)) # Description
        self.lblDesc.grid(row = 1, column = 1, rowspan = 2, columnspan = 3,  padx = (40,25),  pady = (0,0), sticky = 'w')
        self.lblDesc.grid_remove() 

        self.lblSeries = ctk.CTkLabel(self, text = ('Part of the ' + arrAllGames[gameIndex][1][2:] + ' series'), wraplength = 150, justify = 'left', font=('Hevetica',12, 'italic')) # Series
        self.lblSeries.grid(row = 3, column = 1, columnspan = 3,  padx = (40,25),  pady = (0,0), sticky = 'w')
        self.lblSeries.grid_remove() 

        self.grid_columnconfigure(0, weight = 0)  # Image column
        self.grid_columnconfigure(1, weight = 1)  # Description column
        if gameIndex in borrowedInstances:
            Listing.borrowedListings.append(self) # Adds the instance to the borrowed listings
            self.configure(fg_color = 'maroon')
        if gameIndex in ownedInstances:
            Listing.ownedListings.append(self) # Adds the instance to the owned listings
            if self.addOrInfo == 'add':
                self.toggled = True
                self.configure(fg_color = 'green4') # Changes the background colour to green when toggled
        if gameIndex in lendedInstances:
            Listing.lendedListings.append(self)  # Adds the instance to the lended listings
            self.configure(fg_color = 'gray80')# Lended listings are greyed out
            self.lblDesc.configure(text_color = 'gray20')
            self.lblTitle.configure(text_color = 'gray20')
            self.lblSeries.configure(text_color = 'gray20') 
        Listing.allListings.append(self) # Adds the instance to  all listings
        
        self.bind('<Button-1>', self.Toggle)        # Expand/Contracts on mouse click on image,  title, or background
        self.lblImage.bind('<Button-1>', self.Toggle)
        self.lblTitle.bind('<Button-1>', self.Toggle)

    # Changes if the description is visible or not and resizes the widget
    def Toggle(self, event=None):
        self.toggled = not self.toggled
        if self.addOrInfo == 'info':
            if self.toggled:
                self.LstResize(self.widthCurrent, self.widthFinal, descShow = True) # Doubles base size
                if self in Listing.ownedListings:           # Resets clicked instances in Owned
                    for listing in Listing.ownedListings:
                        if listing != self and listing.toggled:
                            listing.LstResize(listing.widthCurrent, listing.widthBase, descHide = True)
                            listing.toggled = not listing.toggled
                elif self in Listing.borrowedListings:        # Resets clicked instances in Borrowed
                    for listing in Listing.borrowedListings:
                        if listing != self and listing.toggled:
                            listing.LstResize(listing.widthCurrent, listing.widthBase, descHide = True)
                            listing.toggled = not listing.toggled
            else:
                self.LstResize(self.widthCurrent, self.widthBase, descHide = True)
        if self.addOrInfo == 'add':
            if self not in (Listing.lendedListings + Listing.borrowedListings):  # Lended or borrowed listings do not toggle
                if self.toggled == True:
                    if self.gameIndex not in (ownedInstances + borrowedInstances):
                        ownedInstances.append(int(self.gameIndex))
                        self.UpdateInstances()    
                        self.configure(fg_color = 'green4') # Changes the background colour to green when toggled
                if self.toggled == False:
                    if self.gameIndex in ownedInstances:
                        ownedInstances.remove(int(self.gameIndex))
                        self.UpdateInstances()    
                        self.configure(fg_color = 'gray16') # Changes the background colour to gray when untoggled
            else: self.toggled = False # Lended or borrowed listings do not toggle
    def UpdateInstances(self):
        global ownedInstances, borrowedInstances, lendedInstances
        allInstances = ownedInstances + borrowedInstances + lendedInstances  # Combines all instances into one list
        with open(os.path.join(dirGameInfo, 'GameInstanceStatus.csv'), mode = 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(borrowedInstances)
            writer.writerow(ownedInstances)
            writer.writerow(lendedInstances)
        with open(os.path.join(dirGameInfo, 'GameInstanceStatus.csv'), newline='', encoding='utf-8') as file:       
            allGameInstances = [[int(value) for value in row] for row in csv.reader(file)] # allInstances[0], borrowedInstances[1], ownedInstances[2], lendedInstances[3]
        borrowedInstances, ownedInstances, lendedInstances = allGameInstances[0], allGameInstances[1], allGameInstances[2]
    # Makes the animation smooth
    def LstResize(self, widthStart, widthEnd, descShow = False, descHide = False):
        duration, steps = 150, 10  # Duration is the animation length in ms # steps is how smooth the animation is
        delay = duration // steps # The // just means floor function so it divides and rounds down to stay an integer
        deltaWidth = widthEnd - widthStart # Width difference between start and end

        def step(i):
            c = i / steps
            movement = -(math.cos(math.pi * c) - 1) / 2 
            widthCurrent = int(widthStart + deltaWidth * movement) # Uses cosine graph to make the animation smooth
            self.configure(width = widthCurrent)
            self.widthCurrent = widthCurrent
            if descShow:
                self.lblDesc.grid() # Show description
                self.lblSeries.grid()
                self.lblTitle.configure(font = ('Segoe UI', 22, 'bold'), justify = 'left') 
                self.lblTitle.grid(row = 0, column = 1, columnspan = 3, padx = (40,20), pady = (0,0), sticky = 'w') # Title moves to description
                self.image.configure(size = (150,150)) # Enlarge Image
                self.lblImage.grid(row = 0, column = 0, pady = (30, 0), padx = (25,0), rowspan = 3)
            if i < steps:
                self.after(delay, lambda: step(i + 1))
            else:
                self.configure(width = widthEnd)
                self.widthCurrent = widthEnd
                if descHide:
                    self.lblDesc.grid_remove() # Hide description
                    self.lblSeries.grid_remove()
                    self.lblTitle.configure(font = ('Segoe UI', 16, 'bold'), justify = 'center', wraplength = 170)  
                    self.lblTitle.grid(row = 3, column = 0, pady = (0, 5), padx = (5,5), sticky = 'ew') # Title moves to Image
                    self.image.configure(size = (120,120)) # Shrink Image
                    self.lblImage.grid(row = 0, column = 0, pady = (0, 0), padx = (40,0), rowspan = 3)

        step(0) # Starts the animation (step is recursive)

class HelpLabel:
    def __init__(self, widget, text):
        self.widget = widget
        self.container = widget.winfo_toplevel()   # Makes it on top
        self.label = None
        self.text = text
        widget.bind("<Enter>", self.Enter)
        widget.bind("<Leave>", self.Leave)
        widget.bind("<Motion>", self.Motion)

    def Enter(self, event=None):
        if self.label is None:
            self.label = ctk.CTkLabel(self.container, text=self.text, fg_color="gray13", text_color="white", corner_radius=6)
            self.label.place(x=-1000, y=-1000)  # Stored off screen until called

    def Motion(self, event):
        if not self.label:
            return
        root_x = self.container.winfo_rootx()# Gets it to the correct mouse psition
        root_y = self.container.winfo_rooty()
        x = event.x_root - root_x - 500
        y = event.y_root - root_y + 20
        self.label.place(x=x, y=y)

    def Leave(self, event=None):
        if self.label:
            self.label.destroy()
            self.label = None
 
if __name__ == "__main__":
    ctk.set_appearance_mode('System')
    ctk.set_default_color_theme(os.path.join(dirMain, 'themetendo.json')) # Nintendo colours dark mode
    tabLibrary = ctk.CTk()
    tabLibrary.geometry('1130x1200')
    tabLibrary.resizable(False, True) # <--- Change this after Testing
    tabLibrary.title('Super Smash Bros MHS | Game Library')
    tabLibrary.grid_columnconfigure((0, 1), weight=1)
    tabLibrary.grid_rowconfigure((1, 3, 4, 5), weight=1)
    fntHeading = ctk.CTkFont(family = 'Impact', size=72)
    fntTitle = ctk.CTkFont(family = 'Segoe UI', size = 16, weight = 'bold')

    def QuickSort(array): # Quicksort is fastest for this use case which usually has large amounts of data
        if len(array) > 1: # I keep using [0] because im only sorting the 1st element of each pair
            pivot = array[len(array) // 2][0]  # Pick the middle element as pivot
            left = [x for x in array if x[0] < pivot] # Everything before the pivot alphabetically gets partitioned to the left
            middle = [x for x in array if x[0] == pivot] # The Pivot stays in the middle
            right = [x for x in array if x[0] > pivot] # Everything after the pivot alphabetically gets partitioned to the right
            return QuickSort(left) + middle + QuickSort(right) # Recursively call the function until it all arrays of length 1
        else:
            return array

    def OwnedFilter(filter): # Gets the order and amount of Listings and places them
        arrFilteredInstances = ownedInstances[::-1] # [::-1] read the array with a negative step and reverses it
        if filter != 'Recent': # The listings are stored by recent so they shouldn't be filtered
            check = 2 if filter == 'Name' else 1 # If the filter is by name, check the name column, otherwise check the series column
            arrGamePairs = [(arrAllGames[i][check], i) for i in ownedInstances] # Makes a list of the game name + the index
            arrFilteredInstances = [x[1] for x in QuickSort(arrGamePairs)] # Sorts the game names alphabetically and returns the indexes of the owned instances
        if filter == 'Lended':
            arrFilteredInstances = lendedInstances # Sets is to be in order of oldest to newest lended instances
        for child in frmOwned.winfo_children():
                child.destroy()
        Listing.ownedListings, Listing.lendedListings = [], [] # Resets the owned and lended listings
        ownRow = -1
        for val, listing in enumerate(arrFilteredInstances):
            lstOwned = Listing(frmOwned, listing, 'info')
            ownCol = val % 4
            if ownCol == 0:
                ownRow += 1
            lstOwned.grid(row = ownRow, column = ownCol, padx = 10, pady = 10, sticky = 'w')
    # Borrowed
    lblBorrowed = ctk.CTkLabel(tabLibrary, text = 'BORROWED', font = fntHeading)
    lblBorrowed.grid(row = 0, column = 0, padx = 20, pady = 0, sticky = 'w')
    scrBorrowed = ctk.CTkScrollableFrame(tabLibrary, orientation='horizontal')
    frmBorrowed = ctk.CTkFrame(scrBorrowed)
    scrBorrowed.propagate(False)
    frmBorrowed.propagate(False)
    scrBorrowed.grid(row = 1, column = 0, padx = 20, pady = 0, sticky = 'ew', columnspan = 5)
    frmBorrowed.grid(row = 0, column = 0,padx = 0, pady = (0, 20), sticky = 'nw')
    status = 'borrowed'
    for val, entry in enumerate(borrowedInstances):
        lstBorrowed = Listing(frmBorrowed, entry, 'info')
        lstBorrowed.grid(row = 1, column = val, padx = 10, pady = 10, sticky = 'w')
    # Owned
    lblOwned = ctk.CTkLabel(tabLibrary, text = 'OWNED', font = fntHeading)
    lblOwned.grid(row = 2, column = 0, padx = 20, pady = 0, sticky = 'w')
    scrOwned = ctk.CTkScrollableFrame(tabLibrary)
    frmOwned = ctk.CTkFrame(scrOwned)
    frmOwned.propagate(False)
    scrOwned.propagate(False)
    scrOwned.grid(row = 3, column = 0, padx = 20, pady = 0, sticky = 'nsew', columnspan = 5, rowspan = 2)
    frmOwned.grid(row = 0, column = 0, padx = 0, pady = 0, sticky = 'nsew')
    ownRow = -1
    for val, entry in enumerate(ownedInstances):
        lstOwned = Listing(frmOwned, entry, 'info')
        ownCol = val % 4 # This structure with ownCol and ownRow allows for a 4-column layout, marked by the %4
        ownRow = ownRow + 1 if ownCol == 0 else ownRow
        lstOwned.grid(row = ownRow, column = ownCol, padx = 10, pady = 10, sticky = 'w')

    frmListing = ctk.CTkFrame(tabLibrary, corner_radius=32, fg_color='gray75')
    frmListing.columnconfigure(0, weight=1)
    frmListing.grid(row=2, column=1, pady=0, padx=20, columnspan=1, sticky = 'w')

    icnListing = ctk.CTkLabel(frmListing, text="+", font=("Segoe UI", 32, "bold"), text_color='red', bg_color='transparent')
    icnListing.grid(row=0, column=0, padx=(20,20), pady=(5, 5))

    imgFilter = ctk.CTkLabel(tabLibrary, image = ctk.CTkImage(Image.open(os.path.join(dirAssets, 'IconFilter.png')), size = (40, 40)) , text = '') # Image
    imgFilter.grid(row = 2, column = 2, pady = 10, padx = 40, sticky = 'e')

    drpFilter = ctk.CTkOptionMenu(tabLibrary, values = ['Recent', 'Name', 'Series', 'Lended'], font=('Impact', 24), width=200, height=50, command = OwnedFilter)
    drpFilter.grid(row = 2, column = 3, pady = 10, padx = 40, sticky = 'w')

    lblAddListing = ctk.CTkLabel(frmListing, text="ADD LISTING", font=("Segoe UI", 20, 'bold'), text_color='gray14', bg_color='transparent')
    lblAddListing.grid(row=0, column=1, padx=(0,20), pady=0)
    lblAddListing.grid_remove()

    icnHelp = ctk.CTkLabel(tabLibrary, image = ctk.CTkImage(Image.open(os.path.join(dirAssets, 'IconHelp.png')), size = (40, 40)) , text = '', fg_color='transparent')
    tooltip = HelpLabel(icnHelp, 'Red Listings are borrowed games\nGrey Listings are lent games\nBlack Listings are owned games')
    icnHelp.grid(row=0, column=3, padx=(20,20), pady=(5, 5))

    def LstClicked(event=None):
        subprocess.Popen([sys.executable, os.path.join(dirWindows, "TabAddListings.py")])     # Launches another the add Library
        tabLibrary.destroy() # Closes the current window
        
    def OnHover(event=None):
        lblAddListing.grid()
    def OnLeave(event=None):
        lblAddListing.grid_remove()
    
    frmListing.bind("<Enter>", OnHover)
    frmListing.bind("<Leave>", OnLeave)
    icnListing.bind("<Enter>", OnHover)
    lblAddListing.bind("<Enter>", OnHover)
    frmListing.bind("<Button-1>", LstClicked)
    icnListing.bind("<Button-1>", LstClicked)
    lblAddListing.bind("<Button-1>", LstClicked)
    tabLibrary.mainloop()

    