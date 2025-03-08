install.packages("remotes")
remotes::install_github("OHDSI/Achilles")

library(Achilles)

# Mac/Linux: Path Example: /Users/cpu/Downloads/OMOP/
# Windows: Path Example: D:\\LoF\\omop\\
# create database connection
cd <- DatabaseConnector::createConnectionDetails(
  dbms     = "postgresql",
  server   = "localhost/omop",
  user     = "postgres",
  password = "admin123",
  port     = 5432,
  pathToDriver = "/path_to_omop_folder/"  # path to your OMOP folder e.g. /Users/cpu/Downloads/OMOP/
)

Achilles::achilles(
  cdmVersion = "5.4", 
  connectionDetails = cd,
  cdmDatabaseSchema = "cdm54",
  resultsDatabaseSchema = "results"
)

# NOW RUN SECOND SQL SCRIPT ON PGADMIN TO CREATE CONCEPT COUNTS