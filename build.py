import markdown
import os, errno, shutil
import json
import re
import datetime
import time

# TO-DO:
# Create new directories for each post, name file 'index.html'

start_time = time.time()

DIRECTORY_NAME = os.path.basename(os.path.dirname(os.path.realpath(__file__)))  # Name of current directory
CURRENT_DIR = dir_path = os.path.dirname(os.path.realpath(__file__))  # Full path to current directory
BLOG_DIR = CURRENT_DIR + "/content"  # Gets path to blog folder
BLOG_FILE_NAMES = [os.path.join(os.path.dirname(os.path.abspath(__file__)), BLOG_DIR, i) for i in os.listdir(BLOG_DIR)]

PROJECTS_DIR = CURRENT_DIR + "/projects"  # Gets path to blog folder
PROJECTS_FILE_NAMES = [os.path.join(os.path.dirname(os.path.abspath(__file__)), PROJECTS_DIR, i) for i in os.listdir(PROJECTS_DIR)]

CURRENT_POST_DIR = CURRENT_DIR + "/posts"
CURRENT_POST_NAMES = [os.path.join(os.path.dirname(os.path.abspath(__file__)), CURRENT_POST_DIR, i) for i in os.listdir(CURRENT_POST_DIR)]

markdown_file_locations = []
project_file_locations = []

WPM = 275
WORD_LENGTH = 5

for i in BLOG_FILE_NAMES:
    if i[-2:] == "md":  # Finds all .md files in blog directory
        markdown_file_locations.append(i)

for i in PROJECTS_FILE_NAMES:
    if i[-4:] == "json":
        project_file_locations.append(i)


def get_template_html_as_text():
    with open("templates/post.html", "r") as html_file:
        return html_file.read()


def get_project_template_as_text():
    with open("templates/projects.html", "r") as html_file:
        return html_file.read()


def get_metadata_as_json(current_directory):
    with open(current_directory, "r") as md_file:

        metadata = md_file.read().rsplit('---END_METADATA---', 1)[0].split("---START_METADATA---", 1)[1]  # Get metadata

        json_metadata = json.loads(metadata)

        return json_metadata


def calculate_reading_time(word_count, wpm, text):

    number_images = text.count("![")

    total_time = number_images * 0.2  # Assuming each picture takes 12 seconds to look at

    total_time += (word_count / wpm)

    return total_time


def get_md_as_text(current_directory):
    with open(current_directory, "r") as md_file:

        body_text = md_file.read().split("---END_METADATA---", 1)[1]

        length = len(body_text)

        word_count = length / WORD_LENGTH  # Assuming average word length is 5

        reading_time = calculate_reading_time(word_count, WPM, body_text)

        return_list = [body_text, reading_time]

        return return_list  # Gets all text after END_METADATA


def process_markdown(current_directory):  # Returns [json, text]
    return get_metadata_as_json(current_directory), get_md_as_text(current_directory)


def md_to_html(md_string):
    return markdown.markdown(md_string)


def add_md_text_to_template(template, md_string, title, title_html, reading_time_html, summary):

    new_html_contents = template.replace('{TABTITLE}', title)

    new_html_contents = new_html_contents.replace('{TITLE}', title_html)

    new_html_contents = new_html_contents.replace('{TIME}', reading_time_html)

    new_html_contents = new_html_contents.replace('{BODY}', md_string)

    summary_string = "content=\"" + summary + "\""

    new_html_contents = new_html_contents.replace('{SUMMARY}', summary_string)

    spaceless_title = title.replace(" ", "-")
    lower_title = spaceless_title.lower()
    final_title = re.sub(r'[^a-zA-Z0-9-]', '', lower_title)

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
    text = processed[1][0]
    reading_time = processed[1][1]

    reading_time = str(int(round(reading_time)))

    title = json['title']
    author = json['author']
    summary = json['summary']
    date = json['date']
    private = json['private']

    if private == "True":
        private = True
    else:
        private = False

    time = datetime.datetime.strptime(date, "%d %B %Y").timestamp()

    md_html = ""

    md_html += md_to_html(text)  # Adds the markdown HTML

    title_html = "<h2 id=\"title_button\" href=\"/\">" + title + "</h2>"

    reading_time_html = "<p class=\"read_time\">" + reading_time + " min read</p>"

    link = add_md_text_to_template(template_html, md_html, title, title_html, reading_time_html, summary)  # Creates new file, adds markdown HTML text

    post_objects.append(PostObject(title, link, date, summary, time, reading_time, private))


def add_index_to_template(number, template):

    if template == "all":
        open_template = "templates/all.html"
        template = "all/index"
    else:
        open_template = "templates/" + template + ".html"

    with open(open_template, "r") as html_template:
        html_string = html_template.read()

        add_to_html = ""

        index_already_exists = (os.path.exists(template + ".html"))

        if number == "all":
            number = len(post_objects)

        if index_already_exists:
            os.remove(template + ".html")

        try:

            sorted_list = sorted(post_objects, key=lambda x: x.time, reverse=True)

            for i in range(0, number):

                if not sorted_list[i].private:

                    add_to_html += "<div>"
                    add_to_html += "<a class=\"post_link\" href=" + sorted_list[i].link + ">" + sorted_list[
                        i].title + "</a>"
                    add_to_html += "<p>" + sorted_list[i].date + ". " + sorted_list[i].summary + "</p>"

                    if i == (len(sorted_list) - 1):
                        add_to_html += "</div>\n                "

                    else:
                        add_to_html += "</div><br />\n                "

        except IndexError:
            pass

        new_html_contents = html_string.replace("{POSTS}", add_to_html)

        print(template)

        new_html_file = open(template + ".html", "w")
        new_html_file.write(new_html_contents)


class PostObject(object):

    def __init__(self, title, link, date, summary, time, reading_time, private):
        self.title = title
        self.link = link
        self.date = date
        self.summary = summary
        self.time = time
        self.reading_time = reading_time
        self.private = private

    def set_link(self, link):
        self.link = link


class ProjectObject(object):

    def __init__(self, name, link, summary):
        self.name = name
        self.link = link
        self.summary = summary


project_objects = []


def create_projects():
    for i in range(0, len(project_file_locations)):
        with open(project_file_locations[i], "r") as json_file:
            json_data = json.load(json_file)
            project_objects.append(ProjectObject(json_data['name'], json_data['link'], json_data['summary']))

    with open("templates/projects.html", "r") as html_template:
        html_string = html_template.read()

        add_to_html = ""

        index_already_exists = (os.path.exists("projects.html"))

        if index_already_exists:
            os.remove("projects.html")

        try:

            for i in range(0, len(project_objects)):

                add_to_html = project_objects[i].name + ": " + project_objects[i].link

        except IndexError:
            pass

        new_html_contents = html_string.replace("{HERE}", add_to_html)

        new_html_file = open("projects.html", "w")
        new_html_file.write(new_html_contents)


post_objects = []
posts_exists = os.path.exists("posts/")


if posts_exists:
    shutil.rmtree("posts")
    os.makedirs("posts")

for i in markdown_file_locations:  # Goes through locations and creates .html files
    create_post_html(i)

#create_index()
add_index_to_template(2, "index")
add_index_to_template("all", "all")

create_projects()

print("--- %s seconds ---" % (time.time() - start_time))