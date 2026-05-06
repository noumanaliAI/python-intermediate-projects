# Patient Management System

A simple patient management system built in Python from scratch.

## Features

* Add, view, and search patients
* Filter patients by disease
* Patient queue using Python generators
* Age statistics (mean, median, std deviation)
* Save and load patient data to/from a file
* Action logging with timestamps using a decorator

## How to Run

```
python Patient_management.py
```

## Skills Used

* Functions and decorators (`@log_action`)
* `**kwargs` for flexible patient input
* `lambda` and `filter()` for search/filtering
* Generators (`yield`) for patient queue
* `statistics` and `math` modules for age stats
* File I/O with `json` for saving/loading data
* f-strings and formatted table output
* Try/Except error handling for invalid input