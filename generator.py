from datetime import datetime
import shutil
import markdown
from pathlib import Path
import os

"""
Objectives of this script:
- Input: `blog/YYYY/MM/DD` (Markdown files)
- Output:
    - index.html
    - `posts/YYYY/MM/DD` (HTML files)
"""


class BlogPost:
    title: str
    subtitle: str
    timestamp: datetime
    html_path: str
    markdown: str
    tags: list[str]

    def __init__(
        self,
        title: str,
        subtitle: str,
        timestamp: datetime,
        html_path: str,
        markdown: str,
        tags: list[str],
    ) -> None:
        self.title = title
        self.subtitle = subtitle
        self.timestamp = timestamp
        self.html_path = html_path
        self.markdown = markdown
        self.tags = tags


INPUT_DIR = "blog"
OUTPUT_DIR = "posts"


def read_blog_posts() -> list[BlogPost]:
    blog_posts = []
    input_dir = Path(INPUT_DIR)

    for md_file in input_dir.glob("**/*.md"):
        with open(md_file, "r") as file:
            lines = file.readlines()
            metadata_start = lines.index("```\n") + 1
            metadata_end = lines.index("```\n", metadata_start)
            metadata_lines = lines[metadata_start:metadata_end]

            metadata = {}
            for meta_line in metadata_lines:
                key, value = meta_line.strip().split("=")
                metadata[key] = value

            title = metadata["title"]
            subtitle = metadata["subtitle"]
            tags = metadata["tags"].split(", ")

            if not title or not subtitle or not tags:
                raise Exception("Missing required metadata")

            markdown_lines = lines[metadata_end + 1 :]
            markdown = "\n".join(markdown_lines)

            year, month, day = map(int, md_file.parts[-4:-1])
            timestamp = datetime(year, month, day)
            md_filename = md_file.parts[-1]
            html_filename = md_filename.replace(".md", ".html")

            blog_post = BlogPost(
                title=title,
                subtitle=subtitle,
                timestamp=timestamp,
                tags=tags,
                markdown=markdown,
                html_path=f"{OUTPUT_DIR}/{year}/{month}/{day}/{html_filename}",
            )
            blog_posts.append(blog_post)

    return blog_posts


def convert_markdown_to_html(markdown_input: str) -> str:
    parsed_markdown = markdown.markdown(markdown_input)
    return parsed_markdown

def write_index(blog_posts: list[BlogPost]) -> None:
    with open("templates/index.html", "r") as file:
        index_template = file.read() 

    post_links = "\n".join(
        f'<li><a href="{post.html_path}">{post.timestamp.strftime("%Y-%m-%d")} - {post.title}</a></li>'
        for post in blog_posts
    )
    index_content = index_template.replace("{post_links}", post_links)

    with open("index.html", "w") as output_file:
        output_file.write(index_content) 


def main() -> None:
    blog_posts = read_blog_posts()

    posts_dir = Path("posts")
    if posts_dir.exists() and posts_dir.is_dir():
        for file in posts_dir.iterdir():
            if file.is_file():
                file.unlink()
            elif file.is_dir():
                shutil.rmtree(file)
        posts_dir.rmdir()

    with open("templates/blog.html", "r") as file:
        post_template = file.read()

    print(f"Found {len(blog_posts)} posts")
    for blog_post in blog_posts:
        html_str = convert_markdown_to_html(blog_post.markdown)

        formatted_html_str = (
            post_template.replace("{title}", blog_post.title)
            .replace("{subtitle}", blog_post.subtitle)
            .replace("{body}", html_str)
            .replace("{timestamp}", blog_post.timestamp.strftime("%Y-%m-%d"))
            .replace("{tags}", ", ".join(blog_post.tags))
        )

        output_path = blog_post.html_path
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as output_file:
            output_file.write(formatted_html_str)

    num_posts_on_index = 5
    sorted_blog_posts = sorted(blog_posts, key=lambda post: post.timestamp, reverse=True)
    newest_blog_posts = sorted_blog_posts[:num_posts_on_index] if len(sorted_blog_posts) >= num_posts_on_index else sorted_blog_posts
    write_index(newest_blog_posts)


if __name__ == "__main__":
    main()
