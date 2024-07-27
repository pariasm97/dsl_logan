# Logan: A Domain-Specific Language for Log Analysis

Welcome to the Logan tutorial! <br />
<br />
Logan is a domain-specific language (DSL) designed specifically for log analysis. With Logan, you can easily load, filter, search, summarize, and export log data using a simple, expressive syntax. Built with Python and the Lark parsing library.

 In this tutorial, you will learn how to set up Logan, write scripts, and use its commands to effectively analyze log files.

 By the end of this tutorial, you will be able to:

- Set up Logan in your development environment
- Write scripts using Logan's DSL syntax
- Use Logan's commands to perform various log analysis tasks

## Prerequisites

- Python installed on your machine
- Lark library installed (pip install lark-parser)
- Basic knowledge of Python

## Setup

### Clone the Repository:
Clone the Logan repository or download the project files to your local machine.

```
git clone https://github.com/pariasm97/dsl_logan.git
```

### Project Structure:
Your project should have the following structure: <br />

log_analysis/ <br />
├── evaluator.py <br />
├── log_analysis_grammar.lark <br />
├── log_analysis_interpreter.py <br />
├── logs/ <br />
│   └── logs.log <br />
├── log_analysis_script.sla <br />
└── exports/ <br />

### Install dependencies
Ensure you have the Lark parser installed:
```
pip install lark
```

## Writing a Logan Script
Logan scripts use a simple syntax to load log files, filter by date, search for terms, summarize log data, and export results. Here is an example script *log_analysis_script.sla*:

```
load(logs.log);
all_errors = search(ERROR, logs.log);
export(from=all_errors, to=error_logs.log);
recent_logs = filter_by_date('2024-07-20', '2024-07-25', logs.log);
summarize(recent_logs);
info_logs = search(INFO, recent_logs);
export(from=info_logs, to=info_logs.log);
count_by_level(logs.log);
```
> [!IMPORTANT]
> **Logan Specifications**
> - All commands end with *;*
> - All commands have parenthesis to enclose the parameters.
> - All commands should be written in lower case.
> - Only works with .log files.
> - Only dates need to be enclosed by quotes.
> - Date format should be YYY-mm-dd for the commands and on the log file.
> - Paremeters *from* and *to* on the export command are mandatory.

## Commands Overview
- **load(filename.log):** Loads the specified log file. It is needed every time a script is run to load the information.
- **filter_by_date('start_date', 'end_date', source):** Filters log entries by date range.
- **search(term, source):** Searches for log entries containing the specified term.
- **summarize(source):** Summarizes log data, providing total entries, date range, log level counts, and most common messages.
- **count_by_level(source):** Counts log entries by log level. On this version it suports the following levels: INFO, ERROR, DEBUG, WARN.
- **export(from=source, to=filename.log):** Exports the specified source to a new log file on the exports folder.

## Running The Interpreter
**1. Prepare Log File** <br />
   Ensure you have a log file in the logs/ directory, for example, logs.log. <br />
   <br />
**2. Create or Modify the Script** <br />
   Edit log_analysis_script.sla to define the log analysis tasks. <br />
   <br />
**3. Run the Interpreter** <br />
   Execute the interpreter to run your Logan script
   <br />
   ```
   python log_analysis_interpreter.py
   ```

## Example Use Case

**1. Loading Logs:**<br />
The load command loads log entries from a specified log file.
```
load(logs.log);
```

**2. Searching for Errors:**<br />
The search command searches for log entries containing the term "ERROR" and stores it on the all_errors variable.
```
all_errors = search(ERROR, logs.log);
```

**3. Exporting Results:**<br />
The export command exports the search results to a new log file on the exports folder. On the example we are exporting the all_errors variable from the command before and exporting only the logs with ERROR level.
```
export(from=all_errors, to=error_logs.log);
```

**4. Filtering by Date:**<br />
The filter_by_date command filters log entries by a specified date range and stores it on the recent_logs variable.
```
recent_logs = filter_by_date('2024-07-20', '2024-07-25', logs.log);
```

**5. Summarizing Logs:**<br />
The summarize command provides a summary of the log entries. On the example it is going to provide a summary just for the logs that are in the recent_logs variable. The summary can be also store on a variable and be exported to a log file.
```
summarize(recent_logs);
```

**6. Counting Log Levels:**<br />
The count_by_level command counts log entries by their log level (INFO, ERROR, etc.).
```
count_by_level(logs.log);
```

