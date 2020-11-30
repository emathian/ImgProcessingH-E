import os 
import shutil
import re
import json

main_folder = os.listdir(os.path.join(os.getcwd()))
for folder in main_folder:
	if folder[:5] == 'TCGA-':
		print("Folder ", folder)
		in_project_folder = os.listdir(os.path.join(os.getcwd(), folder))
		try:
			os.mkdir(os.path.join(os.getcwd(), folder, "SlidesImagesRenamed"))
		except:
			print('Path : ', os.path.join(os.getcwd(), folder, "SlidesImagesRename"), " already created."  )
		dict_OldName_NewName = dict()
		for ele in in_project_folder:
			if ele == "SlidesImages":
				c_slide = 0
				diagnosis_slides =  os.listdir(os.path.join(os.getcwd(), folder, ele))
				for svsfile in diagnosis_slides:
					if svsfile.find(".svs") != -1:
						print(" svsfile  :  ", svsfile)
						former_name = svsfile
						base_name = svsfile.split('.')[0]
						pos_third_dash = 0
						c = 0
						for m in re.finditer(r"-", base_name):
							if c < 3:
								pos_third_dash = m.end()
								c += 1
							else:
								break
						sample_id = base_name[:pos_third_dash -1]
						list_slides_rename = os.listdir(os.path.join(os.getcwd(), folder, ele))
						diagnosis_slides_as_str = ''.join(list_slides_rename)
						#print(diagnosis_slides_as_str , '\n\n\n' )
						len_slide_rename_same_sample_id = len(re.findall(base_name, diagnosis_slides_as_str))
						new_name = sample_id + '.' + folder + '.' + 'S' +  '{:03}'.format(len_slide_rename_same_sample_id) + '.svs'
						dict_OldName_NewName[former_name] = new_name
						shutil.move(os.path.join(os.getcwd(), folder, ele, former_name), os.path.join(os.getcwd(), folder, 'SlidesImagesRenamed', new_name))

		OldName_NewName_filename = 'OldNamesNewNames_' + folder + '.txt'
		with open(os.path.join(os.getcwd(), folder, OldName_NewName_filename ), 'w') as file:
			file.write(json.dumps(dict_OldName_NewName)) # use `json.loads` to do the reverse