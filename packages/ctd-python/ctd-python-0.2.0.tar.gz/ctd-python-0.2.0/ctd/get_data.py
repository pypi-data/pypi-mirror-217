import os
import io
import gzip
import shutil
import logging
import requests
from tqdm import tqdm
import pandas as pd

PACKAGE_DIR = os.path.dirname(__file__)
RAW_DATA_DIR = os.path.join(PACKAGE_DIR, 'unzipped_data')

from pprint import pprint

def download_resource(resource: str) -> str:
    url_dl_pattern = 'http://ctdbase.org/reports/{resource}.csv.gz'
    url = url_dl_pattern.format(resource=resource)

    logging.info('[download_resource]: downloading: %s', resource)
    local_filename = os.path.join(RAW_DATA_DIR, f"{resource}.csv")

    ## TODO - make this a config to refresh
    ## perhaps even add the date of the file created so we can dl new
    ## files when they come in
    if os.path.isfile(local_filename):
        return local_filename

    response = requests.get(url, stream=True)
    response.raise_for_status()
    total_size = int(response.headers.get('content-length', 0))
    block_size = 8192
    progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)

    with open(local_filename, 'wb') as f:
        with gzip.GzipFile(fileobj=response.raw, mode='rb') as gz_file:
            while True:
                chunk = gz_file.read(block_size)
                if not chunk:
                    break
                f.write(chunk)
                progress_bar.update(len(chunk))
    progress_bar.close()

    return local_filename


def get_data(resource: str) -> pd.DataFrame:
    """
    Fetch the data for a specific resource from the CTD database.

    Args:
        resource (str): The name of the resource.

    Returns:
        pd.DataFrame: The data as a pandas DataFrame.

    Raises:
        Exception: If the specified resource is not available.

    Notes:
        The available resources are:
        - GeneInteractionTypes
        - ChemicalPathwaysEnriched
        - GeneDisease
        - GenePathways
        - DiseasePathways
        - ChemocalPhenoTypeInteractions
        - Exposure Studies
        - Chemicals
        - Genes
        - ChemicalGeneInteractions
        - ChemicalDiseaseInteractions
        - Diseases
    """

    RESOURCES = {
        'GeneInteractionTypes': {'filename': 'CTD_chem_gene_ixn_types'},
        'ChemicalPathwaysEnriched': {'filename': 'CTD_chem_pathways_enriched'},
        'GeneDisease': {'filename': 'CTD_genes_diseases'},
        'GenePathways': {'filename': 'CTD_genes_pathways'},
        'DiseasePathways': {'filename': 'CTD_diseases_pathways'},
        'ChemocalPhenoTypeInteractions': {'filename': 'CTD_pheno_term_ixns'},
        'Exposure Studies': {'filename': 'CTD_exposure_studies'},
        'Chemicals': {'filename': 'CTD_chemicals'},
        'Genes': {'filename': 'CTD_genes'},
        'ChemicalGeneInteractions': {'filename': 'CTD_chem_gene_ixns'},
        'ChemicalDiseaseInteractions': {'filename': 'CTD_chemicals_diseases', 'dtypes': {'ChemicalName': str,'ChemicalID': str,'CasRN': str,'DiseaseName': str,'DiseaseID': str,'DirectEvidence': str,'InferenceGeneSymbol': str,'InferenceScore': float,'OmimIDs': str,'PubMedIDs': str}},
        'Diseases': {'filename': 'CTD_chem_gene_ixn_types'}
    }

    resource_obj = RESOURCES.get(resource)

    filename = resource_obj.get('filename')
    dtypes = resource_obj.get('dtypes')

    if not resource_obj:
        raise Exception(f"The resource '{resource}' is not available. Please check https://ctdbase.org/downloads/ for available resources.")

    download_resource(filename)

    fields_line = '# Fields:'
    header_line = '#'
    the_file = os.path.join(RAW_DATA_DIR, f"{filename}.csv")

    fields_line_number = None
    with open(the_file, 'r') as reader:
        for i, row in enumerate(reader):
            if 'Fields:' in row:
                fields_line_number = i + 1
            elif i == fields_line_number:
                fields_line = row.strip("# ").strip()
                fields = [field.strip() for field in fields_line.split(",")]

    df = pd.read_csv(the_file, skiprows=fields_line_number + 1, names=fields, dtype=dtypes)

    return df


if __name__ == '__main__':
    get_data('ChemicalDiseaseInteractions')
