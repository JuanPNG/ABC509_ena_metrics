# from dependencies.genome_metrics_client import get_assembly_metrics
#
# accession = "GCA_964035705"
# re1to3 = get_assembly_metrics(accession)
# print(re1to3.model_dump())
# print(re1to3.scaffold_n50)

from dependencies.genome_metrics_client import build_bq_record

record = {
    "sample_id": "SAMPLE_001",
    "species": "Porites rus",
    "accession": "GCA_964035705",
    "sample_metadata": "2.4.1",
}

accession = record["accession"]

ena_genome_metrics = build_bq_record(accession)

print(ena_genome_metrics)  # Complete assembly metrics record


# import requests
# import json
# from typing import Dict, Optional
# 
# from dependencies.helpers import fetch_ena_assembly_summary
# from dependencies.assembly_metrics_schema import EnaAssemblyResponse, AssemblyMetrics, _coerce_value, ENA_TAG_TO_KEY
# 
# accession = "GCA_964035705"
# 
# raw_payload = fetch_ena_assembly_summary(accession)
# 
# raw = EnaAssemblyResponse.model_validate(raw_payload)
# 
# # Build normalized dict from raw
# metric_data: Dict[str, object] = {}
# 
# # Take from top-level fields
# if raw.assemblyLevel is not None:
#     metric_data["assembly_level"] = raw.assemblyLevel
# if raw.assemblyCoverage is not None:
#     metric_data["coverage"] = float(raw.assemblyCoverage)
# 
# # Take from attributes tag/value list
# for attr in raw.attributes:
#     key = ENA_TAG_TO_KEY.get(attr.tag)
#     if key is None:
#         continue
#     metric_data[key] = _coerce_value(key, attr.value)
# 
# # Validate normalized metrics
# metrics = AssemblyMetrics.model_validate(metric_data)
# 
# print(metrics.model_dump())
# 
# 
# 
# #
# #
# #
# #
# # print("raw.accession:", raw.accession)
# # print("raw.assemblyLevel:", raw.assemblyLevel)
# # print("raw.attributes count:", len(raw.attributes))
# # print("raw.chromosomes count:", len(raw.chromosomes))
# # print(len("raw.attributes"))
# 
# #
# #
# # genome_accession = "GCA_964035705"
# #
# # ena_xml = requests.get(f"https://www.ebi.ac.uk/ena/browser/api/summary/{genome_accession}")
# #
# # response = json.loads(ena_xml.text)
# #
# # summary = response.get("summaries", [])[0]
# #
# # print(json.dumps(summary, indent=2))
# #
# # summary_fields = ['accession', 'title', 'description', 'name', 'version', 'dataType', 'status', 'statusDescription',
# #                   'chromosomes', 'wgsSet', 'assemblyType', 'assemblyLevel', 'platform', 'program', 'assemblyCoverage',
# #                   'attributes', 'links']
# #
# # assembly_summary = {}
# #
# # assembly_summary['accession'] = summary.get("accession")
# # # assembly_summary['name'] = summary.get("name")
# # # assembly_summary['version'] = summary.get("version")
# #
# # for attribute in summary.get("attributes", []):
# #     tag = attribute.get("tag")
# #     assembly_summary[tag] = attribute.get("value")
# #
# # chromosome_count: int = 0
# # mitochondial_count: int = 0
# # chloroplast_count: int = 0
# #
# # for item in summary.get("chromosomes"):
# #
# #     if item.get("type") == "Chromosome":
# #         chromosome_count = chromosome_count + 1
# #     elif item.get("type") == "Mitochondrion":
# #         mitochondial_count = mitochondial_count + 1
# #     elif item.get("type") == "Chloroplast":
# #         chloroplast_count = chloroplast_count + 1
# #
# # assembly_summary['assembly_level'] = summary.get("assemblyLevel")
# # assembly_summary['chromosome_count'] = chromosome_count
# # assembly_summary['mitochondrial_count'] = mitochondial_count
# # assembly_summary['chloroplast_count'] = chloroplast_count
# #
# # assembly_summary["platform"] = summary.get("platform")
# #
# # # assembly_summary["links"] = summary.get("links")
# # #
# # # print(json.dumps(assembly_summary, indent=2))
# # #
# # # att_dict = {}
# # # for attribute in summary.get("attributes", []):
# # #     tag = attribute.get("tag")
# # #     assembly_summary[tag] = attribute.get("value")
# # #
# # # print(att_dict)