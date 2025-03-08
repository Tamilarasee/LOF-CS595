devtools::install_github("OHDSI/ETL-Synthea")

library(ETLSyntheaBuilder)

# Mac/Linux: Path Example: /Users/cpu/Downloads/OMOP/
# Windows: Path Example: D:\\LoF\\omop\\
#
cd <- DatabaseConnector::createConnectionDetails(
  dbms     = "postgresql",
  server   = "localhost/omop",
  user     = "postgres",
  password = "admin123",
  port     = 5432,
  pathToDriver = "/path_to_omop_folder/"  # path to your OMOP folder e.g.
)

# Mac/Linux: syntheaFileLoc Example: /Users/cpu/Downloads/OMOP/csv
# Windows: syntheaFileLoc Example: D:\\LoF\\omop\\csv
# schema names, etc.
cdmSchema = 'cdm54'
cdmVersion     <- "5.4"
syntheaVersion <- "3.3.0"
syntheaSchema  <- "synthea"
syntheaFileLoc <- "/path_to_omop_folder/csv" # path to OMOP/csv folder E.g. /Users/cpu/Downloads/OMOP/csv
resultsDatabaseSchema='results'
cdmSourceName='synthea'

#create tables for source data
ETLSyntheaBuilder::CreateSyntheaTables(connectionDetails = cd, syntheaSchema = syntheaSchema, syntheaVersion = syntheaVersion)

#load data into source data tables
ETLSyntheaBuilder::LoadSyntheaTables(connectionDetails = cd, syntheaSchema = syntheaSchema, syntheaFileLoc = syntheaFileLoc)

#create map and rollup tables
ETLSyntheaBuilder::CreateMapAndRollupTables(connectionDetails = cd, cdmSchema = cdmSchema, syntheaSchema = syntheaSchema, cdmVersion = cdmVersion, syntheaVersion = syntheaVersion)

## Optional Step to create extra indices
ETLSyntheaBuilder::CreateExtraIndices(connectionDetails = cd, cdmSchema = cdmSchema, syntheaSchema = syntheaSchema, syntheaVersion = syntheaVersion)

#load event tables
ETLSyntheaBuilder::LoadEventTables(connectionDetails = cd, cdmSchema = cdmSchema, syntheaSchema = syntheaSchema, cdmVersion = cdmVersion, syntheaVersion = syntheaVersion)

# NOW SEE INSTRUCTIONS AND RUN SQL SCRIPT ON PGADMIN TO CREATE RESULTS TABLES