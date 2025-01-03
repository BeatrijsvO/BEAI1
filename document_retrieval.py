import os

def fetch_documents_from_source(source_type: str, connection_details: dict):
    """
    Haalt documenten op van een specifieke bron.
    :param source_type: Type bron (bijv. "local", "database", "API").
    :param connection_details: Details voor de verbinding (bijv. pad, URL).
    :return: Lijst van documenten.
    """
    if source_type == "local":
        directory = connection_details.get("directory")
        return [os.path.join(directory, f) for f in os.listdir(directory)]
    elif source_type == "api":
        # Voeg logica toe voor API-oproep
        pass
    elif source_type == "database":
        # Voeg logica toe voor database-oproep
        pass
    else:
        raise ValueError("Unsupported source type.")