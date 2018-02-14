---START_METADATA---
{
  "title": "How I Built This Site",
  "author": "Ethan Houston",
  "summary": "Specifics about how I set up this website, and why I believe in it",
  "date": "13 February 2018",
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

Part of the beauty of this site (in my eyes) is its quick performance, which is something I've put a lot of effort into. This is what influenced me
to do (almost) all the design from scratch, rather than use something like Bootstrap (which could significantly slow down load times).

![Chrome F12](https://ethanhouston.com/img/articles/inspect.JPG)

Apart from my style sheets and compressed images, this website doesn't need a whole lot to run, which I find helpful. This is also helped by
the fact that the site is hosted on GitHub pages, meaning it's GitHub's CDN being used, which is without a doubt more powerful than anything I could host myself.

Cloudflare (the reason this site has HTTPS) is both a godsend and an annoyance. While it does provide a great set of tools for monitoring the site, and changing
DNS settings, I've spend far, *far* more time than I would like to admit on trying to diagnose CSS errors that were simply due to Cloudflare having cached old versions

![Cloudflare Caching panel](https://ethanhouston.com/img/articles/cloudflare.JPG)

###### This is quickly becoming one of my most-visited websites.

Previously, I had been worried about the viability of having one file process every website-related HTML file (as it also generated the home page, the "projects" view, 
the "all posts" view, etc), but it really just comes down to simple file I/O and string manipulation, so even when I run build.py with 50,000 Markdown files, it still takes
less than a second to run. If I ever organically get to that many posts, something good must have happened along the way.

I set up the 'tags' system I mentioned before with the goal of filling this personal site with not only traditional 'blog' posts about things that are
important to me, but to also write articles to help people understand how things work (such as this article). I'm doing this because although I find
StackOverflow to be an invaluable resource when I'm working on something, one can sometimes be inundated with too many conflicting answers, whereas one
article written by one person is normally much easier to follow, and, in my experience, slightly more likely to work. Using tags will help me
differentiate between 'blog' posts, and tutorials (which will be tagged by the related programming languages and concepts used).

I hope this article was helpful in explaining the way in which I've chosen to build this website. It took a little while for me to wrap my head around the
concept of not hand-coding every HTML page, but it's definitely a terrific time-saver, with changes to the template being reflected in a fraction of a second throughout
the entire website 

![PyCharm build time](https://ethanhouston.com/img/articles/time.JPG)


