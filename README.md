# Homography Editor

Demonstration of the effects of different types of transformation.

Check blog posts:
[Medium](https://medium.com/@insight-in-plain-sight/deconstructing-the-homography-matrix-35989ecc0b2)
[Personal Homepage](https://hanqiu-jiang.science/blog_entries/04_deconstructing_homography.html)


Usage:
```
# Install dependencies
pip install -r requirements.txt

# Create images for each type of transformation
python homography.py

# Feed custom image
python homography.py -p "./path/image"

# Interactive mode for different transforms
python homography.py -i e
python homography.py -i s
python homography.py -i a
python homography.py -i p
```