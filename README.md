This Python script retrieves WHOIS information for a given domain name using the WhoisXML API
and formats the data into a markdown table.
The output is ready to be pasted into markdown editors such as Dillinger.io.

### Requirements ###
Python 3.7+
install requests

Usage
1- Run : sol.py
2- Enter your WhoisXML API key and the domain name when prompted.
3- Copy the generated markdown table and paste it into any markdown editor like Dillinger.io.

### Error Handling ###
1- If the API key or domain name is missing, the script will handle the error gracefully and notify the user.
2- If no data is available for a specific field, "N/A" will be displayed.
3- If failed to get domain details will raise an error.

### Notes ###
1- Dates are in ISO-8601 format.
2- Hostnames longer than 25 characters are truncated with ....
3- Missing fields display "N/A".
4- If a contact name field is missing, the organization field is used instead.
