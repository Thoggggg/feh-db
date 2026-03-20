import re


def get_from_template(text, template):
    template = template.replace("?", "@")
    text = text.replace("?", "@")
    text = text.replace("%", "ù")

    # Match the text with the template
    m = re.findall(template, text)

    # Find the matched
    if len(m) == 0:
        logging.warning(f"No match found in {text} with {template}")
    else:
        return m

    return []


def extract_default(html: str, template_file: str, extract_id: int) -> str:
    # Open the template file
    template = open(template_file, "r", encoding='utf-8').read()

    # Get the regex matches
    extracted_values = get_from_template(html, template)

    # Return if something has be found
    if len(extracted_values) > 0:
        return extracted_values[0][extract_id]
    else:
        raise Exception(f"Couldn't catch anything from {template_file}")
