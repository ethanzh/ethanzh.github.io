import markdown
import os

DIRECTORY_NAME = os.path.basename(os.path.dirname(os.path.realpath(__file__)))  # Name of current directory
CURRENT_DIR = dir_path = os.path.dirname(os.path.realpath(__file__))  # Full path to current directory
BLOG_DIR = CURRENT_DIR + "/content/markdown"  # Gets path to blog folder
BLOG_FILE_NAMES = [os.path.join(os.path.dirname(os.path.abspath(__file__)), BLOG_DIR, i) for i in os.listdir(BLOG_DIR)]

for i in BLOG_FILE_NAMES:
    if i[-2:] == "md":  # Finds all .md files in blog directory
        print(i)


def get_template_html_as_text():
    with open("post_template.html", "r") as html_file:
        return html_file.read()


def get_md_as_text():
    with open("content/markdown/hello_world.md", "r") as md_file:

        metadata = md_file.read().rsplit('---END_METADATA---', 1)[0].split("---START_METADATA---", 1)[1]
        print(metadata)

        return md_file.read()


def md_to_html(md_string):
    return markdown.markdown(md_string)


def add_md_text_to_template(template, md_string):
    new_html_contents = template.replace('{TEST}', md_string)

    new_html_file = open("content/generated/output.html", "w")
    new_html_file.write(new_html_contents)


template_html = get_template_html_as_text()  # Gets HTML template as string

md_text = get_md_as_text()  # Gets markdown as pure text

md_html = md_to_html(md_text)  # Converts markdown text to HTML

add_md_text_to_template(template_html, md_html)  # Creates new file, adds markdown HTML text
