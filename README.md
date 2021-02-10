# How to install the project (Windows)

1. Install anaconda from this [url](https://www.anaconda.com)
2. Make sure you add anaconda into your PATH by 
   - type ```Edit the System Environment variables``` in your window search bar
   - Click on ```Environment variables```
   - Click on ```Path```
   - Click on the new empty block and put the anaconda's file location. For example, use ```C:\Users\your_name\anaconda3\Scripts``` if you installed it in default location
   - Click Ok and lauch your cmd or terminal again
   - Type ```conda init``` it should show something if you installed it correctly
   - Close your cmd or terminal and open it again 
   - Type ```conda activate```
3. Use ```git clone``` to clone this project to your PC
4. Edit the last section in ```environment.yml``` called prefix to path to anaconda in your computer
4. Run ```conda env create -f environment.yml``` to create enviroment called 'glance-dev'
5. Wait for the install to finish (this may take a while)
6. After everything is finished, type ```python app.py``` to run the program


# How to use image highlighing function

After run the program, it should be hosted on local port ```http://127.0.0.1:5000``` or url that shown on your cmd after run the python program. And use the below api with defined body to get the highlighted image.

```http://127.0.0.1:5000/highlight-image```

- ```imageUrl``` : Path to image you want to get highlighted
- ```isGrouped``` : Group nearby product together or not
- ```productCoords``` : list of products' coordinate (x1, y1, x2, y2) ** one sub-list refer to one product **

```
{
    "imageUrl": "https://[BASE_URL]/R1S5.2.jpg",
    "isGrouped": false,
    "productCoords": [
        [
            "2041 8 2231 392", 
            "1838 2 2027 386", 
            "1435 8 1624 395", 
            "1236 11 1425 392", 
            "2236 19 2420 389", 
            "1028 11 1217 392", 
            "2430 8 2624 392", 
            "824 5 1018 392", 
            "1634 11 1823 383", 
            "2643 11 2856 389", 
            "615 0 814 395", 
            "412 5 596 380", 
            "0 0 198 369", 
            "194 0 388 366"
        ], 
        [
            "1212 1267 1402 1674", 
            "1004 1273 1193 1668", 
            "1402 1273 1587 1665"
        ], 
        [
            "383 1270 577 1674", 
            "175 1273 364 1662", 
            "601 1273 786 1668", 
            "795 1278 990 1662", 
            "4 1278 170 1656"
        ], 
        [
            "1838 611 2013 974", 
            "2037 602 2226 980", 
            "2653 608 2842 986", 
            "2240 602 2430 983", 
            "2449 611 2629 986", 
            "2856 613 3027 983", 
            "1624 599 1823 974"
        ], 
        [
            "2643 1287 2837 1671", 
            "1823 1276 2027 1668", 
            "2449 1281 2638 1665", 
            "2037 1278 2245 1665", 
            "2240 1284 2430 1665", 
            "1634 1278 1823 1659", 
            "2847 1296 3022 1671"
        ]
    ]
}
```