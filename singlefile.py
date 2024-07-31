import pypandoc

input_file = "G:/My Drive/IARS 2024/6. Proposal Narrative.docx"
output_file = "G:/My Drive/IARS 2024/6. Proposal Narrative.pdf"

pypandoc.convert_file(input_file, 'pdf', outputfile=output_file)
