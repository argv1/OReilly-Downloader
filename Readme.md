# OReilly-Downloader
======================

## Purpose
Check the availabilty of O'Reillys free ebooks, create html page for better overview and downloadability.

## Current overview
If you just interested in an up-to-date overview, check out [Ebook Overview](https://github.com/argv1/OReilly-Downloader/blob/master/ebook_overview.md)

## Usage
run pip to ensure all requirements are fulfilled
 
```bash
pip3 install -r requirements.txt
```
</br>

after that adjust your working path "base_path"
</br>
</br>
now you can run the script:

Add new URLS:
```bash
main.py -m A FILENAME
```

Check the availability of the ebooks:
```bash
main.py -m C
```

Create new html overview:
```bash
main.py -m D
```

## License
This code is licensed under the [GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/). 
For more details, please take a look at the [LICENSE file](https://github.com/argv1/OReilly-Downloader/blob/master/LICENSE).

## Outlook
Feel free to adjust the code
