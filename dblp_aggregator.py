from SPARQLWrapper import SPARQLWrapper, JSON
import json

# Define SPARQL endpoint
DBLP_SPARQL_ENDPOINT = "https://sparql.dblp.org/sparql"

# DBLP Author ID
AUTHOR_ID = "332/1508"

def fetch_dblp_data(author_id):
    """
    Fetches comprehensive paper data from DBLP using SPARQL.
    
    Args:
        author_id (str): DBLP author ID (e.g., '332/1508').
    
    Returns:
        list: List of papers with detailed metadata.
    """
    # SPARQL query
    query = f"""
    PREFIX dblp: <http://dblp.org/rdf/schema#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX dc: <http://purl.org/dc/elements/1.1/>

    SELECT ?title ?year ?url ?bibtex ?pages ?venue ?type ?id
    WHERE {{
        ?pub dblp:authoredBy <https://dblp.org/pid/{author_id}> ;
             dc:title ?title ;
             dblp:year ?year ;
             dblp:publishedIn ?venue ;
             dblp:type ?type ;
             dblp:primaryFullTextUrl ?url .
        OPTIONAL {{ ?pub dblp:bibtex ?bibtex }}
        OPTIONAL {{ ?pub dblp:page ?pages }}
        BIND(REPLACE(STR(?pub), "http://dblp.org/rec/", "") AS ?id)
    }}
    ORDER BY DESC(?year)
    """

    # Configure SPARQL endpoint
    sparql = SPARQLWrapper(DBLP_SPARQL_ENDPOINT)
    print(query)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    # Perform the query
    results = sparql.query().convert()

    # Parse results
    papers = []
    for result in results["results"]["bindings"]:
        paper = {
            "id": result.get("id", {}).get("value", "N/A"),
            "title": result.get("title", {}).get("value", "N/A"),
            "year": result.get("year", {}).get("value", "N/A"),
            "venue": result.get("venue", {}).get("value", "N/A"),
            "type": result.get("type", {}).get("value", "N/A"),
            "url": result.get("url", {}).get("value", "N/A"),
            "bibtex": result.get("bibtex", {}).get("value", "N/A"),
            "pages": result.get("pages", {}).get("value", "N/A"),
        }
        papers.append(paper)
    
    return papers

def save_to_json(data, filename):
    """
    Saves data to a JSON file.
    
    Args:
        data (list): List of dictionaries to save.
        filename (str): File name for the JSON file.
    """
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    try:
        print("Fetching publications from DBLP using SPARQL...")
        papers = fetch_dblp_data(AUTHOR_ID)

        if papers:
            output_file = "dblp_papers_detailed.json"
            save_to_json(papers, output_file)
        else:
            print("No papers found.")
    except Exception as e:
        print(f"An error occurred: {e}")
