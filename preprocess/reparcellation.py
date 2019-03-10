import csv
import nibabel as nib
import os
from nibabel.affines import apply_affine



# categorize according to group-level cortical atlas parcellations
def voxel_check(anatomical_img, output_csv, parcellation_data):
    for i in range(len(parcellation_data)):
        for j in range(len(parcellation_data[0])):
            for k in range(len(parcellation_data[0][0])):
                if abs(parcellation_data[i][j][k]) != 0.0:
                    cur_id = '%d_%d_%d' % (i, j, k)
                    [x, y, z] = apply_affine(anatomical_img.affine, (i,j,k))
                    output_csv.writerow([cur_id, x, y, z, parcellation_data[i][j][k]])

def main():
    # set up output path
    output_dir = os.path.abspath('../results')
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    output_path = os.path.join(output_dir, 'coordinates_table.csv')
    output_csv = csv.writer(open(output_path, 'w'), lineterminator="\n")
    output_csv.writerow(['voxel_id', 'mni_x', 'mni_y', 'mni_z', 'shen_regionid'])
    
    # load anatomical nii files and parcellation nii files
    anatomical_img = nib.load(os.path.abspath('../data/parcellation/anatomical.nii'))
    shen_data = nib.load(os.path.abspath('../data/parcellation/shen_2mm_268_parcellation.nii')).get_fdata()
    
    
    voxel_check(anatomical_img, output_csv, shen_data)


if __name__ == '__main__':
    main()
