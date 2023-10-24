# Purdue University's Programming Languages Group

Welcome!

## Adding/Updating Members

Open an issue! We have a template for adding new members to the website. If you want to update your information or add a picture, just open a normal issue or submit a pr.

### Resizing pictures

All images are displayed at a 120x120 ratio. Use `convert image.jpg -resize 120x120^ -extent 120x120 -gravity center image_small.jpg` to get the proper sizing.

A more modern web format can be converted to using `cwebp -m 6 -q 80 -mt -af -progress image.jpg -o image.webp`

## Testing the Website

Either:

- Install Ruby and subsequent dependencies. Then use `./serve`
- Install Docker and run `docker run --rm --volume="${PWD}:/srv/jekyll" -p 4000:4000 -it jekyll/jekyll:3.8 jekyll serve --incremental --drafts --config _config.yml` from the root of this project

### Troubleshooting

You might run into an error when attempting to build the site. The first thing to check is if you have a stale `Gem.lock` or `_site`. Nuke one or both of these and try a fresh build before anything else.
