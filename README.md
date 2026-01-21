# Moral Reasoning and Moral Values: A Moderation Analysis

## Project Overview

This repository contains the data analysis code and materials for a psychological research project investigating the relationship between deliberative/intuitive moral reasoning and perceived wrongness of moral violations. Specifically, we examine how this relationship is moderated by whether moral vignettes target primary or secondary moral values.

## Table of Contents

- [Installation](#installation)
- [Project Structure](#project-structure)
- [Data Description](#data-description)
- [Usage](#usage)
- [Ethics and Compliance](#ethics-and-compliance)
- [Contact](#contact)

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for Python environment management. Follow these steps to set up the project:

### Prerequisites

- Python 3.12
- uv package manager

### Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone [repository-url]
   cd moral-reasoning-2026a
   ```

2. **Install uv** (if not already installed):

3. **Create and activate the virtual environment:**
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies:**
   ```bash
   uv sync
   ```

## Project Structure

```
moral-reasoning-2026a
├── README.md
├── pyproject.toml
├── uv.lock
├── .gitignore
├── .python-version
├── data/
│   ├── raw/                    # Original, unprocessed data
│   │   └── 01_raw_data_all.csv
│   ├── processed/              # Cleaned and processed data
│   │   ├── 01_short_form_data.csv                             # Survey data
│   │   ├── 01_long_form_data.csv                              # Experiment data (all)
│   │   ├── 02_long_df_unstandardized_one_primary.csv          # Untandardized experiment data (participants with one primary norm)
│   │   └── 02_long_df_standardized_one_primary.csv            # Standardized experiment data (participants with one primary norm)
│   └── survey_descriptions.yaml                               # Details on all surveys
├── src/
│   ├── __init__.py
│   ├── charts/
│   │   ├── __init__.py
│   │   └── assumptions.py             # Plots for Q-Q residuals
│   ├── descriptives/
│   │   ├── __init__.py
│   │   ├── descriptive_stat.py        # Functions for extracting descriptives
│   │   └── scale_stat.py              # Reliability and distribution for scales
│   ├── models/
│   │   ├── __init__.py
│   │   ├── regression.py              # Bootstrapped regression implementation
│   │   ├── wrongness_model.r          # Wrongness modeling
│   │   ├── certainty_model.r          # Certainty modeling
│   │   └── processing_type_model.r    # Wrongness modeling (processing type X value relevance)
│   └── util/
│       ├── __init__.py
│       ├── custom_types.py            # Custom types
│       └── value_labels.py            # Demographic variable labels
├── notebooks/
│   ├── 01 Missing Data Exploration.ipynb
│   ├── 02 Descriptive Analysis & Data Prep.ipynb
│   ├── 03 Regression Analyses - MFQ.ipynb
│   ├── 04 Regression Analysis - Primary Moral Norm.ipynb
│   └── 05 Visualization - Interaction.ipynb
└── results/
    ├── coefficients/                  # Stored coefficients of the models
    └── figures/                       # Saved figures used in the article
```

## Data Description
### Variables
#### Dependent Variables (main analyses)
- **Perceived Wrongness**
   - Perceived wrongness of social situations.
   - One item, Likert's scale
   - Range: 1-5
- **Certainty**
   - Certainty in perceived wrongness of social situations.
   - One item, Likert's scale
   - Range: 1-7

#### Independent Variables
- **CTSQ subscale scores**:
   - Average scores on CTSQ subscales
   - Range: 1-5 
- **CRT correct**:
   - The number of correctly answered items on the CRT task.
   - Range: 0-8 
- **CRT heuristic**:
   - The number of "heuristically" answered items on the CRT task.
   - Range: 0-8 

#### Moderating Variables
- **Vignette Type**
   - Whether vignette targets a primary or a secondary moral norm.
   - Extracted by getting participant's largest score on MFQ subscales.
   - Binary: 0 represents secondary norm, 1 represents primary norm.

## Usage
```bash
# Activate the environment
source .venv/bin/activate
```

### Using Jupyter Notebooks
```bash
# Start Jupyter Lab
jupyter lab

# Navigate to notebooks/ directory and explore the analysis.
```

## Ethics and Compliance
### Ethics Approval
- **Institution**: Faculty of Philosophy, University of Belgrade
- **Protocol**: https://www.komocetis.f.bg.ac.rs/projekat.php?p=471
- **Approval Date**: 20.05.2024.

### Data Protection
- All participant data is de-identified
- No personally identifiable information in this repository

### Open Science Practices
- Data sharing: All the data used in this study is available in this repository.
- Code sharing: This repository serves as complete analysis code

## Contact
**Principal Researcher**: Irena Pavlović  
**Email**: irena.pavlovic@live.com  
**Institution**: Faculty of Philosophy, University of Belgrade  
**ORCID**: 0009-0005-7424-9065

For questions about the analysis code, please open an issue on GitHub or contact s.dg.emir@gmail.com.

For questions about the research methodology or data, please contact irena.pavlovic@live.com.

---