from lark import v_args, Transformer
from datetime import datetime
import re
from collections import Counter
import json
import os


@v_args(inline=True)
class Evaluator(Transformer):

    def __init__(self):
        self.log_entries = []
        self.filtered_entries = []
        self.variables = {}
        self.results = []
    
    def _extract_date(self, log_entry):
        try:
            date_str = re.search(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', log_entry).group()
            return datetime.strptime(date_str, '%Y-%m-%d')
        except AttributeError:
            raise AttributeError(f"Error extracting date data in log_entry '{log_entry}': date format should be YYYY-mm-dd please review.")
        except Exception as e:
            raise Exception(f"Error parsing date in log_entry '{log_entry}': {e}")
    
    def start(self, *statement):
        return self.results
    
    def statement(self, *command):
        self.results.append(command)
        return command
    
    def command(self, cmd):
        return cmd
    
    def _is_file_loaded(self):
        if not self.log_entries:
            raise ValueError("File not loaded. Please upload file using load command.")

    def assignment(self, var, value):
        self._is_file_loaded()
        self.variables[str(var)] = value
        return f"Assigned to variable {var}"

    def load(self, filename):
        try:
            log_dir = 'logs'
            filename = f'{filename}.log'
            full_path = os.path.join(log_dir, filename)
            with open(full_path) as file:
                self.log_entries = file.readlines()
            return f"Loaded {len(self.log_entries)} entries from {filename}"
        except FileNotFoundError as e:
            return f"File {filename} Not Found: {e}."
        except IOError as e:
            return f"Error reading file {filename}: {e}"
    
    def filter_by_date(self, start_date, end_date, file_or_var):
        try:
            self._is_file_loaded()
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            if file_or_var in self.variables:
                entries = self.variables[file_or_var]
            elif self.log_entries:
                entries = self.log_entries
            else:
                raise ValueError("No log entries loaded and variable not found")
            self.filtered_entries = [
                entry for entry in entries if start_date <= self._extract_date(entry) <= end_date
            ]
            return self.filtered_entries
        except ValueError as e:
            return f"Invalid date format: {e}"
    
    def search(self, search_word, file_or_var):
        try:
            self._is_file_loaded()
            entries = self.variables.get(str(file_or_var), self.log_entries)
            self.filtered_entries = [
                entry for entry in entries if search_word.upper() in entry.upper() 
            ]
            return self.filtered_entries
        except Exception as e:
            return f"Error during search: {e}"
        
    
    def summarize(self, file_or_var):
        try:
            self._is_file_loaded()
            if file_or_var in self.variables:
                entries = self.variables[file_or_var]
            elif self.log_entries:
                entries = self.log_entries
            else:
                raise ValueError("No log entries loaded and variable not found")
        
            if not entries:
                raise ValueError("No entries to summarize")

            total_entries = len(entries)
            level_counts = self.count_by_level(file_or_var)

            start_date = self._extract_date(entries[0])
            end_date = self._extract_date(entries[-1])

            # Assuming log format contains a message at the end
            messages = [entry.split('] ')[-1] for entry in entries]
            common_messages = Counter(messages).most_common(5)

            summary = {
                'total_entries': total_entries,
                'date_range': {
                    'start_date': str(start_date),
                    'end_date': str(end_date)
                },
                'level_counts': level_counts,
                'common_messages': common_messages
            }
            self._print_summary(summary)
            return json.dumps(summary, indent=2)
    
        except Exception as e:
            return f"Error generating summary: {e}"

    
    def _print_summary(self, summary):
        # Print summary
        print("Log Summary:\n-------------")
        print(f"Total Entries: {summary['total_entries']}")
        print("Time Range:")
        print(f"- Start: {summary['date_range']['start_date']}")
        print(f"- End: {summary['date_range']['end_date']}\n")
        print("Log Level Counts:")
        for level, count in summary['level_counts'].items():
            print(f"- {level}: {count}")
        print("\nMost Common Messages:")
        for message, count in summary['common_messages']:
            print(f"- \"{message}\" ({count} times)")


    def count_by_level(self, file_or_var):
        self._is_file_loaded()
        level_list = ['INFO', 'ERROR', 'DEBUG', 'WARN']
        counts = {level: 0 for level in level_list}
        if file_or_var in self.variables:
                entries = self.variables[file_or_var]
        elif self.log_entries:
            entries = self.log_entries
        else:
            raise ValueError("No log entries loaded and variable not found")
        for entry in entries:
            for level in level_list:
                if level in entry:
                    counts[level] += 1
        return counts
    
    def export(self, file_or_var, tfilename):
        try:
            self._is_file_loaded()
            if file_or_var in self.variables:
                entries = self.variables[file_or_var]
            elif self.log_entries:
                entries = self.log_entries
            else:
                raise ValueError("No log entries loaded and variable not found")
            export_dir = 'exports'
            os.makedirs(export_dir, exist_ok=True)
            full_path = os.path.join(export_dir, tfilename + '.log')
            with open(full_path, 'w') as file:
                file.writelines(entries)
            message = f"{file_or_var} exported succesfully to {full_path}"
            return message
        except IOError as e:
            return f"Error exporting to file {tfilename}: {e}"
        except Exception as e:
            return f"Unexpected error during export: {e}"

    
    def start_date(self, stdt):
        return stdt
    
    def end_date(self, enddt):
        return enddt
    
    def filename(self, fname):
        return fname
    
    def textnum(self, tnum):
        return tnum
    
    def var(self, name):
        return str(name)

