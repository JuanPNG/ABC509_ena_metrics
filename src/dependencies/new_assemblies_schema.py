
# To replace assemblies block in line 84 of biodiveristy-data-ingestion/airflow/dags/dependencies/sample_schema.py

samples_schema = {
  "name": "assemblies",
  "type": "RECORD",
  "mode": "REPEATED",
  "fields": [
    { "name": "accession", "type": "STRING", "mode": "NULLABLE" },
    { "name": "assembly_name", "type": "STRING", "mode": "NULLABLE" },
    { "name": "description", "type": "STRING", "mode": "NULLABLE" },
    { "name": "study_accession", "type": "STRING", "mode": "NULLABLE" },
    { "name": "sample_accession", "type": "STRING", "mode": "NULLABLE" },
    { "name": "last_updated", "type": "STRING", "mode": "NULLABLE" },
    { "name": "version", "type": "STRING", "mode": "NULLABLE" },
    # New lines below
    {
      "name": "assembly_metrics",
      "type": "RECORD",
      "mode": "NULLABLE",
      "fields": [
        { "name": "assembly_level", "type": "STRING", "mode": "NULLABLE" },
        { "name": "ungapped_length", "type": "INTEGER", "mode": "NULLABLE" },
        { "name": "scaffold_n50", "type": "INTEGER", "mode": "NULLABLE" },
        { "name": "scaffold_count", "type": "INTEGER", "mode": "NULLABLE" },

        { "name": "contig_n50", "type": "INTEGER", "mode": "NULLABLE" },
        { "name": "contig_count", "type": "INTEGER", "mode": "NULLABLE" },
        { "name": "coverage", "type": "FLOAT", "mode": "NULLABLE" },
        { "name": "spanned_gaps", "type": "INTEGER", "mode": "NULLABLE" },
        { "name": "unspanned_gaps", "type": "INTEGER", "mode": "NULLABLE" },

        { "name": "contig_l50", "type": "INTEGER", "mode": "NULLABLE" },
        { "name": "scaffold_l50", "type": "INTEGER", "mode": "NULLABLE" },
        { "name": "contig_n75", "type": "INTEGER", "mode": "NULLABLE" },
        { "name": "contig_n90", "type": "INTEGER", "mode": "NULLABLE" },
        { "name": "scaffold_n75", "type": "INTEGER", "mode": "NULLABLE" },
        { "name": "scaffold_n90", "type": "INTEGER", "mode": "NULLABLE" },
        { "name": "replicon_count", "type": "INTEGER", "mode": "NULLABLE" },
        { "name": "non_chromosome_replicon_count", "type": "INTEGER", "mode": "NULLABLE" }
      ]
    }
  ]
}



# To be added to tge bq_metadata_schema in beam/src/dependencies/utils/bq_metadata_schema.py
# To be inserted in line 572
bq_metadata_schema = {
    "fields": [
        {
            "name": "assemblies",
            "type": "RECORD",
            "mode": "REPEATED",
            "fields": [
                {
                    "name": "accession",
                    "type": "STRING",
                    "mode": "NULLABLE"
                },
                {
                    "name": "description",
                    "type": "STRING",
                    "mode": "NULLABLE"
                },
                # New lines below
                {
                    "name": "assembly_metrics",
                    "type": "RECORD",
                    "mode": "NULLABLE",
                    "fields": [
                        {
                            "name": "assembly_level",
                            "type": "STRING",
                            "mode": "NULLABLE"
                        },
                        {
                            "name": "ungapped_length",
                            "type": "INTEGER",
                            "mode": "NULLABLE"
                        },
                        {
                            "name": "scaffold_n50",
                            "type": "INTEGER",
                            "mode": "NULLABLE"
                        },
                        {
                            "name": "scaffold_count",
                            "type": "INTEGER",
                            "mode": "NULLABLE"
                        },

                        {
                            "name": "contig_n50",
                            "type": "INTEGER",
                            "mode": "NULLABLE"
                        },
                        {
                            "name": "contig_count",
                            "type": "INTEGER",
                            "mode": "NULLABLE"
                        },
                        {
                            "name": "coverage",
                            "type": "FLOAT",
                            "mode": "NULLABLE"
                        },
                        {
                            "name": "spanned_gaps",
                            "type": "INTEGER",
                            "mode": "NULLABLE"
                        },
                        {
                            "name": "unspanned_gaps",
                            "type": "INTEGER",
                            "mode": "NULLABLE"
                        },

                        {
                            "name": "contig_l50",
                            "type": "INTEGER",
                            "mode": "NULLABLE"
                        },
                        {
                            "name": "scaffold_l50",
                            "type": "INTEGER",
                            "mode": "NULLABLE"
                        },
                        {
                            "name": "contig_n75",
                            "type": "INTEGER",
                            "mode": "NULLABLE"
                        },
                        {
                            "name": "contig_n90",
                            "type": "INTEGER",
                            "mode": "NULLABLE"
                        },
                        {
                            "name": "scaffold_n75",
                            "type": "INTEGER",
                            "mode": "NULLABLE"
                        },
                        {
                            "name": "scaffold_n90",
                            "type": "INTEGER",
                            "mode": "NULLABLE"
                        },
                        {
                            "name": "replicon_count",
                            "type": "INTEGER",
                            "mode": "NULLABLE"
                        },
                        {
                            "name": "non_chromosome_replicon_count",
                            "type": "INTEGER",
                            "mode": "NULLABLE"
                        }
                    ]
                }
            ]
        },
    ]
}