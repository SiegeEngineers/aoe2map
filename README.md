# aoe2map
[aoe2map.net](https://aoe2map.net) is a website to share and find Age of Empires II Random Map Scripts.

This is a Django application.

## Changelog

### 18.11.2

- When uploading a new version of a map, the `information` field is now also
  pre-filled with the text from the previous map version.

- Descriptions of Collections may now also contain markdown formatting.

- Bugfix: The names of `ZR@` maps do not get butchered anymore when downloading a
  Collection.

### 18.11.1

- The mappack creator now allows to individually configure the probability for each map to be chosen.

- Improved the map normalisation in the mappack creator.

- The `api/version` call now actually outputs useful information.

- Added `api/allmaps` call, which returns a list containing uuid, name, authors
  and version of all current maps.

### 18.11.0

- Added link to snippets page.

- Page titles are now more verbose.

- Maps without image did not display the placeholder image properly in search results
  and on the main page. This has been fixed.


### 18.10.6

Map cards were using large images instead of the smaller preview images, leading to
slower loading times and larger data usage. This has been fixed.

### 18.10.5

Fixed an issue where maps that were uploaded together with large images could not
be downloaded afterwards.

### 18.10.4

Uploaded images may now be at most 4200x4200 px in size. Images that are larger
in width and/or height are automatically resized to fit within those dimensions.

For each uploaded image, a preview image is automatically generated. 
It will contain the greatest possible area with the aspect
ratio of 600x311 from the center of the image. 
That means that after resizing, an equal amount of pixel rows will be removed 
either from the top and the bottom, or from the left and the right (if the image
does not have an aspect ratio of 600x311 already).

The website will display preview images. Clicking on a preview image on the
map detail page will open the full size image in a new tab.

Existing maps will use their existing images of 600x311 px as both main
and preview images.


### 18.10.3

- You can now add a map to one of your collections directly from the map page
- You can now add a map to a new collection directly from the map page
- Your collection pages now display an edit button
- Made map list on collection edit page more blocky

### 18.10.2

- Bugfix: When creating a new map, the changelog information is now actually saved.

### 18.10.1

- Added link to full map list at the end of the index page.
- Added filter input to maps and collections pages. Filter maps and collections 
  by typing in the filter input, the lists get updated instantly.

### 18.9.8

- Long descriptions are now shortened in map previews. They can be expanded to full 
  length by klicking/tapping on the description text.
- The mappack generator now generates the probabilities for each map more evenly
- Fixed an issue with tag names containing leading or trailing spaces
- Fix changelog field: Should be optional in new map form

### 18.9.7

- Added changelog field to maps. A changelog is displayed at the bottom of the map
  detail page if changelog text is available and/or if there are successive versions
  of the map (created via the 'Upload new version' functionality).
- Maps you own now show an 'Edit Map' button when you are logged in

### 18.9.6

- Links are now allowed in the description field. Use `[link text](https://example.org)` to create a link.
- Made form field descriptions even more descriptive

### 18.9.5

- The `Website` button is now only displayed if a url has been added

### 18.9.4

- The images in the map preview cards are now also a link to the respective map page
- Added OpenGraph tags to map pages, this creates pretty previews when a link to a map
  is shared on social media

### 18.9.3

- Rms files and images can now be drag+dropped into the new map and edit map forms. 
  You can unfortunately only drop one rms file _or_ one or multiple images at once, 
  not both at the same time. 
- Tags are now also copied from a map to the form when uploading a newer map version.

### 18.9.2

- Images can now be added and removed when editing a map
- Rms file input form input got moved to the top of form
- Alerts improved

### 18.9.1

- Mappack Creator: Reject ZR maps
- Images now must be 600x311 px (was 600x315 px)

### 18.9.0

Initial public version.

## Development setup

Let's assume you are on linux.

You should have installed: 
 - A recent version of Python 3 (Version 3.6 or above)
 - `virtualenv`
 - `pip3`
 - `git`

You can check your versions like this:

```
$ python3 --version
Python 3.6.5
$ virtualenv --version
15.1.0
$ pip3 --version
pip 9.0.1 from /usr/lib/python3/dist-packages (python 3.6)
$ git --version
git version 2.17.1
```

Clone this repository into a folder of your choice, 
this will create the `aoe2map` folder with all the relevant files:
```
git clone https://github.com/HSZemi/aoe2map.git
```
Now we set up a virtual python environment inside that folder
```
cd aoe2map
virtualenv -p python3 venv
```
A folder `venv` is created that contains the virtual python environment.

Now we activate that environment:
```
source venv/bin/activate
```
Your command line prompt should now show `(venv) ` at the beginning.

We install the required dependencies into our environment. 
They have been written down into `dependencies.txt`, so we just have to execute:
```
pip install -r dependencies.txt
```

We also want to install the development dependencies from `development.txt`:
```
pip install -r development.txt
```

Before we can start the application, we have to add a configuration file. 
We copy the template in the aoe2map _subfolder_, but for development, 
we do not have to edit anything inside.
```
cp aoe2map/deployment.py.template aoe2map/deployment.py
```


Now we get to work with Django itself. We initialize the database:
```
./manage.py migrate
```

… add a superuser:
```
./manage.py createsuperuser --username admin --email admin@example.org
```

… and can run the development server:

```
./manage.py runserver
```

It should say something like:
```
Performing system checks...

System check identified no issues (0 silenced).
September 10, 2018 - 19:03:25
Django version 2.1, using settings 'aoe2map.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

Open your browser and go to `http://localhost:8000` and you should see an 
empty aoe2map.net instance where you can login with the superuser we created earlier.

Further useful information:

 - The admin interface is then available at `http://localhost:8000/admin`
 - In the default development configuration, all emails the system would send
 get logged to the console instead
 - The development server reloads automatically when files change
 - I use PyCharm for development

## License
aoe2map.net  
Copyright © 2018 hszemi

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
