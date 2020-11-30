import pandas as pd
import os

# main_folder = os.listdir()
# list_slides = []
# list_types = []
# for folder in main_folder:
#     if folder.find("TCGA") != -1 and folder.find("TCGA-AO") == -1:
#         current_type = folder
#         print(folder)
#         print(os.getcwd())
#         sub_folder = os.listdir(os.path.join(os.getcwd(), folder))
#         for sf in sub_folder:
#             if sf.find("Slides") != -1:
#                 files = os.listdir(os.path.join(os.getcwd(), folder, sf ))
#                 for f in files:
#                     if f.find("TCGA-") != -1:
#                         list_slides.append(f)
#                         list_types.append(current_type)
# df_slides_report = pd.DataFrame()
# df_slides_report["SlideName"] = list_slides
# df_slides_report["CancerType"] = list_types
# df_slides_report.to_csv("SlidesReport.csv", sep="\t", header=True, index=False)


# list_slides = []
# list_types = []
# main_folder_path = "/data/gcs/tcgadata/files/DiagnosisSlides/DataExtraction_DataManagement"
# main_folder_list = os.listdir(main_folder_path)
# for subfolder in main_folder_list:
#     if subfolder.find("TCGA") != -1:
#         subfolder_slides_path = os.path(main_folder_path, subfolder, subfolder, "harmonized/Biospecimen/Slide_Image")
#         current_type = subfolder
#         subfolder_slides_list = os.listdir(subfolder_slides_path)
#         for folder in subfolder_slides_list:
#             slides_folder = os.listdir(subfolder_slides_path, folder)
#             for f in slides_folder:
#                 list_slides.append(f)
#                 list_types.append(current_type)
# df_slides_report = pd.DataFrame()
# df_slides_report["SlideName"] = list_slides
# df_slides_report["CancerType"] = list_types
# df_slides_report.to_csv("/data/gcs/tcgadata/files/DiagnosisSlides/DataExtraction_DataManagement/SlidesReport.csv", sep="\t", header=True, index=False)


###########################################################################
#   Count carcinoids
###########################################################################
# path_folder_carcinoids_images = "/data/gcs/lungNENomics/files/Internal_Data/Images/LungNENomics_2020"
# folder_carcinoids = os.listdit(path_folder_carcinoids_images)
# filename = []
# id_ = [] 
# for f in folder_carcinoids:
#     filename.append(f)
#     id_c =f.split('.')[0]
#     id_.append(id_c)

# df_carcinoids = pd.DataFrame()
# df_carcinoids["filename"] = filename
# df_carcinoids["id"] = id_
# df_carcinoids.to_csv("CountImgagesCarcinoids.csv", header=True)

# Check Images in DB and expected
df_carcinoids_db = pd.read_csv("CountImgagesCarcinoids.csv")
df_carcinoids_exp = pd.read_csv("hescarcinoidesprt-k02112020.csv")

print(df_carcinoids_exp.head())

print("\n\n\n", df_carcinoids_db.head())

set_id_exp = set(df_carcinoids_exp[" ID (anonyme)"])
print(len(set_id_exp))

set_id_db = set(df_carcinoids_db["id"])

print("Not on osiris   :", set_id_exp - set_id_db)
print("Unexpected id on osiris  :", set_id_db - set_id_exp)

missing_osiris = list(set_id_exp - set_id_db)

df_missing_osiris = df_carcinoids_exp[df_carcinoids_exp[" ID (anonyme)"].isin(missing_osiris)]
print(df_missing_osiris.head())
df_missing_osiris.to_csv("SamplesMissingInOsiris.csv")