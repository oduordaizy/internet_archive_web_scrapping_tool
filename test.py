import os
import internetarchive as ia
import csv
from internetarchive import configure, Search, get_item, ArchiveSession

configure('victor.karimi@students.jkuat.ac.ke', 'Ld5vs$u2a$GAT6b')

def search_and_save(search_query, output_dir='docs', output_file='python_pdfs_test.csv'):
    session = ArchiveSession()

    count = 0
    fields = ['mediatype', 'identifier']
    search = Search(archive_session=session, query=search_query, fields=fields, sorts=['date desc'])

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, output_file)

    with open(output_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Identifier', 'Title', 'Author', 'Description', 'Collection', 'PDF_Link'])  # Added 'PDF_Link' to the header

        for item in search.iter_as_results():
            if count >= 250:
                break  # Exit the loop if count reaches 500

            if item['mediatype'] == 'texts':
                identifier = item['identifier']
                file_item = get_item(identifier)

                metadata = file_item.metadata
                title = metadata.get('title', 'unknown title')
                author = metadata.get('creator', ['Unknown Author'])[0]
                description = metadata.get('description', 'No Description Available')
                collection = metadata.get('collection', 'No collection Available')
                
                # Extract PDF link if available
                pdf_link = ''
                if 'pdf' in metadata:
                    pdf_link = metadata['pdf'][0]['url']

                count += 1
                print(f"count is {count} and identifier is {item['identifier']}")

                writer.writerow([identifier, title, author, description, collection, pdf_link])  # Added pdf_link to the row

if __name__ == "__main__":
    query = 'python programming'
    search_and_save(query)
