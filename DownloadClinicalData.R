library(TCGAbiolinks)
library(tidyverse)


# Functions ---------------------------------------------------------------

write_clinical_data <- function(all_clinical_data, project_name){
  get_names <- names(all_clinical_data)
  dir.create(file.path('/data/gcs/tcgadata/files/DiagnosisSlides/DataExtraction_DataManagement' ,project_name, 'ClinicalData' ))
  c = 1
  for (i in get_names){
    write.table( all_clinical_data[[c]], file.path('/data/gcs/tcgadata/files/DiagnosisSlides/DataExtraction_DataManagement' ,project_name, 'ClinicalData',  
                              paste(i, '.txt', sep = '')), row.names= F, sep = '\t')
    c = c + 1
  }
}

get_clinical_data <- function(project_name){
  query <- GDCquery(project = project_name, 
                    data.category = "Clinical",
                    data.type = "Clinical Supplement", 
                    data.format = "BCR Biotab")
  GDCdownload(query)
  clinical.data.all <- GDCprepare(query)
  write_clinical_data(clinical.data.all, project_name)
}


# List of project --------------------------------------------------------
list_projects <- c('BRCA', 'CESC', 'COAD', 'READ', 'STAD', 'HNSC', 'LIHC', 'LUAD',
                   'LUSC', 'SKCM', 'PAAD', 'PRAD', 'KICH', 'KIRC', 'KIRP')

l_project_list <- lapply(list_projects, function(x) paste('TCGA' , x, sep='-'))


# Main --------------------------------------------------------------------

lapply(l_project_list, get_clinical_data)




