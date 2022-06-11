g = [
    "Alabama 4.461.130 7 0 637.304 4.062.608 7 0 580.373",
    "Alaska 628.933 1 0 628.933 551.947 1 0 551.947",
    "Arizona 5.140.683 8 2 642.585 3.677.985 6 1 612.998",
    "Arkansas 2.679.733 4 0 669.933 2.362.239 4 0 590.560",
    "California 33.930.798 53 1 640.204 29.839.250 52 7 573.832",
    "Colorado 4.311.882 7 1 615.983 3.307.912 6 0 551.319",
    "Connecticut 3.409.535 5 -1 681.907 3.295.669 6 0 549.278",
    "Delaware 785.068 1 0 785.068 668.696 1 0 668.696",
    "Florida 16.028.890 25 2 641.156 13.003.362 23 4 565.364",
    "Georgia 8.206.975 13 2 631.306 6.508.419 11 1 591.674",
    "Hawaii 1.216.642 2 0 608.321 1.115.274 2 0 557.637",
    "Idaho 1.297.274 2 0 648.637 1.011.986 2 0 505.993",
    "Illinois 12.439.042 19 -1 654.686 11.466.682 20 -2 573.334",
    "Indiana 6.090.782 9 -1 676.754 5.564.228 10 0 556.423",
    "Iowa 2.931.923 5 0 586.385 2.787.424 5 -1 557.485",
    "Kansas 2.693.824 4 0 673.456 2.485.600 4 -1 621.400",
    "Kentucky 4.049.431 6 0 674.905 3.698.969 6 -1 616.495",
    "Louisiana 4.480.271 7 0 640.039 4.238.216 7 -1 605.459",
    "Maine 1.277.731 2 0 638.866 1.233.223 2 0 616.612",
    "Maryland 5.307.886 8 0 663.486 4.798.622 8 0 599.828",
    "Massachusetts 6.355.568 10 0 635.557 6.029.051 10 -1 602.905",
    "Michigan 9.955.829 15 -1 663.722 9.328.784 16 -2 583.049",
    "Minnesota 4.925.670 8 0 615.709 4.387.029 8 0 548.379",
    "Mississippi 2.852.927 4 -1 713.232 2.586.443 5 0 517.289",
    "Missouri 5.606.260 9 0 622.918 5.137.804 9 0 570.867",
    "Montana 905.316 1 0 905.316 803.655 1 -1 803.655",
    "Nebraska 1.715.369 3 0 571.790 1.584.617 3 0 528.206",
    "Nevada 2.002.032 3 1 667.344 1.206.152 2 0 603.076",
    "NewHampshire 1.238.415 2 0 619.208 1.113.915 2 0 556.958",
    "NewJersey 8.424.354 13 0 648.027 7.748.634 13 -1 596.049",
    "NewMexico 1.823.821 3 0 607.940 1.521.779 3 0 507.260",
    "NewYork 19.004.973 29 -2 655.344 18.044.505 31 -3 582.081",
    "NorthCarolina 8.067.673 13 1 620.590 6.657.630 12 1 554.803",
    "NorthDakota 643.756 1 0 643.756 641.364 1 0 641.364",
    "Ohio 11.374.540 18 -1 631.919 10.887.325 19 -2 573.017",
    "Oklahoma 3.458.819 5 -1 691.764 3.157.604 6 0 526.267",
    "Oregon 3.428.543 5 0 685.709 2.853.733 5 0 570.747",
    "Pennsylvania 12.300.670 19 -2 647.404 11.924.710 21 -2 567.843",
    "RhodeIsland 1.049.662 2 0 524.831 1.005.984 2 0 502.992",
    "SouthCarolina 4.025.061 6 0 670.844 3.505.707 6 0 584.285",
    "SouthDakota 756.874 1 0 756.874 699.999 1 0 699.999",
    "Tennessee 5.700.037 9 0 633.337 4.896.641 9 0 544.071",
    "Texas 20.903.994 32 2 653.250 17.059.805 30 3 568.660",
    "Utah 2.236.714 3 0 745.571 1.727.784 3 0 575.928",
    "Vermont 609.890 1 0 609.890 564.964 1 0 564.964",
    "Virginia 7.100.702 11 0 645.518 6.216.568 11 1 565.143",
    "Washington 5.908.684 9 0 656.520 4.887.941 9 1 543.105",
    "WestVirginia 1.813.077 3 0 604.359 1.801.625 3 -1 600.542",
    "Wisconsin 5.371.210 8 -1 671.401 4.906.745 9 0 545.194",
    "Wyoming 495.304 1 0 495.304 455.975 1 0 455.975",
]
g = [i.split(" ") for i in g]

j = {i[0]: int(i[1].replace(".", "")) for i in g}
k = {i[0]: int(i[5].replace(".", "")) for i in g}

print(j)
print(k)
