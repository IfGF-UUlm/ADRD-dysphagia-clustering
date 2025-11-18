# ADRD Dysphagia Clustering

This GitHub repository contains the code used for the clustering analysis in the paper "Clustering analysis reveals an Alzheimer’s disease-associated swallowing pattern in geriatric patients with oropharyngeal dysphagia".

## Project Overview

pending

## Key Messages

pending

## Repository Structure

- [`analysis.ipynb`](./analysis.ipynb): Feature extraction and clustering analysis
- [`data.xlsx`](./data.xlsx): Data from the dysphagia study in geriatric patients
- [`environment.yml`](./environment.yml): Virtual environment used for the analysis
- [`LICENSE`](./LICENSE): License for this project (MIT License, as per the project's uniform approach)

## Explore the Analysis:

Open [`analysis.ipynb`](./analysis.ipynb) in GitHub to inspect feature extraction and clustering.

It is possible to download or clone the repository and create a virtual environment using conda. \
The data is included in data.xlsx, allowing the full analysis notebook to be rerun.

### Cloning the Repository
1. Open a terminal or command prompt.
2. Run the following command to clone the repository:
   ```
   git clone https://github.com/IfGF-UUlm/ADRD-dysphagia-clustering.git
   ```
3. Navigate into the repository directory:
   ```
   cd ADRD-dysphagia-clustering
   ```

### Setting Up the Environment
This repository includes an `environment.yml` file for creating a Conda environment with the required dependencies.

1. Ensure you have [Conda](https://docs.conda.io/en/latest/) installed.
2. Create the environment using:
   ```
   conda env create -f environment.yml -n adrd-dysphagia-env
   ```
3. Activate the environment:
   ```
   conda activate adrd-dysphagia-env
   ```

#### The analysis utilizes:
- Python 3.x
- numpy
- pandas
- scipy
- matplotlib
- scikit-learn (sklearn)
- Other dependencies as listed in `environment.yml`

To explore the analysis, open the main notebook (e.g., `Analysis.ipynb`) in Jupyter Notebook or JupyterLab after setting up the environment.

## License

This project is licensed under the MIT License.

## Citation

The manuscript is currently undergoing peer review and will be added once published.

## Contact

Questions, Feedback, or Concerns? Reach out to thomas.kocar@uni-ulm.de.
