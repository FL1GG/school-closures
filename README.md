# Purpose
This program is intended to increase the speed at which a user can catalog the county system school closures in the state of georgia. It does this by preloading the location for school announcement and automatically fetching it in a browser tab so it can be quickly processed by a person.

# Installation
Installation requires python3 and git

First install python if you have not done so already. On windows systems, you can type python3 into a command prompt to be brought to the app store to install it:
```pwsh
python
```

alternatively on linux simply use apt
```bash
sudo apt install python3
```

now fetch the repository
```bash
git clone https://github.com/FL1GG/school-closures.git
```

next install the requirement of the program 
```bash
cd school-closures
python3 -m pip install -r requirements.txt
```

You should be good to go.

# Running
Now we need to run the program. The syntax is as follows:
```bash
python3 run.py <date1> <date2> <etc>
```
So a command might look like
```bash
python3 run.py 'Tues 1/21' 'Mond 1/22'
```

# How to use
The browser will automatically spawn with the school page loaded. Once it does so you can input into the console the status of the school for a given date.