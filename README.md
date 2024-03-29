# <img width="40" height="40" src=icon.jpg/>TakeawaySim
![GitHub top language](https://img.shields.io/github/languages/top/glcas/TakeawaySim) ![GitHub](https://img.shields.io/github/license/glcas/TakeawaySim) ![GitHub repo size](https://img.shields.io/github/repo-size/glcas/TakeawaySim?color=yellow)  
a takeaway simulation system
## What's this?
This is a food delivery simulation program with a graphical user interface.  
In the program, user is supposed to be a manager of the delivery corporation, who is resposible for the food delivery in a specific area(9*9 units). The user can employ delivery men by clicking the button on the screen, and replace consumers ordering food by clicking a restaurant unit and a home unit in succession. The orders' dispatch and delivery are processed by the program.  
While the system is running, the program is able to update the capital, duration and information of each delivery man in real time. And react by the user's action and positions of delivery men immediately.
## Introduction
### Libraries Included
The program uses following libraries:  
* **[pygame](https://github.com/pygame/pygame)**  
  Use pygame to realize the main GUI & animation.
* **tkinter**  
  Use tkinter to realize information windows.
### Core Algorithm
Because of the uncertainty of orders, the program take a strategy like `Greedy Algorithm` to dispatch orders and decide delivery men's routes.  
* Order Allocation  
  New order is allocated to the man that has nothing to do. If every man is on his way, the order will be allocated to who can reach the order's restaurant without extra effort. If no man meets above requiements, the order will be allocated to the last man.  
  In additon, the order is allocated to one man only if he reach the order's restaurant. That's to say, order allocation just means let everyone has something todo.  
  The codes realize above features start from [line 606](https://github.com/glcas/TakeawaySim/blob/master/main.pyw#L606)  and end at line 640. 
  
* Path Decision  
    A coordinate system is set in the program, every units has its own coordinate and that's what delivery men can see. Each delivery man has a `"Reachable Destination Queue"`, which decides the man's route. The queue is dynamic, sorted by the coordinates of the man and destinations, always choosing the shortest path for the man to reach destinations in the queue at that time.  

    The following function and methods realize the feature:
    * function [ontheWayAnalysis](https://github.com/glcas/TakeawaySim/blob/master/main.pyw#L265 "Line 265")
    * method [decideDirection](https://github.com/glcas/TakeawaySim/blob/master/main.pyw#L79 "Line 79") (belongs to class `man`)
    * method [arrive](https://github.com/glcas/TakeawaySim/blob/master/main.pyw#L183 "Line 183") (belongs to class `man`)
### User Interface Design
The icons used in the program all come from **Microsoft Office**.  
The font used in the program is **等线** by Beijing Founder Electronics Co.,Ltd..
## To Do List
* delivery men can run out of the window(only up & down borders), caused by algorithm
## Thanks
This is my project of general education course *`Computer Algorithm and Program`*, which is lectured by Professor Dai Bo, University of Electronic Science and Technology of China.  
The idea of this design completely comes from Mrs. Zhang Yanmei, Beijing University of Posts and Telecommunications.  
Thanks to these venerable teachers!
## By the way
    I don't konw why I create the branch with the name and I'm typing this words.
    I'm just following the 'Hello World' guidance by Github.
I wrote these words because this is my first repository and just as what I said, I followed the beginners guidance. However, I want to use the repo for my takeaway simulation system(though it's a shame to call it "sys") when I created the repository, and that's how the repo's name came.   
Now, I want to save this history.
