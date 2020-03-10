import sys
import os
import argparse

try:
    import pandas as pd
except ImportError:
    sys.exit("~ Make sure you install pandas. Run `pip install pandas` and try this again ~")



argparser = argparse.ArgumentParser()
# If you're getting "pandas.errors.ParserError: Error tokenizing data. C error" use -engine python
argparser.add_argument('-engine', nargs='?', default="c", help="Set to 'c' if you're getting Error tokenizing data errors")
argparser.add_argument('-break_on_errors', nargs='?', default=True, help="Default behavior is to break on errors. Set to false if you dgaf")
argparser.add_argument('-output_filename', nargs='?', default="! Combined_file.csv", help="If you want an output filename other than the default")

args = argparser.parse_args()


def detect_boolean(v):

    if type(v) == type(True) and v:
        return True
    if type(v) == type(True) and not v:
        return False
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def combine_csvs():
    list_of_files = [f for f in os.listdir('.') if os.path.isfile(f) and ".csv" in f and f != args.output_filename]
    print(f"\nFiles that will be concatenated are: {list_of_files} \n")

    original_df = pd.DataFrame()
    for file in list_of_files:
        df = pd.read_csv(file, keep_default_na=False, engine=args.engine, error_bad_lines=detect_boolean(args.break_on_errors))
        original_df = pd.concat([original_df, df], axis=0, ignore_index=True, sort=False)

    original_df.to_csv(args.output_filename, index=False)
    print(f"Combination process is finished. Output file is called: '{args.output_filename}'. It has {original_df.shape[0]} rows and {original_df.shape[1]} columns \n")

if __name__ == "__main__":
    combine_csvs()
