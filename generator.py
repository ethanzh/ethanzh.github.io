import os
import markdown
from pathlib import Path


def get_blog_template():
    with open("templates/blog.html", "r") as inputfile:
        return inputfile.read()


def get_blog_markdown():
    return os.listdir("blog")


def process_metadata(raw_metadata):
    fields = ["TITLE", "SUBTITLE", "DATE"]
    metadata = {}
    # for every line, iterate through every key
    # this is not super efficient, but this will
    # also never be more than ~5 or so lines...
    for line in raw_metadata:
        for field in fields:
            # check if the field is in the line, if so then split the line
            # based on the field= and rstrip it
            if field in line and field not in metadata:
                metadata[field] = line.split(f"{field}=")[1].rstrip()
    # assert that we must have found every value
    assert len(metadata.values()) == len(
        fields
    ), "must have every field present in metadata"
    return metadata


def fill_template(data, template):
    assert "metadata" in data.keys()
    metadata = data.get("metadata")
    assert "TITLE" in metadata.keys()
    assert "SUBTITLE" in metadata.keys()
    assert "DATE" in metadata.keys()
    assert "body" in data.keys()

    subtitle, title, body = (
        metadata.get("SUBTITLE"),
        metadata.get("TITLE"),
        data.get("body"),
    )
    formatted_template = (
        template.replace("{SUBTITLE}", subtitle)
        .replace("{TITLE}", title)
        .replace("{BODY}", body)
    )

    return formatted_template


def read_blog_markdown(filename, template):
    with open(f"blog/{filename}", "r") as inputfile:
        lines = inputfile.readlines()

        # grab the metadata from the top of each markdown file
        break_indices = [i for i, val in enumerate(lines) if val == '"""\n']
        assert len(break_indices) == 2, "only two seperators should exist"
        lower_meta, upper_meta = break_indices[0] + 1, break_indices[1]

        # process lines, grab relevant information
        metadata = process_metadata(lines[lower_meta:upper_meta])

        # join the remaining lines together, format into HTML
        post_body = "".join(lines[upper_meta + 1 :])
        body_html = markdown.markdown(post_body)

        # format data for templating
        template_data = {"metadata": metadata, "body": body_html}

        # create directory structure based on date
        date = metadata.get("DATE")
        Path(date).mkdir(parents=True, exist_ok=True)

        # format title for directory structure
        title = metadata.get("SUBTITLE")
        formatted_title = title.replace(" ", "-").replace(":", "-").replace("--", "-").lower()

        # append date path with formatted title
        format_path = f"{date}/{formatted_title}.html"

        # write to html file at given directory
        formatted = fill_template(template_data, template)
        with open(format_path, "w") as outputfile:
            outputfile.write(formatted)


if __name__ == "__main__":
    # get all post markdown files
    posts = get_blog_markdown()

    # get the single blog template to reuse
    blog_template = get_blog_template()

    # create a formatted page for every blog post
    for i in posts:
        read_blog_markdown(i, blog_template)
