# Poodle bug test site

Site at http://silvaneves.org/poodle/ that regularly updates whether a bunch of sites have SSLv3 still enabled.

# Requirements

 * nmap
 * python 2.7 (hasn't been tested with other versions)

# Usage

Update the sites list in ```scripts/poodlebug.py```.

Run: ```scripts/poodlebug.py```

This generates the index.html file that is visible to the users. Setup the static site anyway you wish.

