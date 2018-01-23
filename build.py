
import markdown

mdHTML = markdown.markdown("blog/hello_world.md")

print(mdHTML)

with open("index.html", "r") as myfile:
    data = myfile.read().replace('\n', '')

newdata = data.replace('{TEST}', '<p> pls work </p>')

newHTML = open("new.html", "w")

newHTML.write(newdata)
