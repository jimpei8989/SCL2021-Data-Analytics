# Shopee Code League 2021 - Data Analytics

> Multi-Channel Contacts Problem

### About us

- Team Name: _HAMSTERR_

### Directory Tree

```
HAMSTERR
├── README.md
├── main.py
└── output.csv
```

- README - the doucment here
- main.py - the program that solves the task
- output.csv - the output csv

### How to run our script?

#### Help message

```
usage: main.py [-h] [--data_json DATA_JSON] [--output_csv OUTPUT_CSV]

optional arguments:
  -h, --help            show this help message and exit
  --data_json DATA_JSON
  --output_csv OUTPUT_CSV
```

#### Example

```
python3 main.py --data_json contacts.json --output_csv output.csv
```

- The program reads the json file `contacts.json` in current directory and output `output.csv` in the current directory.

### Environment

- Python **3.9.0**
- Requirements
  - pandas **1.2.2**
