import datetime
import errno
import json
import os
import re
import shutil
import time
import markdown

start_time = time.time()

DIRECTORY_NAME = os.path.basename(os.path.dirname(os.path.realpath(__file__)))  # Name of current directory
CURRENT_DIR = dir_path = os.path.dirname(os.path.realpath(__file__))  # Full path to current directory

BLOG_DIR = os.path.join(CURRENT_DIR, "content")  # Gets path to blog folder
BLOG_FILE_NAMES = [os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                BLOG_DIR, i) for i in os.listdir(BLOG_DIR)]

PROJECTS_DIR = os.path.join(CURRENT_DIR, "projects")  # Gets path to blog folder
PROJECTS_FILE_NAMES = [os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    PROJECTS_DIR, i) for i in os.listdir(PROJECTS_DIR)]

CURRENT_POST_DIR = os.path.join(CURRENT_DIR, "posts")
CURRENT_POST_NAMES = [os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   CURRENT_POST_DIR, i) for i in os.listdir(CURRENT_POST_DIR)]

markdown_file_locations = []
project_file_locations = []

WPM = 275
WORD_LENGTH = 5

post_objects = []
project_objects = []
tag_list = []

# TODO: For 'all' page, make max 8 posts per page: ethanhouston.com/all/2, etc
# TODO: Natural Language Analysis (think more about this)


class PostObject(object):

    def __init__(self, title, link, date, summary, post_time, reading_time, private, tags):
        self.title = title
        self.link = link
        self.date = date
        self.summary = summary
        self.time = post_time
        self.reading_time = reading_time
        self.private = private
        self.tags = tags

    def set_link(self, link):
        self.link = link


class ProjectObject(object):

    def __init__(self, name, link, summary, platforms, wip):
        self.name = name
        self.link = link
        self.summary = summary
        self.platforms = platforms
        self.wip = wip


def get_template(template):
    with open(os.path.join("templates", template + ".html"), "r") as html_file:
        return html_file.read()


def get_metadata_as_json(current_directory):
    with open(current_directory, "r") as md_file:

        metadata = md_file.read().rsplit('---END_METADATA---', 1)[0].split("---START_METADATA---", 1)[1]  # Get metadata

        json_metadata = json.loads(metadata)

        return json_metadata


def calculate_reading_time(word_count, wpm, text):

    number_images = text.count("![")
    total_time = 0

    if number_images > 10:
        total_time += 1.25
        total_time += (number_images - 10)

    elif number_images != 1:
        total_time += 0.01667 * ((number_images * 12) - (((number_images ** 2) + number_images) / 2))

    else:
        total_time += 0.2

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


def add_md_text_to_template(template, md_string, title, title_html, reading_time_html, summary, tags):

    new_tag_html = create_html_tag("p", "Tags: ", css="post_tags")

    for i in range(0, len(tags)):

        tag_string = tags[i]

        if i != len(tags) - 1:
            tag_string += " - "

        new_tag_html += create_html_tag("a", tag_string, css="post_tag_links", href="/tags/" + tags[i])

    summary_string = "content=\"" + summary + "\""
    spaceless_title = title.replace(" ", "-")
    lower_title = spaceless_title.lower()
    final_title = re.sub(r'[^a-zA-Z0-9-]', '', lower_title)
    directory_so_far = "posts"

    replacements = {

        "TABTITLE": title,

        "TITLE": title_html,

        "TIME": reading_time_html,

        "BODY": md_string,

        "TAGS": new_tag_html,

        "SUMMARY": summary_string

    }

    new_html_contents = html_replace(template, replacements)

    try:

        os.makedirs(os.path.join(directory_so_far, final_title))

        index_less_location = os.path.join("posts", final_title)
        new_html_location = os.path.join("posts", final_title, "index.html")

        new_html_file = open(new_html_location, "w")
        new_html_file.write(new_html_contents)

    except OSError as e:

        index_less_location = None
        if e.errno != errno.EEXIST:
            raise

    return index_less_location


def create_post_html(path):

    template_html = get_template("post")

    processed = process_markdown(path)  # [json, text]
    processed_json = processed[0]
    text = processed[1][0]
    reading_time = processed[1][1]

    reading_time = str(int(round(reading_time)))

    title = processed_json['title']
    # author = processed_json['author']
    summary = processed_json['summary']
    date = processed_json['date']
    private = processed_json['private']
    tags = processed_json['tags']

    for i in tags:

        if i not in tag_list:

                if private == "False":
                    tag_list.append(i)

    if private == "True":
        private = True
    else:
        private = False

    post_time = datetime.datetime.strptime(date, "%d %B %Y").timestamp()

    md_html = ""

    md_html += md_to_html(text)  # Adds the markdown HTML

    change_list = \
        [["img", "h6"],
         ["article_image", "caption"]]

    change_dict = {

        "img": "article_image",
        "h6": "caption"

    }

    md_html = custom_markdown_class(change_list, md_html)

    md_html = md_html.replace("<a", "<a target=\"_blank\"")

    title_html = create_html_tag("h2", "TEST", href="/", css="title_button")

    title_html = title_html.replace("TEST", create_html_tag("a", title, css="title_link", href="/"))

    print(title_html)

    reading_time_html = create_html_tag("p", reading_time + " min read", css="read_time")

    # Creates new file, adds markdown HTML text
    link = add_md_text_to_template(template_html, md_html, title, title_html, reading_time_html, summary, tags)

    post_objects.append(PostObject(title, link, date, summary, post_time, reading_time, private, tags))


def custom_markdown_class(change_list, md_text):

    # TODO: change from array to dictionary

    for i in range(0, len(change_list[0])):
        md_text = md_text.replace("<" + change_list[0][i], "<" + change_list[0][i] +
                                  " class=\"" + change_list[1][i] + "\"")

    return md_text


def add_index_to_template(number, template):

    template_file = template + ".html"

    if template == "all":
        open_template = os.path.join("templates", "all.html")
        template = "all/index"
    else:
        open_template = os.path.join("templates", template_file)

    with open(open_template, "r") as html_template:
        html_string = html_template.read()

        add_to_html = ""

        index_already_exists = os.path.exists(template_file)

        if number == "all":
            number = len(post_objects)

        if index_already_exists:
            os.remove(template_file)

        try:

            sorted_list = sort_by_time(post_objects)

            sorted_list = [i for i in sorted_list if not i.private]

            for i in range(0, number):

                if not sorted_list[i].private:

                    add_to_html += create_blurb(sorted_list[i])

        except IndexError:
            pass

        new_html_contents = html_string.replace("{POSTS}", add_to_html)

        if template == "all/index":
            tag_dict = create_tag_dict()

            tag_html = ""

            for tag in tag_dict:

                tag_html += create_html_tag("a", tag, css="tag_links", href="/tags/" + tag + "/") + "<br />"

            new_html_contents = new_html_contents.replace("{TAGS}", tag_html)

        new_html_file = open(template + ".html", "w")
        new_html_file.write(new_html_contents)


def create_projects():

    with open(os.path.join("projects", "list.json"), "r", encoding="utf-8") as json_file:

        json_data = json.load(json_file)

        for i in range(0, len(json_data)):
            project_objects.append(ProjectObject(json_data[i]['name'], json_data[i]['link'],
                                                 json_data[i]['summary'], json_data[i]['platforms'],
                                                 json_data[i]['wip']))

    html_string = get_template("projects")

    add_to_html = ""

    index_already_exists = (os.path.exists("projects.html"))

    if index_already_exists:
        os.remove("projects.html")

    try:

        add_to_html = ""

        for i in range(0, len(project_objects)):

            platforms = project_objects[i].platforms.count(",")

            add_to_html += "<div>"

            add_to_html += create_html_tag("a", project_objects[i].name, css="post_link",
                                           href=project_objects[i].link, target="_blank")

            if project_objects[i].wip:
                add_to_html += create_html_tag("p", " [WORK IN PROGRESS]", css="wip")

            add_to_html += create_html_tag("p", project_objects[i].summary)

            if platforms == 0:
                platform_text = "Platform: "
            else:
                platform_text = "Platforms: "

            add_to_html += create_html_tag("p", platform_text + project_objects[i].platforms)

            if i == (len(project_objects) - 1):
                add_to_html += "</div>\n                "

            else:
                add_to_html += "</div><br />\n                "

    except IndexError:
        pass

    new_html_contents = html_string.replace("{HERE}", add_to_html)

    new_html_file = open(os.path.join("projects", "index.html"), "w")
    new_html_file.write(new_html_contents)


def create_tag_dict():
    tag_dict = {}

    for i in tag_list:
        current_list = []

        for j in range(0, len(post_objects)):

            if i in post_objects[j].tags:
                current_list.append(post_objects[j])

            tag_dict[i] = current_list

    return tag_dict


def create_blurb(post):

    iter_string = "<div>"

    iter_string += create_html_tag("a", post.title, css="post_link",
                                   href="/" + post.link)

    iter_string += create_html_tag("p", post.date + ". " + post.summary)

    iter_string += "</div>"

    return iter_string


def sort_by_time(post_list):
    return sorted(post_list, key=lambda x: x.time, reverse=True)


def create_tag_pages():

    tag_dict = create_tag_dict()

    for tag in tag_dict:

        iter_string = ""

        for i in range(0, len(tag_dict[tag])):

            tag_dict[tag] = sort_by_time(tag_dict[tag])  # This somehow works.

            if not tag_dict[tag][i].private:

                iter_string += create_blurb(tag_dict[tag][i])

        try:
            os.makedirs("tags/" + tag)

            directory_so_far = "tags/" + tag + "/"

            template_html = get_template("tag")

            replacements = {

                "TAGS": iter_string,

                "TAGNAME": "#" + tag.lower(),

                "HEADTITLE": "#" + tag.lower()

            }

            template_html = html_replace(template_html, replacements)

            new_tag_html = open(directory_so_far + "index.html", "w")
            new_tag_html.write(template_html)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise


def html_replace(original, replace_dict):

    for key, value in replace_dict.items():
        original = original.replace(
            "{" + key + "}",
            str(value)
        )

    return original


def create_html_tag(tag, content, **kwargs):

    html = "<" + tag

    for key, value in kwargs.items():

        if key == "css":
            key = "class"

        html += " " + key + "=\"" + value + "\""

    html += ">" + content + "</" + tag + ">"

    return html


def build_lists():
    for i in BLOG_FILE_NAMES:
        if i[-2:] == "md":  # Finds all .md files in blog directory
            markdown_file_locations.append(i)

    for i in PROJECTS_FILE_NAMES:
        if i[-4:] == "json":
            project_file_locations.append(i)


def reset_dirs():

    folders_to_reset = ["posts", "tags"]

    for i in folders_to_reset:
        if os.path.exists(i):
            shutil.rmtree(i)
            os.makedirs(i)


def run():

    build_lists()

    reset_dirs()

    for i in markdown_file_locations:  # Goes through locations and creates .html files
        create_post_html(i)

    add_index_to_template(2, "index")
    add_index_to_template("all", "all")

    create_tag_pages()
    create_projects()

    print("--- %s seconds ---" % (time.time() - start_time))


run()
