import os, sys, subprocess, csv
from PIL import Image
import customtkinter as ctk
from TabListingLibrary import Listing, HelpLabel # Gets the Listing and HelpLabel class from TabListingLibrary.py (everything that isn't in __name__ == "__main__" is imported)

dirMain = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Main directory (gets the parent directory of the current file)
dirAssets = os.path.join(dirMain, 'Assets') # Asset Directory
dirWindows = os.path.join(dirMain, 'Windows') # Window Directory
dirGameInfo = os.path.join(dirMain, 'GameInformation') # Game Information Directory
with open(os.path.join(dirGameInfo, 'AllGameInformation.csv'), newline='', encoding='utf-8') as file:       # Reads all game information from a CSV file (this makes it easy to edit outside of the program)
    arrAllGames = list(csv.reader(file)) # Extracts the CSV file into an array which is a list in python
with open(os.path.join(dirGameInfo, 'GameInstanceStatus.csv'), newline='', encoding='utf-8') as file:       
    allGameInstances = [[int(value) for value in row] for row in csv.reader(file)] # borrowedInstances[0], ownedInstances[1], lendedInstances[2]
borrowedInstances, ownedInstances, lendedInstances = allGameInstances[0], allGameInstances[1], allGameInstances[2]
allInstances = ownedInstances + borrowedInstances  # Combines all instances into one list
ctk.set_appearance_mode('System')
ctk.set_default_color_theme(os.path.join(dirMain, 'themetendo.json')) # Nintendo colours dark mode
tabAddListings = ctk.CTk()
tabAddListings.geometry('700x400')
tabAddListings.resizable(False, True) # <--- Change this after Testing
tabAddListings.title('Super Smash Bros MHS | Add Listings')
tabAddListings.grid_columnconfigure((0,1,2), weight = 1)
tabAddListings.grid_rowconfigure((0,1,2,3), weight = 0)

fntHeading = ctk.CTkFont(family = 'Impact', size=72)
fntTitle = ctk.CTkFont(family = 'Segoe UI', size = 16, weight = 'bold')
fntHeading = ctk.CTkFont(family = 'Impact', size=72)
fntTitle = ctk.CTkFont(family = 'Segoe UI', size = 16, weight = 'bold')

Query = ctk.StringVar()
def Return(event=None): # Goes back to the Library
    subprocess.Popen([sys.executable, os.path.join(dirWindows, "TabListingLibrary.py")])     # Launches the ListingLibrary file
    tabAddListings.destroy() # Closes the current window

def OpenGamePicker(caller, choice): # This is a linear search
    if caller == 'Dropdown':
        if choice != 'Pick a Series': # Hides the frame if the user has not selected a series
            Query.set('')
            scrSeries.grid(row=2, column=0, columnspan=3, padx=20, pady=20, sticky='nsew', rowspan=5) 
            for child in frmSeries.winfo_children():
                child.destroy()
            filteredGames = []
            for game in arrAllGames:
                if game[1][2:] == choice: # Checks the series of the game matches the selected series and adds it to the filteredGames list
                    filteredGames.append(arrAllGames.index(game))
            gamRow = -1
            for value, entry in enumerate(filteredGames):
                lstGame = Listing(frmSeries, entry, 'add') # Creates a new Listing instance for each game in the filteredGames list
                gamCol = value % 3
                if gamCol == 0:
                    gamRow += 1
                lstGame.grid(row=gamRow, column=gamCol, padx=10, pady=5, sticky='ew')
        else:
            scrSeries.grid_remove()
    elif caller == 'Searchbar':
        query = Query.get().strip().lower()
        if query != '':
            drpGamePicker.set('Pick a Series')
            scrSeries.grid(row=2, column=0, columnspan=3, padx=20, pady=20, sticky='nsew', rowspan=5) 
            for child in frmSeries.winfo_children():
                child.destroy()
            lblNoResults = ctk.CTkLabel(frmSeries, text='No Results Found', font=('Impact', 24))
            filteredGames = []
            for game in arrAllGames:
                if query in game[2].lower(): # Checks if the search query is in the game title
                    filteredGames.append(arrAllGames.index(game))
            if not filteredGames: # If filteredGames is empty, it returns False
                lblNoResults.grid(row=0, column=0, padx=20, pady=20, sticky='nsew', columnspan=3) # Displays "No Results Found" label if no games match the search query
            else:
                lblNoResults.grid_remove()
            gamRow = -1
            for value, entry in enumerate(filteredGames):
                lstGame = Listing(frmSeries, entry, 'add') # Creates a new Listing instance for each game in the filteredGames list
                gamCol = value % 3 # This structure with gamCol and gamRow allows for a 3-column layout, marked by the %3
                gamRow = gamRow + 1 if gamCol == 0 else gamRow
                lstGame.grid(row=gamRow, column=gamCol, padx=10, pady=5, sticky='ew')
        else:
            scrSeries.grid_remove() # If searchbar search is empty/whitespace
    else:
        scrSeries.grid_remove() #Can't be called but in future changes but if the caller is not Dropdown or Searchbar it will just close

#Makes the list of series dynamically, so adding new series will not create issues
GameSeries = ['Pick a Series']
for row in arrAllGames:
    if row[1][2:] not in GameSeries:
        GameSeries.append(row[1][2:])
#Places GUI elements
btnReturn = ctk.CTkButton(tabAddListings, text='Return to Library', command=Return, width=100)
btnReturn.grid(row=0, column=0, padx=20, pady=20, sticky='nw')

lblSearch = ctk.CTkLabel(tabAddListings, text='Search for a Game', font=('Impact', 24))
lblSearch.grid(row=0, column=1, padx=20, pady=20, sticky='w')

drpGamePicker = ctk.CTkOptionMenu(tabAddListings, values = GameSeries, font=('Impact', 24), width=200, height=50, command = lambda choice: OpenGamePicker('Dropdown', choice))
drpGamePicker.grid(row=1, column=1, columnspan=2, padx=20)

scrSeries = ctk.CTkScrollableFrame(tabAddListings)
scrSeries.grid()
frmSeries = ctk.CTkFrame(scrSeries)
frmSeries.grid()
scrSeries.grid_remove()

entSearch = ctk.CTkEntry(tabAddListings, placeholder_text='Search for a Listing', textvariable=Query)
entSearch.grid(row=1, column=0, padx=(20,20), pady=(5, 5), sticky='ew')

lblOr = ctk.CTkLabel(tabAddListings, text='or', font=('Impact', 24)).grid(row=1, column=1, padx=(20,20), pady=(5, 5), sticky = 'w') # This is never used for anything so I declared and placed it in the same line

icnHelp = ctk.CTkLabel(tabAddListings, image = ctk.CTkImage(Image.open(os.path.join(dirAssets, 'IconHelp.png')), size = (40, 40)) , text = '', fg_color='transparent')
tooltip = HelpLabel(icnHelp, 'Red Listings are borrowed games\nGrey Listings are lent games\nBlack Listings are unowned games\nGreen Listings are owned games\nClick on a black/green listing to add/remove it from your library')
icnHelp.grid(row=0, column=2, padx=(20,20), pady=(5, 5))

entSearch.bind('<Return>', lambda event: OpenGamePicker('Searchbar', Query.get())) # Searchbar searches once enter is pressed

tabAddListings.mainloop()