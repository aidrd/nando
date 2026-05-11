#!/usr/bin/env python3

from __future__ import annotations

import argparse
import csv
import re
from collections import defaultdict
from pathlib import Path
from typing import DefaultDict
from xml.etree import ElementTree as ET


RESOURCES = ["NANDO", "MONDO", "OMIM", "Orphanet", "DO"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build a bidirectional overlap table across NANDO, MONDO, OMIM, "
            "Orphanet, and DO using explicit mappings in local NANDO and MONDO files."
        )
    )
    parser.add_argument("--nando", required=True, help="Path to the NANDO TTL file")
    parser.add_argument("--mondo", required=True, help="Path to the MONDO OWL file")
    parser.add_argument(
        "--nando-mapping-mode",
        choices=["exact", "exact+close"],
        default="exact+close",
        help="Which NANDO -> MONDO mappings to use",
    )
    parser.add_argument(
        "--output-prefix",
        required=True,
        help="Output path prefix, without extension",
    )
    return parser.parse_args()


def parse_nando_mappings(
    nando_path: Path, mapping_mode: str
) -> DefaultDict[str, set[str]]:
    nando_to_mondo: DefaultDict[str, set[str]] = defaultdict(set)
    current_nando_id: str | None = None

    with nando_path.open(encoding="utf-8", errors="ignore") as handle:
        for line in handle:
            if line.startswith("<http://nanbyodata.jp/ontology/NANDO_"):
                match = re.match(
                    r"<http://nanbyodata\.jp/ontology/(NANDO_\d+)>", line
                )
                current_nando_id = (
                    match.group(1).replace("_", ":", 1) if match else None
                )
                continue

            if not current_nando_id:
                continue

            is_exact = "skos:exactMatch obo:MONDO_" in line
            is_close = "skos:closeMatch obo:MONDO_" in line
            if not is_exact and not is_close:
                if line.strip().endswith("."):
                    current_nando_id = None
                continue

            if is_close and mapping_mode != "exact+close":
                if line.strip().endswith("."):
                    current_nando_id = None
                continue

            match = re.search(r"obo:(MONDO_\d+)", line)
            if match:
                mondo_id = match.group(1).replace("_", ":", 1)
                nando_to_mondo[current_nando_id].add(mondo_id)

            if line.strip().endswith("."):
                current_nando_id = None

    return nando_to_mondo


def parse_mondo_xrefs(
    mondo_path: Path,
) -> dict[str, DefaultDict[str, set[str]]]:
    resource_to_mondos: dict[str, DefaultDict[str, set[str]]] = {
        resource: defaultdict(set) for resource in RESOURCES
    }

    rdf_ns = "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}"
    owl_class = "{http://www.w3.org/2002/07/owl#}Class"
    has_dbxref = "{http://www.geneontology.org/formats/oboInOwl#}hasDbXref"

    for _, elem in ET.iterparse(mondo_path, events=("end",)):
        if elem.tag != owl_class:
            continue

        about = elem.attrib.get(f"{rdf_ns}about", "")
        if not about.startswith("http://purl.obolibrary.org/obo/MONDO_"):
            elem.clear()
            continue

        mondo_id = about.rsplit("/", 1)[1].replace("_", ":", 1)
        resource_to_mondos["MONDO"][mondo_id].add(mondo_id)

        for child in elem:
            if child.tag != has_dbxref or not child.text:
                continue

            xref = child.text.strip()
            if xref.startswith("OMIM:"):
                resource_to_mondos["OMIM"][xref].add(mondo_id)
            elif xref.startswith("Orphanet:"):
                resource_to_mondos["Orphanet"][xref].add(mondo_id)
            elif xref.startswith("DOID:"):
                resource_to_mondos["DO"][xref].add(mondo_id)

        elem.clear()

    return resource_to_mondos


def build_overlap_table(
    resource_to_mondos: dict[str, DefaultDict[str, set[str]]]
) -> dict[str, dict[str, int | None]]:
    mondo_pools = {
        resource: set().union(*concepts.values()) if concepts else set()
        for resource, concepts in resource_to_mondos.items()
    }

    table: dict[str, dict[str, int | None]] = {}
    for row_resource in RESOURCES:
        table[row_resource] = {}
        for col_resource in RESOURCES:
            if row_resource == col_resource:
                table[row_resource][col_resource] = None
                continue

            overlap_count = sum(
                1
                for mondo_ids in resource_to_mondos[row_resource].values()
                if mondo_ids & mondo_pools[col_resource]
            )
            table[row_resource][col_resource] = overlap_count

    return table


def write_csv(output_path: Path, table: dict[str, dict[str, int | None]]) -> None:
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([""] + RESOURCES)
        for row_resource in RESOURCES:
            writer.writerow(
                [
                    row_resource,
                    *[
                        "" if table[row_resource][col_resource] is None else table[row_resource][col_resource]
                        for col_resource in RESOURCES
                    ],
                ]
            )


def write_markdown(
    output_path: Path,
    table: dict[str, dict[str, int | None]],
    nando_path: Path,
    mondo_path: Path,
    mapping_mode: str,
) -> None:
    lines = [
        "# Table X. Bidirectional overlap of disease concepts among NANDO and international disease resources",
        "",
        "Numbers of overlapping disease concepts among NANDO, MONDO, OMIM, Orphanet, and DO, evaluated in both directions.",
        "Each cell indicates the number of concepts in the row resource that overlap with at least one concept in the column resource.",
        "",
        "## Counting rule",
        "",
        f"- NANDO concepts are linked to MONDO via `{mapping_mode}` `skos` mappings in `{nando_path}`.",
        f"- MONDO, OMIM, Orphanet, and DO concepts are read from explicit `oboInOwl:hasDbXref` assertions in `{mondo_path}`.",
        "- Two concepts are treated as overlapping when they share at least one MONDO concept as a bridge.",
        "",
        "| | NANDO | MONDO | OMIM | Orphanet | DO |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]

    for row_resource in RESOURCES:
        row = [row_resource]
        for col_resource in RESOURCES:
            value = table[row_resource][col_resource]
            row.append("" if value is None else str(value))
        lines.append("| " + " | ".join(row) + " |")

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    nando_path = Path(args.nando).expanduser().resolve()
    mondo_path = Path(args.mondo).expanduser().resolve()
    output_prefix = Path(args.output_prefix).expanduser().resolve()
    output_prefix.parent.mkdir(parents=True, exist_ok=True)

    resource_to_mondos = parse_mondo_xrefs(mondo_path)
    resource_to_mondos["NANDO"] = parse_nando_mappings(
        nando_path, args.nando_mapping_mode
    )

    table = build_overlap_table(resource_to_mondos)

    csv_path = output_prefix.with_suffix(".csv")
    md_path = output_prefix.with_suffix(".md")
    write_csv(csv_path, table)
    write_markdown(
        md_path, table, nando_path, mondo_path, args.nando_mapping_mode
    )

    print(f"Wrote {csv_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
