# Placeholdy

A website/service I created for generating *simple placeholder images* that I can embed in my new web applications:

```html
<img alt="A placeholder with the size 512x512"
     src="https://placeholdy.albins.website/placeholder?width=512&height=512"/>
```

Which returns the following image:

<img alt="A placeholder with the size 512x512" src="https://placeholdy.albins.website/placeholder?width=512&height=512"/>

The service supports customizing width and height and colors of the image and the text.

Documentation is available [on the homepage](https://placeholdy.albins.website/).

### API / Image generation

The backend is written using Python and Flask. Image generation is done using Pillow, a fork of
the image generation library PIL.

> Once an image has been generated (requested) once, it is automatically saved in a cache directory
> (with the default configuration) to avoid additional computation power and requests.

### Documentation

The documentation is hosted by the Flask server that is running the script.
