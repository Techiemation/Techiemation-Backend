import requests
from bs4 import BeautifulSoup


def get_text_content(tag):
    content = []
    for child in tag.children:
        if child.name == 'pre' or child.name == 'code':
            code_content = child.get_text(strip=True)
            if code_content:
                content.append(f"```\n{code_content}\n```")
        elif child.string:
            text_content = child.string.strip()
            if text_content:
                content.append(text_content)
        else:
            content.append(get_text_content(child))
    return '\n'.join(content)


def scrape_webpage(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        # print(soup.prettify())

        # Initialize an empty dictionary to store the heading-paragraph pairs
        heading_para_dict = {}

        # Find all headings and their corresponding paragraphs
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        # print(headings)
        for heading in headings:
            # Extract the heading text
            heading_text = heading.get_text().strip()

            # Find the next paragraph after the heading
            # next_para = heading.find_next_sibling('p')
            next_para = heading.find_next('p')

            # If a paragraph exists, extract its text
            if next_para:
                para_text = next_para.get_text().strip()

                # Add the heading and its corresponding paragraph to the dictionary
                heading_para_dict[heading_text] = para_text
        # print(heading_para_dict)
        return heading_para_dict

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    # url = 'https://developer.mozilla.org/en-US/docs/Web/HTML'
    url = "https://docs.julialang.org/en/v1/manual/strings/"
    # url = "https://doc.rust-lang.org/book/ch01-03-hello-cargo.html"
    # url = "https://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes.html"
    print(scrape_webpage(url))