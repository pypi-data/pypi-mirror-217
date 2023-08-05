import re

import pandas as pd
from PyPDF2 import PdfReader

pdf_file = "/Users/khalimconn-kowlessar/Documents/epc/epc-api-python/examples/Mergers And Acquisitions Made Simple_Due+Diligence+Check+List.pdf"

reader = PdfReader(pdf_file)

results = []

for page in reader.pages:
    text = page.extract_text()

    # Remove the table of contents
    text_string = re.sub(r"Table of Contents.*?\d+\n", "", text)

    # Replace numbering patterns with a newline character followed by the pattern
    text = re.sub(r'(?<=\d\.)(?!\d)', '\n', text)

    # Split the text into sections based on double newline characters
    sections = text.split('\n')

    page_results = []
    for section in sections:
        cleaned_section = section.strip()
        cleaned_section = cleaned_section.replace("\t", " ")

        if re.split(r'\s\d+\.\d+\s', cleaned_section):
            split = re.split(r'\s\d+\.\d+\s', cleaned_section)

            # main = split.pop(0).rstrip('0123456789').strip()

            split = [x.rstrip('0123456789').strip() for x in split]

            # Split bullet points within each subsection
            split_clean = []
            for subsection in split:
                bullet_points = re.split(r'\s•\s', subsection)
                split_clean.extend(bullet_points)

            if "Copyright" in split_clean[0] or "John Colley" in split_clean[0]:
                split_clean.pop(0)

            if not split_clean:
                continue

            main = split_clean.pop(0)

            # It is a main section
            page_results.append({"main": main, "subsections": split_clean})
        else:
            page_results.append({"main": cleaned_section, "subsections": []})

    results.extend(page_results)

results = [r for r in results if r["subsections"]]

results_df = pd.DataFrame(results)

results_df.to_csv("results.csv", index=False)


