# Master Thesis
Easy to use application for data analysis. Uses python-weka-wrapper3 for importing some data mining algorithms from Weka (like JRip and Apriori, which are not implemented in sckit-learn). In our work we use this application for analysis of NBA statistics but it can be used for any kind of numeric and nominal data.

Requirements:
- Python 3
  - python-weka-wrapper3
    - javabridge (>= 1.0.14)
    - matplotlib (optional)
    - pygraphviz (optional)
    - PIL (optional)
  - pandas
  - liac-arff
- Oracle JDK 1.8+

Uses:
- Weka (3.9.2)

## Installation of requirements
Following step-by-step installation process is for Linux platforms.
- Installation of python-weka-wrapper3:  
  Install c/c++ compiler  
  ```shell
  sudo apt-get install g++
  ```
  Install compile Python modules and python setuptools  
  ```shell
  sudo apt-get install build-essential python3-dev
  sudo pip3 install setuptools
  ```
  Install numpy, pil, matplotlib and pygraphviz 
  ```shell
  sudo apt-get install python3-pip python3-numpy  
  sudo apt-get install python3-pil python3-matplotlib python-pygraphviz  
  ```
  Istall OpenJDK  
  ```shell
  sudo apt-get install default-jdk
  ```
  Install javabridge and python-weka-wrapper3  
  ```shell
  sudo pip3 install javabridge  
  sudo pip3 install python-weka-wrapper3
  ```
- Installation of pandas:  
  ```shell
  sudo pip3 install pandas
  ```
- Installation of liac-arff:
  ```shell
  sudo pip3 install liac-arff
  ```

For installation on other platforms, last two steps should be the same and instructions for first step can be find in official documentation of python-weka-wrapper3.

Now clone the application and you are ready to use it.
```git
git clone https://github.com/istancin/master-thesis.git
```

## Instruction manual
Position yourself in src folder and type:
```shell
python3 main.py
```
This will raise an exception because there are some required arguments we need to pass through command line in order to get some results.
- __Required command line arguments:__
  - __*"--algorithm"*__ - tells application which algorithm to use. Currently supported __"JRip"__ and __"Apriori"__
  - __*"--path"*__ - path to the dataset
  - __*"--filetype"*__ - filetype of dataset given with path argument. Currently supported __"csv"__ and __"arff"__  
  
  ```shell
  python3 main.py --algorithm JRip --path test.csv --filetype csv
  ```
  Above command is valid and it will not raise exception by default, __BUT__, in our implementation JRip always uses last feature in dataset as a class label, so if in dataset (given with path) last label is not nominal JRip will raise exception. For preventing this kind of error there is few command line arguments that are not required but we strongly recommend you to use them.
- __Recommended command line arguments:__
  - __*"--label"*__ - name of a class label. Api will put given label as last in dataset (as class label is always last label in our implementation)
  - __*"--L"*__ - if loading data from csv this command will force given attributes to be nominal. Syntax is, e.g. __"--L ATTR1:1,0"__, which will force attribute with name ATTR1 to be nominal and have values of 1 or 0. For more detailed explanation see csv_loader_parser function in parsers.py or Weka documentation for CSVLoader class. 
  Now command could look something like this:
  ```shell
  python3 main.py --algorithm JRip --path test.csv --filetype csv --label ATTR1 --L ATTR1:1,0
  ```
  That command would print JRip ruleset and it's evaluation to console. ATTR1 would be class label and it would have only 1 or 0 values. If we want to save our results into file we can do it by adding other argument 
  - __*"--rusultdest"*__ - path to file in which we want to store results of our algorithm. Results will be appended at the end of file. If this argument is not given, results will be printed to console.
- __Data manipulation arguments:__
  - __*"--excludecol"*__ - if we want to exclude some columns from dataset we use this command, e.g. __"--excludecol ATTR1,ATTR2"__ will remove columns with names ATTR1 and ATTR2 from dataset.
  - __*"--includecol"*__ - if we want to include only some columns from dataset we use this command, e.g. __"--includecol ATTR1,ATTR2"__ will remove all columns from dataset except columns with names ATTR1 and ATTR2.  
  NOTE: --includecol and --excludecol can not be used at the same time!
  - __*"--excluderow"*__ - if we want to remove some rows based on some condition we can use this command, e.e. __"--excluderow ATTR1==1;ATTR2<50"__ will remove all rows where attribute ATTR1==1 and all rows where attribute ATTR2<50. We can pass as much conditions as we want. For now there is no support for situations where two conditions needs to be valid at the same time.
  - __*"--L"*__ - this argument is already explained. In case we have class label with many values, but we are interested only in one and all the other values want to put "in the same basket", we can do it with this command. For example, __"--L ATTR1:1,rest"__ will do exactly that, class label ATTR1 will keep value 1 and all the rest values will be replaced with 'rest'
  - __*"--discretize"*__ - if we want to discretize data we can use __"--discretize yes"__. Default is 'no'. Weka's unsupervised discretization function is used for discretization. For more options for discretization look at unsuprovised_discretize_parser function in parsers.py of in official Weka documentation.
- __Other offtenly used arguments:__
  - __*"--Njrip"*__ - argumment for JRip algorithm. This will be parsed to __"-N"__ option for weka implementation of JRip. Set the minimal weights of instances within a split.
  - __*"--Capriori"*__ - argument for Apriori algorithm. It will be parsed to __"-C"__ option for Weka implementation of Apriori. It's the minimum confidence of a rule.  

There is many more arguments that can be passed, but these are most important. For all other possible arguments see parsers.py. In examples we will show some cases of usage.

## Examples of usage
We will show some examples of usage on test_dataset.csv. Dataset consists of team player tracking statistics of every game (almost every, 8 games are missing) in 2017-18 NBA season. Dataset has 24 attributes and 2444 records, two records per game (for each team one record).  
### JRip example:
```shell
python3 main.py --algorithm JRip --path test_dataset.csv --filetype csv --label WINNER --L WINNER:1,0 --excludecol PTS,FG_PCT,WINS,WIN_GROUP --excluderow WIN_GROUP==36-49;WINS<25 --Njrip 100
```
Application will print out following result to console:  
```text
========== JRip =========
Command line:
	['/home/linuxmint/main.py', '--algorithm', 'JRip', '--filetype', 'csv', '--path', '/home/linuxmint/Downloads/test_dataset.csv', '--label', 'WINNER', '--L', 'WINNER:1,0', '--excludecol', 'PTS,FG_PCT,WINS,WIN_GROUP', '--excluderow', 'WIN_GROUP==36-49;WINS<25', '--Njrip', '100']
Start time: 
	2018-05-08 16:43:05.426464
Header of dataset:
	['AST', 'CFGA', 'CFGM', 'CFG_PCT', 'DFGA', 'DFGM', 'DFG_PCT', 'DIST', 'DRBC', 'FTAST', 'GAME_ID', 'ORBC', 'PASS', 'RBC', 'SAST', 'TCHS', 'TEAM_ABBREVIATION', 'UFGA', 'UFGM', 'UFG_PCT', 'WINNER']
Arguments of JRip algorithm: 
	weka.classifiers.rules.JRip -F 3 -N 100.0 -O 2 -S 1

JRIP rules:
===========

(UFG_PCT <= 0.431) => WINNER=0 (418.0/146.0)
 => WINNER=1 (559.0/186.0)

Number of Rules : 2


Correctly Classified Instances         645               66.0184 %
Incorrectly Classified Instances       332               33.9816 %
Kappa statistic                          0.3142
Mean absolute error                      0.1794
Root mean squared error                  0.2995
Relative absolute error                 89.7835 %
Root relative squared error             94.8996 %
Total Number of Instances              977     
```
First section of result gives us information about executed command line, time of execution, attributes selected to data and parameters for selected algorithm (JRip in this case).  
Second section shows us rules generated by algorithm.  
Third section shows us evaluation of generated JRip rules.  

__Let's comment parts of command line arguments:__
```shell
--label WINNER --L WINNER:1,0
```
This ensures that the class label WINNER is last attribute in data and that it is nominal with values of 1 or 0.
```shell
--excludecol PTS,FG_PCT,WINS,WIN_GROUP
```
This excludes PTS, FG_PCT, WINS and WIN_GROUP attributes from dataset. If we take a look to result and printed header of dataset, we can see that there is no these attributes.
```shell
--excluderow WIN_GROUP==36-49;WINS<25
```
This excludes rows where WIN_GROUP is equal to '36-49' and where WINS are less than 25. If we take a look at the evaluation part of result, we can see that total number of instances is 977, while original dataset had 2444 instances.
```shell
--Njrip 100
```
This is parameter for JRip algorithm (-N). Set the minimal weights of instances within a split.

### Apriori example:
```shell
python3 main.py --algorithm Apriori --path test_dataset.csv --filetype csv --label WIN_GROUP --L WIN_GROUP:50+,rest --discretize yes --includecol AST,SAST,FTAST,PASS,TCHS,DST,UFGM,UFGA,UFG_PCT,WINNER,WIN_GROUP --Capriori 0.5 --Napriori 15 
```
Application will print out following result to console:  
```text
========== Apriori =========
Command line:
	['/home/linuxmint/main.py', '--algorithm', 'Apriori', '--filetype', 'csv', '--path', '/home/linuxmint/Downloads/test_dataset.csv', '--label', 'WIN_GROUP', '--L', 'WIN_GROUP:50+,rest', '--includecol', 'AST,SAST,FTAST,PASS,TCHS,DST,UFGM,UFGA,UFG_PCT,WINNER,WIN_GROUP', '--discretize', 'yes', '--excluderow', 'WIN_GROUP==36-49;WINS<25', '--Capriori', '0.5', '--Napriori', '15']
Start time: 
	2018-05-08 17:19:23.586676
Header of dataset:
	['AST', 'FTAST', 'PASS', 'SAST', 'TCHS', 'UFGA', 'UFGM', 'UFG_PCT', 'WINNER', 'WIN_GROUP']
Arguments of Apriori algorithm: 
	weka.associations.Apriori -N 15 -T 0 -C 0.5 -D 0.05 -U 1.0 -M 0.1 -S -1.0 -c -1


Apriori
=======

Minimum support: 0.2 (423 instances)
Minimum metric <confidence>: 0.5
Number of cycles performed: 16

Generated sets of large itemsets:

Size of set of large itemsets L(1): 23

Size of set of large itemsets L(2): 12

Best rules found:

 1. PASS='(303-328.4]' 535 ==> TCHS='(420-453.8]' 468    <conf:(0.87)> lift:(2.79) lev:(0.14) [300] conv:(5.4)
 2. PASS='(277.6-303]' 663 ==> TCHS='(386.2-420]' 541    <conf:(0.82)> lift:(2.26) lev:(0.14) [301] conv:(3.44)
 3. WINNER='(-inf-0.1]' 986 ==> WIN_GROUP=rest 801    <conf:(0.81)> lift:(1.11) lev:(0.04) [80] conv:(1.43)
 4. PASS='(277.6-303]' 663 ==> WIN_GROUP=rest 516    <conf:(0.78)> lift:(1.07) lev:(0.01) [31] conv:(1.21)
 5. TCHS='(420-453.8]' 664 ==> WIN_GROUP=rest 512    <conf:(0.77)> lift:(1.06) lev:(0.01) [26] conv:(1.17)
 6. TCHS='(386.2-420]' 765 ==> WIN_GROUP=rest 584    <conf:(0.76)> lift:(1.04) lev:(0.01) [24] conv:(1.13)
 7. FTAST='(-inf-0.7]' 744 ==> WIN_GROUP=rest 560    <conf:(0.75)> lift:(1.03) lev:(0.01) [16] conv:(1.08)
 8. UFGM='(19.8-23]' 693 ==> WIN_GROUP=rest 519    <conf:(0.75)> lift:(1.02) lev:(0.01) [12] conv:(1.07)
 9. UFGA='(49.5-54.8]' 592 ==> WIN_GROUP=rest 439    <conf:(0.74)> lift:(1.01) lev:(0) [6] conv:(1.04)
10. UFG_PCT='(0.441-0.4912]' 587 ==> WIN_GROUP=rest 432    <conf:(0.74)> lift:(1.01) lev:(0) [3] conv:(1.01)
11. FTAST='(0.7-1.4]' 730 ==> WIN_GROUP=rest 523    <conf:(0.72)> lift:(0.98) lev:(-0) [-10] conv:(0.94)
12. TCHS='(386.2-420]' 765 ==> PASS='(277.6-303]' 541    <conf:(0.71)> lift:(2.26) lev:(0.14) [301] conv:(2.34)
13. TCHS='(420-453.8]' 664 ==> PASS='(303-328.4]' 468    <conf:(0.7)> lift:(2.79) lev:(0.14) [300] conv:(2.52)
14. WINNER='(0.9-inf)' 1131 ==> WIN_GROUP=rest 746    <conf:(0.66)> lift:(0.9) lev:(-0.04) [-80] conv:(0.79)
15. WIN_GROUP=rest 1547 ==> WINNER='(-inf-0.1]' 801    <conf:(0.52)> lift:(1.11) lev:(0.04) [80] conv:(1.11)
```
First section in result has same information like in case of JRip algorithm.  
In second section we can see most important parameters of Apriori algorithm and rules that was generated and "evaluation" of each rule.

__Let's comment parts of command line arguments:__
```shell
--label WIN_GROUP --L WIN_GROUP:50+,rest
```
First part ensures that the class label WIN_GROUP is last attribute in data (although it is not that important for Apriori algorithm) and second part will leave 50+ label in our class attribute, while every other value (0-35 and 36-49) will replace with rest. We can see many occurrence of WIN_GROUP=rest in rules.
```shell
--discretize yes
```
This is not necessary for Apriori algorithm because it discretize data by default. We put it here just for example of usage.
```shell
--includecol AST,SAST,FTAST,PASS,TCHS,DST,UFGM,UFGA,UFG_PCT,WINNER,WIN_GROUP
```
This will include only selected attributes into dataset. If we take a look to "Header of dataset" in result, we can see that these are really only selected attributes in dataset.
```shell
--Capriori 0.5 --Napriori 15 
```
These are parameters of Apriori algorithm. First will be parsed into -C for Weka's Apriori algorithm and it sets minimal confidence level of rules. Second will be parsed into -N for Weka's Apriori algorithm and it sets maximal number of rules that we want.
