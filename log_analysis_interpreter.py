from lark import Lark
from evaluator import Evaluator
import logging
import os

class LogAnalysisInterpreter:
    
    def __init__(self):
        try:
            with open('log_analysis_grammar.lark', 'r') as grammar_file:
                self.grammar = grammar_file.read()
            self.parser = Lark(self.grammar, parser='lalr', transformer=Evaluator())
            self.logger = self._setup_logger()
        except FileNotFoundError:
            raise FileNotFoundError("Grammar file 'log_analysis_grammar.lark' not found.")
        except Exception as e:
            raise RuntimeError(f"Error initializing interpreter: {str(e)}")
    
    
    def _setup_logger(self):
        logger = logging.getLogger('LogAnalysisInterpreter')
        logger.setLevel(logging.DEBUG)
        export_dir = 'log_analysis_logs'
        os.makedirs(export_dir, exist_ok=True)
        full_path = os.path.join(export_dir, 'log_analysis_interpreter.log')
        fh = logging.FileHandler(full_path)
        fh.setLevel(logging.INFO)   
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)   
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)   
        logger.addHandler(fh)
        logger.addHandler(ch)
        return logger

    def evaluate(self, expression):
        try:
            for line in expression.strip().split('\n'):
                result = self.parser.parse(line)
                self.logger.info(f"Executed: {line}")
                self.logger.info(f"Result: {result[-1]}")
                print()
            return"Execution completed."
        except Exception as e:
            if not line.lower().endswith('.log);'):
                self.logger.error(f"Error at line '{line}': Only .log files are allowed.")
            else:
                self.logger.error(f"Error at line '{line}': {e}")

if __name__ == "__main__":
    try:
        interpreter = LogAnalysisInterpreter()
        
        with open('log_analysis_script.sla', 'r') as script_file:
            script = script_file.read()
        
        print("Executing Log Analysis Script:")
        results = interpreter.evaluate(script)

        if results is None:
            pass
        else:
            print(results)
    
    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")