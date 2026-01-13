# Examples on how to run this code

from dependencies.genome_metrics_client import get_assembly_metrics, build_bq_record

accession = "GCA_964035705"
example = get_assembly_metrics(accession)
print("All the assembly metrics:")
print(example.model_dump())
print("Just the scaffold N50:")
print(example.scaffold_n50)


record = {
    "sample_id": "SAMPLE_001",
    "species": "Porites rus",
    "accession": "GCA_964035705",
    "sample_metadata": "2.4.1",
}
accession = record["accession"]

print("Record ready to be merged into a biodiversity data ingestion pipeline record:")
ena_genome_metrics = build_bq_record(accession)
print(ena_genome_metrics)