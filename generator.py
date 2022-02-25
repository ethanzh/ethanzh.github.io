import os
from typing import List
import markdown
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class Metadata:
    title: str = field(default="")
    subtitle: str = field(default="")
    date: str = field(default="")


def get_blog_template():
    with open("templates/blog.html", "r") as inputfile:
        return inputfile.read()


def get_blog_markdown():
    return os.listdir("blog")


def process_metadata(raw_metadata: List[str]) -> Metadata:
    fields = ["TITLE", "SUBTITLE", "DATE"]
    metadata = Metadata()
    # for every line, iterate through every key
    # this is not super efficient, but this will
    # also never be more than ~5 or so lines...
    for line in raw_metadata:
        for field in fields:
            # check if the field is in the line, if so then split the line
            # based on the field= and rstrip it
            if field in line:
                setattr(
                    metadata,
                    field.lower(),
                    line.split(f"{field}=")[1].rstrip(),
                )

    return metadata


def fill_template(metadata: Metadata, body: str, template: str):

    subtitle, title, body = (
        metadata.subtitle,
        metadata.title,
        body,
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

        # create directory structure based on date
        date = metadata.date
        Path(f"posts/{date}").mkdir(parents=True, exist_ok=True)
        filename = filename.replace(".md", "")

        # append date path with formatted title
        format_path = f"posts/{date}/{filename}.html"

        # write to html file at given directory
        formatted = fill_template(metadata, body_html, template)
        with open(format_path, "w") as outputfile:
            outputfile.write(formatted)


if __name__ == "__main__":
    # get all post markdown files
    posts = get_blog_markdown()

    # get the single blog template to reuse
    blog_template = get_blog_template()

    # create a formatted page for every blog post
    for i in posts:
        if i == "template.md" or ".md" not in i:
            continue
        read_blog_markdown(i, blog_template)
