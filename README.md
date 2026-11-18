# ADRD Dysphagia Clustering

This GitHub repository contains the code used for the clustering analysis in the paper "Clustering analysis reveals an Alzheimer’s disease-associated swallowing pattern in geriatric patients with oropharyngeal dysphagia".

## Project Overview

Oropharyngeal dysphagia is common in older adults with Alzheimer's disease and related dementias (ADRD), but it is insufficiently understood how endoscopic swallowing abnormalities co-occur in this population. Most previous work relied on videofluoroscopy and described individual findings in isolation.

In this retrospective cohort study, we analysed 158 consecutive geriatric inpatients with oropharyngeal dysphagia (98 with and 60 without dementia) who underwent standardized flexible endoscopic evaluation of swallowing (FEES) at the Department of Geriatric Medicine, Marien Hospital Herne (Ruhr University Bochum), between December 2019 and January 2025.

To identify combinations of FEES findings associated with dementia, we combined supervised feature-subset selection with unsupervised clustering:

- Agglomerative hierarchical clustering (Ward's method, Euclidean distance) was applied to dichotomized FEES features.
- The analysed feature subset was selected from all 2,047 combinations of 11 expert-defined candidate features by its agreement with dementia status (adjusted Rand index, ARI).
- Selection optimism was assessed by permutation testing (999 permutations with full re-selection).
- Sensitivity analyses excluded patients with mild Parkinson's disease, a history of stroke, or both.

The resulting three clusters did not separate patients with and without dementia but formed a spectrum of increasing swallowing-pattern complexity.

## Key Messages

- **Dementia was associated with co-occurring findings across swallowing phases, not with airway invasion.** Patients with dementia more often showed prolonged pre-pharyngeal bolus transit (34 % vs 7 %), repetitive swallowing (66 % vs 33 %), delayed pharyngeal swallow initiation (34 % vs 13 %) and piriform sinus residue (58 % vs 37 %), whereas penetration and aspiration (PAS ≥ 3) did not differ between groups (13 % vs 18 %).
- **These associations were robust.** Each of the four findings remained associated with dementia after adjustment for age, Barthel Index, sex, mild Parkinson's disease and prior stroke.
- **Five features defined the best clustering solution.** Among all 2,047 candidate subsets, the combination of the four findings above plus reduced white-out intensity showed the highest agreement with dementia status (ARI 0.25; permutation p = 0.001) and yielded three clusters with dementia proportions of 29 %, 70 % and 85 %.
- **Clusters represent a spectrum, not a diagnosis-specific phenotype.** Clusters with a higher proportion of patients with dementia showed more complex dysphagia patterns (super-complex pattern, ≥ 3 co-occurring findings, in 81 % of the highest vs 27 % of the lowest cluster).
- **Clinical implication:** Endoscopic evaluation of older adults should assess patterns of findings across the whole swallowing sequence, not only penetration and aspiration. These patterns require validation in independent prospective cohorts.

## Repository Structure

- [`analysis.ipynb`](./analysis.ipynb): Feature extraction and clustering analysis
- [`revision_analyses.py`](./revision_analyses.py): Additional analyses for the revision
- [`revision_analyses_output.txt`](./revision_analyses_output.txt): Console output of `revision_analyses.py`
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
