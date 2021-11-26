# Project: Identifier Name linter


### **Name:** Sujith Reddy Dharmareddy

### **PSID:** 1965551

### **Description:**

The main aim of this project is to write a python program that takes Address of a public GitHub repository and take various files like .py, .rb, .go, .js from the url depending on the input from the user using tree-sitter package.

### **Output1 :**
We have to parse all the identifier names from that particular type of file from the above and print them in a file with their respective locations.

### **Output2 :**

Now, we need to check if all the identifier names are following the butler's naming convention rules or not. We need to print the identifier names which don't follow these convention rules with it's location and the type of rules it breaks.

### **Package installations:**
````
pip3 install tree-sitter
````
````
pip install gitpython
````

### **Command to run program:**
````
python program_python.py giturl file-extension language outputfile1 outputfile2
````
Example:

````
python program_python.py https://github.com/sujith15/TestFiles .py python Output1.txt Output2.txt
````



