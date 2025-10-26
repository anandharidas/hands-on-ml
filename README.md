# Hands-On Machine Learning - Housing Data Pipeline

This project is part of a hands-on machine learning course that focuses on real-world data processing and analysis. The initial phase involves downloading, extracting, and loading housing market data for further analysis and machine learning tasks.

## Project Structure

```
hands-on-ml/
├── requirements.txt              # Python dependencies
├── README.md                    # This file
├── setup_env.sh                 # Environment setup script
└── end-to-end/
    └── get/
        └── get_data.py          # Data fetching and loading script
```

## What This Project Does

The `get_data.py` script automates the process of:

1. **Downloading Data**: Fetches the California housing dataset (in TAR.GZ format) from a remote URL
2. **Extracting Data**: Automatically extracts the compressed archive to local storage
3. **Loading Data**: Loads the housing data into a pandas DataFrame for analysis
4. **Displaying Preview**: Shows the first few rows of the dataset

This is the first step in an end-to-end machine learning pipeline that will eventually include:
- Data exploration and visualization
- Feature engineering
- Model training
- Model evaluation and deployment

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone or navigate to the project directory:**
   ```bash
   cd /Users/anandharidas/python/hands-on-ml
   ```

2. **Run the setup script to create a virtual environment:**
   ```bash
   bash setup_env.sh
   ```

   Or manually:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   pip install -r requirements.txt
   ```

3. **Run the data fetching script:**
   ```bash
   python end-to-end/get/get_data.py
   ```

### Using the Virtual Environment

**Activate the virtual environment:**
```bash
source venv/bin/activate
```

**Deactivate when finished:**
```bash
deactivate
```

## Dependencies

- **pandas**: Data manipulation and analysis library for Python

## Data Source

The housing dataset is downloaded from:
- URL: https://github.com/ageron/data/raw/main/housing.tgz
- This dataset contains information about California housing districts

## Next Steps

After successfully downloading the data, you can proceed with:
1. Data exploration and cleaning
2. Data visualization
3. Feature engineering
4. Model training and evaluation

## Notes

- The data will be stored in the `datasets/` directory after running the script
- The script automatically handles directory creation
- Subsequent runs will skip the download if the data already exists

## License

This is an educational project following the "Hands-On Machine Learning" book by Aurélien Géron.
