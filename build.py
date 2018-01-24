import markdown
import os, errno, shutil
import json
import re
import datetime
import operator

# TO-DO:
# Create new directories for each post, name file 'index.html'

DIRECTORY_NAME = os.path.basename(os.path.dirname(os.path.realpath(__file__)))  # Name of current directory
CURRENT_DIR = dir_path = os.path.dirname(os.path.realpath(__file__))  # Full path to current directory
BLOG_DIR = CURRENT_DIR + "/content"  # Gets path to blog folder
BLOG_FILE_NAMES = [os.path.join(os.path.dirname(os.path.abspath(__file__)), BLOG_DIR, i) for i in os.listdir(BLOG_DIR)]

CURRENT_POST_DIR = CURRENT_DIR + "/posts"
CURRENT_POST_NAMES = [os.path.join(os.path.dirname(os.path.abspath(__file__)), CURRENT_POST_DIR, i) for i in os.listdir(CURRENT_POST_DIR)]

markdown_file_locations = []

for i in BLOG_FILE_NAMES:
    if i[-2:] == "md":  # Finds all .md files in blog directory
        markdown_file_locations.append(i)


def get_template_html_as_text():
    with open("templates/post.html", "r") as html_file:
        return html_file.read()


def get_metadata_as_json(current_directory):
    with open(current_directory, "r") as md_file:

        metadata = md_file.read().rsplit('---END_METADATA---', 1)[0].split("---START_METADATA---", 1)[1]  # Get metadata

        json_metadata = json.loads(metadata)

        return json_metadata


def get_md_as_text(current_directory):
    with open(current_directory, "r") as md_file:

        return md_file.read().split("---END_METADATA---", 1)[1]  # Gets all text after END_METADATA


def process_markdown(current_directory):  # Returns [json, text]
    return get_metadata_as_json(current_directory), get_md_as_text(current_directory)


def md_to_html(md_string):
    return markdown.markdown(md_string)


def add_md_text_to_template(template, md_string, title):
    new_html_contents = template.replace('{TEST}', md_string)

    spaceless_title = title.replace(" ", "_")
    lower_title = spaceless_title.lower()
    final_title = re.sub(r'[^a-zA-Z0-9_]', '', lower_title)

    directory_so_far = "posts/"

    try:
        os.makedirs(directory_so_far + final_title)
        directory_so_far += final_title

        # post_links.append(directory_so_far + "/")
        new_html_location = directory_so_far + "/index.html"

        new_html_file = open(new_html_location, "w")
        new_html_file.write(new_html_contents)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    return directory_so_far + "/"


def create_post_html(path):

    template_html = get_template_html_as_text()  # Gets HTML template as string

    processed = process_markdown(path)  # [json, text]
    json = processed[0]
    text = processed[1]

    title = json['title']
    author = json['author']
    summary = json['summary']
    date = json['date']

    # post_titles.append(title)
    # post_summaries.append(summary)

    time = datetime.datetime.strptime(date, "%d %B %Y").timestamp()

    # post_dates.append(date)
    # post_time.append(time)

    md_html = md_to_html(text)  # Converts markdown text to HTML

    link = add_md_text_to_template(template_html, md_html, title)  # Creates new file, adds markdown HTML text

    post_objects.append(PostObject(title, link, date, summary, time))


def create_index():
    with open("templates/index.html", "r") as html_template:
        html_string = html_template.read()

        add_to_html = ""

        index_already_exists = (os.path.exists("index.html"))

        if index_already_exists:
            os.remove("index.html")

        try:

            sorted_list = sorted(post_objects, key=lambda x: x.time, reverse=True)

            for i in range(0, len(sorted_list)):

                add_to_html += "<div>"
                add_to_html += "<a href=" + sorted_list[i].link + ">" + sorted_list[i].title + "</a>"
                add_to_html += "<p>" + sorted_list[i].date + ". " + sorted_list[i].summary + "</p>"
                add_to_html += "</div><br />"

        except IndexError:
            pass

        new_html_contents = html_string.replace("{BLOG}", add_to_html)

        new_html_file = open("index.html", "w")
        new_html_file.write(new_html_contents)


class PostObject(object):

    def __init__(self, title, link, date, summary, time):
        self.title = title
        self.link = link
        self.date = date
        self.summary = summary
        self.time = time

    def set_link(self, link):
        self.link = link


post_objects = []


posts_exists = os.path.exists("posts/")

if posts_exists:
    shutil.rmtree("posts")
    os.makedirs("posts")

for i in markdown_file_locations:  # Goes through locations and creates .html files
    create_post_html(i)

create_index()

#print(sorted(post_time)[::-1])


