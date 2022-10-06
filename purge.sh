#!/bin/bash

# ========================================
# This script will analyze the HTMLs on the web (40dex for now), and use [PurgeCSS](https://purgecss.com/) to remove the unused CSS defined by [Bootstrap](https://getbootstrap.com/)
# ========================================

# Download the HTML (we can't use the local jinja template)
wget http://elpekenin.tk/40dex/ --output-document 40dex.html

# Purge
purgecss --css static/css/bootstrap.min.css --content 40dex.html --output static/css/purged.css

# Remove HTML file
rm 40dex.html
