import datetime
import requests

# Retrieves domain information using the WhoisXML API.
def get_domain_details(domain, api_key):
    url = f"https://www.whoisxmlapi.com/whoisserver/WhoisService?domainName={domain}&apiKey={api_key}&outputFormat=JSON"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        print(f"Error: Unable to fetch data for {domain}. Reason: {error}")
        return None

# Converts a given date to ISO-8601 format or returns "N/A" if invalid.
def format_date_iso(date_string):
    try:
        parsed_date = datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S%z")
        return parsed_date.isoformat()
    except Exception:
        return "N/A"

# Formats WHOIS data into the exact markdown-style table required by the task.
def create_output_table(whois_data):
    # Extract key details from the API response
    domain_name = whois_data.get("domainName", "N/A")
    registrar = whois_data.get("registrarName", "N/A")
    registration_date = format_date_iso(whois_data.get("createdDate"))
    expiration_date = format_date_iso(whois_data.get("expiresDate"))
    estimated_age = whois_data.get("estimatedDomainAge", "N/A")

    # Extract hostnames and truncate if necessary
    name_servers = whois_data.get("nameServers", {}).get("hostNames", [])
    hostnames = ", ".join(name_servers)
    if len(hostnames) > 25:
        hostnames = hostnames[:25] + "..."

    # Handle contact information
    registrant_info = whois_data.get("registrant", {})
    registrant_name = registrant_info.get("name", registrant_info.get("organization", "N/A"))
    technical_contact = whois_data.get("technicalContact", {}).get("name", "N/A")
    admin_contact = whois_data.get("administrativeContact", {}).get("name", "N/A")
    contact_email = registrant_info.get("email", "N/A")

    # Create markdown table
    table = f"""
| **Domain Name**        | **Registrar**        | **Registration Date** | **Expiration Date**  | **Estimated Domain Age** | **Hostnames**         |
|-------------------------|----------------------|------------------------|-----------------------|--------------------------|-----------------------|
| {domain_name}           | {registrar}         | {registration_date}    | {expiration_date}     | {estimated_age}          | {hostnames}          |

| **Registrant Name**     | **Technical Contact Name** | **Administrative Contact Name** | **Contact Email** |
|--------------------------|---------------------------|----------------------------------|-------------------|
| {registrant_name}        | {technical_contact}       | {admin_contact}                 | {contact_email}   |
"""
    print(table)

# Main function to execute the WHOIS API lookup task.
def run_task():
    # Get the API key and domain from the user
    # example :
    # api_key : at_iNdqfiDpt5WNutlCamV67wYZCLCbJ
    # domain : amazon.com

    api_key = input("Enter your WhoisXML API key: ").strip()
    if not api_key:
        raise ValueError("API key cannot be empty.")

    domain = input("Enter the domain name: ").strip()
    if not domain:
        raise ValueError("Domain name cannot be empty.")

    print(f"Fetching WHOIS data for: {domain}")
    data = get_domain_details(domain, api_key)

    if data and "WhoisRecord" in data:
        create_output_table(data["WhoisRecord"])
    else:
        raise ValueError("No valid data received from the API.")


if __name__ == "__main__":
    run_task()

