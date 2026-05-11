# Table X. Bidirectional overlap of disease concepts among NANDO and international disease resources

Numbers of overlapping disease concepts among NANDO, MONDO, OMIM, Orphanet, and DO, evaluated in both directions. Each cell indicates the number of concepts in the row resource that overlap with at least one concept in the column resource through explicit mappings. NANDO concepts were linked to MONDO using `skos:exactMatch` and `skos:closeMatch` assertions in `nando_20260421.ttl`, and MONDO, OMIM, Orphanet, and DO concepts were linked using explicit `oboInOwl:hasDbXref` assertions in `mondo20260410.owl`. Differences between opposite directions reflect asymmetry in mapping coverage, concept granularity, and the number of source concepts represented by shared MONDO bridge terms.

| | NANDO | MONDO | OMIM | Orphanet | DO |
| --- | ---: | ---: | ---: | ---: | ---: |
| NANDO |  | 2091 | 982 | 1796 | 1561 |
| MONDO | 1556 |  | 10069 | 10380 | 11856 |
| OMIM | 687 | 10168 |  | 3850 | 5334 |
| Orphanet | 1275 | 10492 | 3854 |  | 3748 |
| DO | 1142 | 12032 | 5343 | 3756 |  |
