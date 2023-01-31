# Placeholdy

A website/service I created for generating *simple placeholder images* that I can embed in my new web applications:

```html
<img alt="A placeholder with the size 512x512"
     src="https://placeholdy.fly.dev/placeholder?width=512&height=512"/>
```

Which returns the following image:

<img alt="A placeholder with the size 512x512" src="https://placeholdy.fly.dev/placeholder?width=512&height=512" width="80" height="80"/>

The service supports customizing width and height and colors of the image and the text.

Documentation is available [on the homepage](https://placeholdy.fly.dev/).

## Tech stack

> **➡️Psst!** All of the code is located within the [website](website/) folder. I have it as a subfolder
> in case if I want to add anything cool here in the future. 😎

### API / Image generation

The backend is written using [Python](https://python.org) and [Flask](https://flask.palletsprojects.com). Image generation is done using [Pillow](https://pillow.readthedocs.io/), a fork of
the image generation library PIL.

> **💡 Stay fast!** Once an image has been generated (requested) once, it is automatically saved in a cache directory
> (with the default configuration) to avoid additional computation power and requests.

### Documentation

The documentation is hosted by the Flask server that is running the script. It is made using [Pico CSS](https://picocss.com/),
a new CSS framework I tried and was quite happy with.

## Installation

All steps assume you've edited the [configuration file](website/config.json5) and filled out the values
you want. It is quite straightforward. There are comments there and it uses the cool [JSON5](https://json5.org) syntax!

The steps also assume that you have moved to the correct directory: `cd website/`
### Automatic

#### Using Fly.io
1. Create a new app on Fly.io
2. Create a volume that mounts on `/images` for storing the generated images
3. Deploy the app.

#### Using anything else
Start from the [Dockerfile](website/Dockerfile) and make some magic.

### Manual
1. Install requirements using `pip -r requirements.txt`
2. **For development:** `python run_app_dev`.
3. **For production** Run a WSGI server, for example Gunicorn: `gunicorn app:create_app() --bind=host:port`
