---START_METADATA---
{
  "title": "How I Built This Site",
  "author": "Ethan Houston",
  "summary": "Specifics about how I set up this website, and why I believe in it",
  "date": "11 February 2018",
  "private": "False",
  "tags": ["html", "python", "web"]
}
---END_METADATA---

This website was born out of my desire to try something new: web development.

Make no mistake, there is no shortage of tools that make it easy and simple to create a website, like Squarespace,
Weebly, and Wordpress. I immediately discounted these as it defeated the whole point of delving into web development.

I was initially daunted by the prospect of writing an entire website, CSS and all, from scratch. After expressing these
concerns to a friend, I was introduced to the notion of 'static site generation', something I have started to
(possibly inaccurately) refer to as a 'templating system'. Although there are [many](https://www.staticgen.com/) of these
services already in existence, I wanted to make my own.

This site is (at the moment) built by just one file, my [build.py](https://github.com/ethanzh/ethanzh.github.io/blob/master/build.py).
I chose Python for this simply because I thought it would be the quickest to set up, and easiest to maintain.

####How does build.py work?

When I write a blog post (as I'm doing right now), I write it in [Markdown](http://kirkstrobeck.github.io/whatismarkdown.com/), as it is
easily translated into HTML later, and I don't want to deal with writing HTML as I create a blog post. At the top of these Markdown files,
I have some metadata in the form of JSON, with information such as the post title, summary, date, tags, etc.

Although my build.py has become more and more complicated over the past few weeks, this is an oversimplified view of how it works:
1. Build.py finds all of the Markdown files in a certain directory (in my case, the 'content' folder)
2. The contents of each Markdown file are processed as strings, and then turned into HTML through [a Python Markdown library](https://pypi.python.org/pypi/Markdown)
3. These strings of newly-created HTML are then added into template HTML files I've created.

![Site structure](https://ethanhouston.com/img/articles/site-structure.png)

This is still the basic function of build.py, but I've found myself adding more features I would never have thought of even a week ago.
Among these is a 'tags' system, which I saw as an interesting problem to work on.

Python's weird mix of being part functional, part object-oriented has been useful in the creation of this site. For instance, every
blog post is turned into what I call a 'PostObject', that has information such as post length, link, and author (which will likely always be me).




