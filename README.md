# Purdue University's Programming Languages Group

Welcome!

## Adding/Updating Members

Open an issue! We have a template for adding new members to the website. If you want to update your information or add a picture, just open a normal issue or submit a pr.

### Resizing pictures

All images are displayed at a 120x120 ratio. To resize and center images:

```bash
magick image.jpg -resize 120x120^ -gravity center -extent 120x120 image_small.jpg
cwebp -m 6 -q 80 -mt -af -progress image_small.jpg -o image_small.webp
```

## Testing the Website

Either:

- Install Ruby 3.3.4 and run `bundle install`. Then use `./serve` to preview, and `./check` to build and validate links the way CI does.
- Install Docker and run `docker run --rm --volume="${PWD}:/srv/jekyll" -p 4000:4000 -it jekyll/jekyll:3.8 jekyll serve --incremental --drafts --config _config.yml` from the root of this project

### Troubleshooting

You might run into an error when attempting to build the site. The first thing to check is `ruby -v` — the `Gemfile` requires 3.3.4, and a mismatch fails with a missing-bundler error that reads as unrelated. After that, check for a stale `Gemfile.lock` or `_site`.
