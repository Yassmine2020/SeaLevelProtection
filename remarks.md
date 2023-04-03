Here are my remarks for paths_generation:

- I’d like the roads to be in this format:

for example:

 T_Ci[8] = 

[entry0  zone01 zone02 zone03 asset     nan   nan

 entry1  zone11 zone12 zone13 zone14 asset nan 

 entry2  zone21 zone22 asset    nan       nan    nan]

⇒ Which means T_Ci[8] is a matrix: each line presents the road i & I want to start from the entry to the assets, not the inverse 

- If we will give the entries the height of the sea level rise then we will not need the variable entries as the output of the function generator(), and we will put instead their height in the matrix of region

- I added smthg in the code : from line 14 to 18 number of rows and cols
- generator function : returns also this number of rows and cols