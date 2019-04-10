import csv
import nibabel as nib
import os
import numpy as np
from nibabel.affines import apply_affine



# categorize according to group-level cortical atlas parcellations
def voxel_match(mni_img, output_csv, parcellation_img):
    mni_affine = mni_img.affine
    mni_data = mni_img.get_fdata()
    parcellation_affine = parcellation_img.affine
    parcellation_data = parcellation_img.get_fdata()
    
    for i in range(len(mni_data)):
        for j in range(len(mni_data[0])):
            for k in range(len(mni_data[0][0])):
                cur_id = '%d_%d_%d' % (i, j, k)
                [x, y, z] = apply_affine(mni_affine, (i,j,k)) # voxel id to real-world coordinates
                [x_parcel, y_parcel, z_parcel] = apply_affine(np.linalg.inv(parcellation_affine), (x,y,z)) #real-world coordinates to voxel id
                    
                if parcellation_data[int(np.round(x_parcel))][int(np.round(y_parcel))][int(np.round(z_parcel))] != 0:
                    output_csv.writerow([cur_id, x, y, z, parcellation_data[int(np.round(x_parcel))][int(np.round(y_parcel))][int(np.round(z_parcel))]])



def main():
    # set up output path
    output_dir = os.path.abspath('../results')
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    output_path = os.path.join(output_dir, 'coordinates_table_BN_Atlas_246.csv')
    output_csv = csv.writer(open(output_path, 'w'), lineterminator="\n")
    output_csv.writerow(['voxel_id', 'mni_x', 'mni_y', 'mni_z', 'regionid'])
    
    # load anatomical nii files and parcellation nii files
    mni_img = nib.load(os.path.abspath('../data/parcellation/anatomical.nii'))
    parcellation_img = nib.load(os.path.abspath('../data/parcellation/BN_Atlas_246_2mm.nii.gz'))
    
    
    voxel_match(mni_img, output_csv, parcellation_img)


if __name__ == '__main__':
    main()

