import os
import nibabel as nib
from util import util


def check_nii_format():
    logger = util.get_logger()
    logger.info("check nii format")
    data_dir = os.path.join('../data/keyword_uniformity_test/')
    sample_nii = 'abilities_uniformity-test_z_FDR_0.01.nii.gz'
    nib_file = nib.load(os.path.join(data_dir, sample_nii))
    print(nib_file)
    pass


def check_compressed_csv():
    logger = util.get_logger()
    logger.info("check_compressed_csv")
    pass


def check_sparse_matrix():
    pass


def main():
    check_nii_format()
    # check_compressed_csv()


if __name__ == '__main__':
    main()

