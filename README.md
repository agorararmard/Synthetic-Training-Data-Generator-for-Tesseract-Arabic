## Words Corpus:
  It's essential to have a Corpus of words or sentences to use in the training. The training data should be stored in a simple text file and saved into:
  ```
    cd ./image-generation/text-corpus
  ```
  The data can be composed of sentences or words, space separated or end-line separated.

  You can use the already existing space-separated data set [elmenus-text.txt](./image-generation/text-corpus/elmenus-text.txt) This dataset was collected manually from Elmenus website and it includes around 1800 unique words.

  or you can add your own data-set to the folder in .txt extension.

## Useful Utils:
### Changing Space Separated Dataset to Endline Separated Dataset:
  If you have a space separated dataset and would like to convert it into an endline separated one, you can simply use the following command, running ``` useful-utils/stoe.py ``` python script:
  ```
    python steo.py argv[1] argv[2]

    argv[1]: the text file where the original dataset is stored. (Space-Separated Dataset)
    agrv[2]: the name of the text file that the resulting dataset should be stored in. (Endline-Separated Dataset)
  ```
### Changing JPG Images in the directory to Tiff Images:
  You can convert JPG images into equivalent Tiff images using the following python script: ``` useful-utils/jpg_to_tif.py ``` by using this command:
  ```
    python jpg_to_tif.py argv[1]

    argv[1]: The directory in which the jpg images are located
  ```
### Changing Yollo Box Format to Tesseract Box Format:
  If you have manually labeled boxes in Yollo Format, you can change it into Tesseract Format box files. You can do that simply using the following python script ``` useful-utils/yollo_to_box.py ``` running this command:
  ```
    python yollo_to_box.py argv[1]

    argv[1]: The directory in which the jpg/box pairs are located
  ```
### Predefined classes for all characters English + Arabic + Symbols:
  If you are about to use manual labeling or looking for the list of characters English + Arabic + Symbols, you can find it in [useful-utils/predefined_classes.txt](./useful-utils/predefined_classes.txt) running this command:

## Image Generation:
#### Dependencies:
  Dependencies for image generation:
  ```
    The code is tested on:
    Python 3.6
    Python 2.6

    installing tesseract:
      sudo apt install tesseract-ocr
      sudo apt install libtesseract-dev

    Pre-existing folders:
      - ./fonts
       including:
        * Fonts to be used the training.
        * fonts.txt including the true names from the info of each font end-line separated
      - ./text-corpus
        including:
         * Dataset to be used
  ```
#### Image Generation output:
  After running the generation code, you should have a folder called ```./image-generation/generated-data``` The folder will include a randomized data-set containing tif/box file pairs along with the ground truth in text format.
  Each .tif file is an image containing the text extracted from corresponding ground truth and the box file includes the annotated box of each character in the image. fonts differ and sizes differ in a randomized way. All output files begin with the prefix Sample, that can be changed in the code.

#### Running The code:
  To generate the training data-set, you have to run [generator.py](./image-generation/generator.py). It takes 3 arguments:
  ```
    First Argument: The number of generated images per font. In other words, the total number of ground-truths generated.
    Second Argument: The state of the input data to be handled by the generator.
    Third Argument: the name of the text file to extract the data from that is placed inside ./image-generation/text-corpus folder
    ```
    ```
    The state of the input data is given as an integer number using the first 2 binary digits as flags:

    Declaring the state of the input data:
        0 : is endline separated sentences;
        1 : is endline separated words;
        3 : is space separated words;


        looked at in binary format as a bit mask:
        First binary digit:
            True: The data is given as separate words
            False: The data is given as separate sentences
        Second binary digit:
            True: The data is space separated
            False: The data is endline separated
  ```
  a sample command line run:
  ```
    python generator.py 1200 3 elmenus-text.txt

    This will generate 1200 image for each font inside the /fonts folder extracting word separated words from ./image-generation/text-corpus/elmenus-text.txt and output the generated files into ./image-generation/generated-data
  ```
