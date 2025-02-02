import re
import json

md_pattern = r'\[(.*?)\]\((.*?)\)'

key_words = [
    'Jr-Sr 71',
    'Prince of Peace Memorial',
    'DECA DCM',
    'DECA Charlotte',
    'DECA Rocky Mt',
    'DECA Boss Banquet',
    'DECA 25',
    'Busch Gardens',
    "Brenda Gail's Shower",
    'Bob Jones U',
    'Dist Runner-up',
    'Amy Jo Gussom',
    'Busch Gardens',
    'Boys Basketball',
    'Amy Elmore',
    'Jeremy',
    'Ick'
]


def get_properties(line):
    match_object = re.search(md_pattern, line)
    caption = match_object.group(1)
    key = get_key_from_caption(caption)
    image = match_object.group(2)

    return {
        'key': key, 
        'caption': caption, 
        'image': image
        }


def get_key_from_caption(caption):
    for key in key_words:
        if key in caption:
            return key
        
    return caption


def get_map(filename):
    map = {}

    with open(filename, 'r') as file:
        lines = file.readlines()

        for line in lines:
            props = get_properties(line)

            if props['key'] in map:
                map[props['key']].append((props['image'], props['caption']))
            else:
                map[props['key']] = []
                map[props['key']].append((props['image'], props['caption']))

    return dict(sorted(map.items()))


def write_html(filename, map):
    for key, images in map.items():
        write_json(key, images)
    
    with open(filename, 'w') as file:
        write_header(file)
        write_links(file, map)
        file.write('<div id="slideshow" class="container mt-5"></div>\n\n')
        write_script(file)
        write_footer(file)


def write_header(file):
        file.write(
            '<!DOCTYPE html>\n'
            '<html>\n'
            '<head>\n'
            '  <meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">'
            '  <link href="style.css" rel="stylesheet">'
            '</head>\n'
            '<body>\n'
            '\n'
        )


def write_footer(file):
    file.write(
        '\n'
        '</body>\n'
        '</html>\n'
    )


def write_json(key, images):
    className = get_class_name(key)
    filename = f"{className}.json"
    
    definition = {
        "className": className,
        "key": key,
        "images": [{"source": img[0], "caption": img[1]} for img in images]
    }


    with open(filename, 'w') as file:
        file.write(json.dumps(definition, indent=2))

def write_links(file, map):

    file.write('<div class="container fixed-top text-center mt-1">\n')
    file.write('  <button class="btn btn-light btn-sm dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">\n')
    file.write('    Select a Category\n')           
    file.write('  </button>\n')
    file.write('  <ul class="dropdown-menu">\n')

    for key in map:
        text = key if len(key) > 0 else "Not Labeled"
        className = get_class_name(key)
        file.write(f'    <li><a class="dropdown-item" onclick="showSlides(\'{className}\')">{text}</a></li>\n')

    file.write('  </ul>\n')
    file.write('</div>\n')


def get_class_name(key):
    if key == "":
        return "no_key"
    return key.replace(" ", "").replace("'", "").replace("&", "").replace("-", "").replace(",", "").lower()


def write_script(file):
    file.write('\n')
    file.write('<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>\n')
    file.write('<script src="slides.js" type="text/javascript"></script>\n')
    file.write('\n')


map = get_map('Proof Sheet.md')

write_html('index.html', map)