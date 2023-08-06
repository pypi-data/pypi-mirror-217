Certainly! Here's an updated README file for your DataScrub package:

---

# DataScrub

DataScrub is a Python package that provides powerful data cleaning and preprocessing capabilities for pandas DataFrames. It offers a collection of functions and utilities to facilitate data cleaning tasks, handling missing values, standardizing data formats, and more. With DataScrub, you can streamline your data preparation process and ensure the quality and consistency of your datasets.

## Installation

DataScrub can be easily installed using pip. Simply run the following command:

```shell
pip install datascrub
```

Make sure you have Python 3.7 or above installed on your system.

## Usage

To use DataScrub in your Python projects, import the package and create an instance of the `DataClean` class:

```python
from datascrub import DataClean
import pandas as pd

# Create a DataFrame
data = pd.read_csv("data.csv")

# Create an instance of DataClean
cleaner = DataClean(data)

# Call the available methods to clean and preprocess your data
cleaned_data = cleaner.prep(clean='all', missing_values={}, perform_scaling_normalization_bool=False,
                            explode={}, parse_date=[], translate_column_names={})
```

The `DataClean` class takes a pandas DataFrame or a file path as input. You can then use the various methods available in the class to clean and preprocess your data.

Refer to the [documentation](https://github.com/samuelshine/datascrub) for detailed information on available methods and usage examples.

## Contributing

Contributions to DataScrub are welcome! If you encounter any bugs, have suggestions for improvements, or would like to add new features, please open an issue or submit a pull request on the [GitHub repository](https://github.com/samuelshine/datascrub).

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/samuelshine/CleanMyData/blob/main/LICENSE.txt) file for more information.
