# Bluebook-Scan-Sis-Update
The project is made as a part of Digital Image Processing learning. The user needs to scan the picture of the bluebook containing the marks and the USN. 
The project currently requires this picture to be feeded to the cloned repository and named as text.jpg.
The flask file can now be executed on the terminal, which shall perform **Optical Character Recognition** on the image, extract the require details, and automatically update it to the mock SIS created for this purpose.

## Requirements
- Account on Google Cloud Platform
- API key ready with the Google Cloud Vision API enabled
- Flask
- Python

Detailed explanation can be seen in the 2 pdf's provided in the repository.

## Instructions
```
git clone https://github.com/amyy28/DIP_Project.git
```

Install google cloud and run the file vision.py. 
Wait while it extracts the data from the image.
Hit the localhost URL to find the updated mock SIS.

### Preferrable to use a virtual environment to avoid unnecessary dependencies being bulked on the system.
