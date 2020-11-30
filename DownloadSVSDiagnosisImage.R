library(TCGAbiolinks)
library(tidyverse)
# Functions ---------------------------------------------------------------
write_summary_table <- function(project_name){
  # Write a summary table for each project
	c_summary <- getSampleFilesSummary(project_name)
	dir.create(file.path(getwd(),  project_name))
	write.table(c_summary, file = file.path(getwd(), project_name , paste("summary_TCGA", project_name, ".txt", sep='_') ), quote = FALSE, sep = "\t", 
		na = "NA", dec = ".", row.names = FALSE, col.names = TRUE)
}


get_ID_with_diagnosis_slide <- function(project_name){
  # Get ID for each at least one diagnosis slide is available.
  c_table <- read.table(file.path(getwd(), project_name, list.files(file.path(getwd(), project_name), pattern='summary')), sep = '\t', header = TRUE)
  sample_with_WSI <- c_table[c_table[,3] > 0 , ]$".id"
  df_MANIFEST <- read.table('MANIFEST.txt', sep = '\t', header=TRUE)
  l_sample_done <- df_MANIFEST$filename
  l_ID_done <- lapply(l_sample_done, function(x) substr(strsplit(x, '/')[[1]][2], 1, 12))
  sample_with_WSI <- sample_with_WSI[-c(which(c_table$'.id' %in% l_ID_done))]
  return(c_table[c_table[,3] > 0 , ]$".id")
  }

download_diagnosis_slide <- function(project_name){
  # Download slides
  query <- GDCquery(project = project_name, 
                   data.category = "Biospecimen", 
                   data.type = "Slide Image",
                   experimental.strategy = "Diagnostic Slide",
                  barcode = c(get_ID_with_diagnosis_slide(project_name)))
  GDCdownload(query, directory=file.path(getwd(),project_name) , method = "api", files.per.chunk = 10)
}

# Main --------------------------------------------------------------------

# List of project used by Karther et al.
list_projects <- c('BRCA', 'CESC', 'COAD', 'READ', 'STAD', 'HNSC', 'LIHC', 'LUAD',
					'LUSC', 'SKCM', 'PAAD', 'PRAD', 'KICH', 'KIRC', 'KIRP')

l_project_list <- lapply(list_projects, function(x) paste('TCGA' , x, sep='-'))

# Get list of ID with diagnosis slide
# lapply(l_project_list, write_summary_table)

# Download SVS images
# (l_project_list, download_diagnosis_slide)

# Get clinical data
get_clinical_data <- function(project_name){
  query <- GDCquery(project = "TCGA-COAD", 
                    data.category = "Clinical",
                    data.type = "Clinical Supplement", 
                    data.format = "BCR Biotab")
  GDCdownload(query)
  
}


clinical.BCRtab.all <- GDCprepare(query)
write.csv(clinical.BCRtab.all[1], "test_clinical.txt")
df <- read.csv("test_clinical.txt", header=TRUE)
write_clinical_data <- function(all_clinical_data){
  get_names <- names(all_clinical_data)
  print(get_names)
  for (i in get_names){
    write.table( x, paste(i, '.txt', sep = ''), row.names= F, sep = '\t')
  }
}



write_clinical_data(clinical.BCRtab.all)
lapply(clinical.BCRtab.all, function(x) write.table( x, paste(names(x), '.txt', sep = ''), row.names= F, sep = '\t'))
lapply(clinical.BCRtab.all, function(x) print(names(x)))

# All available tables
names(clinical.BCRtab.all)
