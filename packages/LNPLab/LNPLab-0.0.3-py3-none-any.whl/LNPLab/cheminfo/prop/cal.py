from rdkit.Chem import Descriptors, MolFromSmiles, QED
from rdkit.ML.Descriptors import MoleculeDescriptors
from padelpy import from_smiles

# calculate molecular descriptors for propane\
descriptors = from_smiles('CCC')

# calculate molecular descriptors for propane and butane
# descriptors = from_smiles(['CCC', 'CCCC'])

# in addition to descriptors, calculate PubChem fingerprints
desc_fp = from_smiles('CCC', fingerprints=True)

# only calculate fingerprints
fingerprints = from_smiles(
    'CC1=C(C=C(C=C1)NC(=O)C2=CC=C(C=C2)CN3CCN(CC3)C)NC4=NC=CC(=N4)C5=CN=CC=C5',
    fingerprints=True,
    descriptors=False
)
# setting the number of threads, this uses one cpu thread to compute descriptors
# descriptors = from_smiles(['CCC', 'CCCC'], threads=1)

# save descriptors to a CSV file
_ = from_smiles(
    'CC1=C(C=C(C=C1)NC(=O)C2=CC=C(C=C2)CN3CCN(CC3)C)NC4=NC=CC(=N4)C5=CN=CC=C5',
    fingerprints=True,
    output_csv='descriptors.csv'
)

'''
calc = MoleculeDescriptors.MolecularDescriptorCalculator(
    [x[0] for x in Descriptors._descList]
)

desc_list = [x[0] for x in Descriptors._descList]
rdkit_desc = calc.CalcDescriptors(
    MolFromSmiles(
        'CC1=C(C=C(C=C1)NC(=O)C2=CC=C(C=C2)CN3CCN(CC3)C)NC4=NC=CC(=N4)C5=CN=CC=C5'
    )
)

for desc, value in zip(desc_list, rdkit_desc):
    print(desc, value)

print(len(desc_list))
'''

