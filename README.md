# Purdue University's Programming Languages Group

Welcome!

## Adding/Updating Members

Open an issue! We have a template for adding new members to the website. If you want to update your information or add a picture, just open a normal issue or submit a pr.

### Resizing pictures
All images are displayed at a 120x120 ratio. Use `convert image.jpeg -resize 120x120 image_small.jpeg` to get the proper sizing.

## Testing the Website

Either:

- Install Ruby and subsequent dependencies. Then use `./serve`
- Install Docker and run `docker run --rm --volume="${PWD}:/srv/jekyll" -p 4000:4000 -it jekyll/jekyll:3.8 jekyll serve --incremental --drafts --config _config.yml` from the root of this project
