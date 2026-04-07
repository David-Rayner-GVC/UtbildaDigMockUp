# Utbilda Dig!

This is a proof-of-concept for a Researchdata.se course portal, provisionally called Utbilda Dig!

Deployment: There is both a [Course card view](https://david-rayner-gvc.github.io/UtbildaDigMockUp/topics/)  and a [Topic summary view](https://david-rayner-gvc.github.io/UtbildaDigMockUp/topic-cards/) that you click through to see courses for that topic.

Information about courses is provided as md files in [src/courses/](src/courses/). Additionally, the site harvests from the SciLifeLab training portal information about courses that match the topics shown on the site using [scripts/import_scilifelab.py](scripts/import_scilifelab.py)! Note the harvest is at build-time, it is static after deployment. 

See [project_summary.md](project_summary.md) for a description of the architecture of this demo site.
