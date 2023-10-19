# PolicyTimeMachine

- [Installation](#installation)
- [Functions & How to Use](#functions--how-to-use)
  - [Function 1: Scraping Historical Data](#function-1-scraping-historical-data)
  - [Function 2: Scraping Up-to-date Data](#function-2-scraping-up-to-date-data)
  - [Function 3: Comparing the Scraped Data](#function-3-comparing-the-scraped-data)
  - [Running Progress](#running-progress)
- [Storage of the Scraped and Compared Files](#storage-of-the-scraped-and-compared-files)

## Installation

**For Windows users:**
1. Install the package and unzip it.
2. Open the "app_windows" folder and its subfolder.
3. Run the exe file.

**For MacOS users:**
1. Install the package and unzip it.
2. Open the "python codes" folder.
3. Run the Py file.

## Functions & How to Use

<img src="https://github.com/scarlettsun86/Plots/blob/addfb10b3389a330db9d69940bc5962dadf1b17d/Interface.png" alt="Interface" width="50%">

There are three functions available in this application, listed as three columns on the interface. 
The upper side of the columns is the operating area, which includes scraping/comparing options, execution buttons, progress bars, and information bars. 

Two of the functions are for scraping, and the remaining one is for comparing the scraped files with past files to identify changes in the policies. 
If changes are detected, an HTML file will be generated to highlight the differences between the two versions using red, green, and yellow colors.

### Function 1: Scraping Historical Data
 
This function is currently under development.

### Function 2: Scraping Up-to-date Data

`Step 1:` Select the targeted platform or select "all" to scrape all the platforms' policies.

`Step 2:` Click the "Scraping!" button.

### Function 3: Comparing the Scraped Data

`Step 1:` Select the "All_platform" option.

`Step 2:` Click the "Comparing!" button.

### Running Progress
| ![Processing](https://github.com/scarlettsun86/Plots/blob/addfb10b3389a330db9d69940bc5962dadf1b17d/Processing.png) |![Finished](https://github.com/scarlettsun86/Plots/blob/addfb10b3389a330db9d69940bc5962dadf1b17d/Finished.png) |
|-----------------|-------|

**Processing:** The progress bar will start scrolling, and the text "downloading/comparing, please wait" will appear below the progress bar. 
The information bar at the bottom will display the platform name, policy name, and date.

**Finished:** When the process is finished, the progress bar will stop scrolling, and the text "Finished!" will appear below the progress bar.

## Storage of the Scraped and Compared Files

After running the application, three folders will be generated: "Data_DayByDay", "Data_DayByDay_combine", and "Data_ComparePolicies". 

**Data_DayByDay** 

| ![CsvFolder](https://github.com/scarlettsun86/Plots/blob/addfb10b3389a330db9d69940bc5962dadf1b17d/CsvFolder.png) | ![CSV](https://github.com/scarlettsun86/Plots/blob/addfb10b3389a330db9d69940bc5962dadf1b17d/CSV.png) |
|----------------|----------|

This folder will contain 50 sub-folders named after the platforms after scraping the policies of all platforms. 
Within each sub-folder, the scraped data is stored as CSV files using a dataframe structure. 
The files are named following the pattern "platform name + policy name + date of scraping", and the dataframe has 4 columns and 1 row, with columns for "platform", "date", "url", and "content".

**Data_DayByDay_combine** 

The files in this folder contain multiple rows and 4 columns. 
They are named using the format "platform name + policy name". 
The columns represent "platform", "date", "url", and "content", and the rows represent different versions of policies.

**Data_ComparePolicies**

This folder will contain 50 sub-folders named after the platforms after scraping the policies of all platforms.
Each sub-folder contains HTML files named using the format "platform name + sequence numbers + dates".

| ![HtmlFolder](https://github.com/scarlettsun86/Plots/blob/addfb10b3389a330db9d69940bc5962dadf1b17d/HtmlFolder.png) | ![HTML](https://github.com/scarlettsun86/Plots/blob/addfb10b3389a330db9d69940bc5962dadf1b17d/HTML.png) |
|-----------------|-----------|

These HTML files illustrate the differences between two versions of policies. 
The left-hand side shows the old version, and the right-hand side shows the new version. 
Deleted parts are highlighted in red, added parts in green, and changed parts in yellow.

