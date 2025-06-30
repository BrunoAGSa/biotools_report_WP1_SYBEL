# Bio.Tools Report Generator

Originally developed as part of **Work Package I of the SYBEL Project** and later expanded for broader community use, this Python-based workflow (with a convenient shell wrapper) automatically fetches bio.tools data for any topic, analyzes it in a Jupyter notebook, renders visualizations, and exports a polished PDF report.


## Installation

Before installing, we recommend creating an virtual environment (e.g. Conda).

```bash
conda create -n report_env python=3.9
conda activate report_env
```


### Clone and Install
```bash
git clone https://github.com/BrunoAGSa/biotools_report_WP1_SYBEL
cd biotools_report_WP1_SYBEL
pip install -r requirements.txt
```


## Example

Use the `run_report.sh` shell script to generate a PDF report from the report template.

### Usage

```bash
bash run_report.sh [TOPIC] [MODE] [LOAD_PATH]
```

* **TOPIC** (default: `"Systems biology"`)
  The topic to query, all available topics can be found in the [BioPortal - EDAM ](https://bioportal.bioontology.org/ontologies/EDAM?p=classes&conceptid=http%3A%2F%2Fedamontology.org%2Ftopic_0003).


* **MODE** (default: `extract_and_save`)

   * `extract` — fetch data only.
   * `extract_and_save` — fetch data **and** save it as a pickle in `data/`.
   * `load` — skip extraction and load from an existing pickle (you must supply `LOAD_PATH`).


* **LOAD\_PATH**
  Path to a previously saved pickle file (required when `MODE` is `load`).

---

### Generating a Systems Biology Report

1. **Extract data and generate a new report**

   ```bash
   bash run_report.sh "Systems biology"
   ```

   * Saves [data](data/bio_tools_systems_biology_June_30_2025.pkl) to

     ```text
     data/bio_tools_systems_biology_<Month>_<DD>_<YYYY>.pkl
     ```
   * Generates [PDF](reports/report_systems_biology_June_30_2025.pdf) at

     ```text
     reports/report_systems_biology_<Month>_<DD>_<YYYY>.pdf
     ```

2. **Regenerate from existing data**

   ```bash
   bash run_report.sh "Systems biology" load "data/bio_tools_systems_biology_<Month>_<DD>_<YYYY>.pkl"
   ```

   This uses the pickle you specify.

---

### Generating a Report for Another Topic

Because the script uses topic based search, you can generate reports for **any** topic. For example, to create a [**Plant Biology** report](./reports/report_plant_biology_June_30_2025.pdf):

```bash
bash run_report.sh "Plant biology"
```

## Additional Analysis

For each attribute section in the report, you’ll find an **Additional analysis** code cell in [`report.ipynb`](./report.ipynb). Use it to insert custom commentary or deeper insights.

```python
from IPython.display import display, Markdown

# Additional analysis
display(Markdown("""
Any additional notes can be inserted here.
"""))
```





# License

This project is licensed under the [MIT License](license.txt).

# Authors

- Bruno Sá

- Carissa Bleker

- Anže Županič

- Miguel Rocha


