import pandas as pd
import nibabel as nib


keyword_list = pd.read_csv('data/keyword_list.csv') #load keyword data (behaviors)

anatomy_img = nib.load('data/anatomical.nii') 
anatomy_img_matrix = anatomy_img.get_fdata().flatten() #load default brain anatomy data (to infer valid coordinates)

unif_matrix = dict()
assoc_matrix = dict()

unif_matrix['anatomy'] = list(anatomy_img_matrix)
assoc_matrix['anatomy'] = list(anatomy_img_matrix)

#load brain activation data (uniformity test, association test)
for word in keyword_list['keyword']:
    print(word)
    unif_matrix[word] = list(nib.load('data/keyword_uniformity_test/' + word + '_uniformity-test_z_FDR_0.01.nii.gz').get_fdata().flatten())
    assoc_matrix[word] = list(nib.load('data/keyword_association_test/' + word + '_association-test_z_FDR_0.01.nii.gz').get_fdata().flatten())
    
unif_matrix_df = pd.DataFrame(unif_matrix)
assoc_matrix_df = pd.DataFrame(assoc_matrix)
                
unif_matrix_df.to_csv('results/matrix_uniformity_test.csv')
assoc_matrix_df.to_csv('results/matrix_association_test')