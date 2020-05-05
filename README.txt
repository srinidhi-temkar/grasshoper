Team Name: BC_114_255_879
Topic: Greenest Part

Our project aimed at collecting satellite images of the 198 wards of Bangalore through
google maps (phase 1), followed by processing each of them seperately to get the green cover
present in each ward and abstracting this data into a csv file (phase 2), and finally using 
hadoop's hdfs and mapreduce to analyse the data for creating a list of wards with above 
75% green cover and also noting the ward with the highest green cover (phase 3).

Phase 1:
The first phase was automated using selenium web driver and python on mozilla firefox. 
The script also makes use of a add-on(browser extension called "No Transition") to disable all CSS transitions and
animations, thus making the process of screencapture faster. List of wards is fed as txt file.
Moreover, each screencapture is taken in two google map views, viz., the normal view and the 
satellite view, whose importance will be expounded on in phase 2. The image is then cropped
to include just the region and remove all irrelevant elements from the picture.
This process takes roughly 30 minutes for completion.

This particular implementation has been named as screenie_v2.py in the files contained
within Phase 1. The generic implementation that will work with just firefox, web driver,
and python is named screenie_v1.py

Phase 2:
The second phase utilises the capabilities of openCV to take this preprocessed image and 
crop it to the ward's border to only include ward. This is done using two images.
The first image of the ward in the traditional 2D layout outlines the ward with a red border.
The region enclosed by the border is selected through the detection of its contours.
This region is now overlapped onto the satellite image and the remaining is cast out. Now, 
the satellite image contains only the region bounded by the ward. Following that, 
greensapce analysis is performed on this image and the precentage green cover is stored in
a csv file.

Phase 3:
The HDFS and its mapreduce libraries are used to perform analysis on the csv file to get
information on: the wards containing more than 75% green cover, and the ward that contains
the most green cover.

Challenges Faced:

1. Certain wards weren't bounded clearly using google maps. There were 3 cases observed:
wards showed 2 diconnected boundaries, searches that did not yield results of wards but
other things: like a road or a temple, and boundaries that were considered too small to be
considered wards.
Wards without border:
	2
	17
	18
	22
	34
	75
	77
	87
	94
	102
	115
	119
	126
	129
	142
	165
	166
	178
	196

Opportunities Siezed:

1. Our screenshot algorithm has been tested for speed and accuracy. It certainly is one of
the fastest.

2. Our openCV border detection and greenspcae detection is also of great accuracy that
has been tuned to improve performance over multiple attempts. The enitre execution
is completed in under 20 seconds for 198 wards.

3. We have created a python notebook that grahpically illustrates the process followed by
our OpenCV implementation.


Final Note:
We have been thorough with out approach and planned each stage as meticulously as possible,
and also desgined metrics to analyse our own performance. We have tried to respect this 
project as an engineering project and believe that we have learnt and improved immensely
over the past few days. It is our most sincere request that our effort and results be looked
upon favourably and our humble desire that we be given an opportunity to work at CCBD.
We earnestly look forward to the future in the hope of collaborating, learning and improving
with the professors and our peers at CCBD.


