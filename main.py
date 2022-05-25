import requests
from bs4 import BeautifulSoup
import json

def nameDistribution(startYear, endYear, top, mode):
    """
        Returns a dictionary containing the distribution of names per year per gender and creates the corresponding json file
    :param startYear: First year taken in consideration
    :param endYear: Final year taken into consideration
    :param top: How many top names to consider per year
    :param mode: "p" gets percentages, "n" gets number of births
    :return: Dictionary in the form {'year': {'male'/'female': {'name': float(xx.yyyy)}}}
    """
    root = {}
    for year in range(startYear, endYear+1):
        url = "https://www.ssa.gov:443/cgi-bin/popularnames.cgi"
        data = {"year": year, "top": top, "number": mode}
        res = requests.post(url, data=data)
        soup = BeautifulSoup(res.text, features="lxml")

        maleNames = {}
        femaleNames = {}
        for row in soup.select('tr tr')[1:-1]:
            mName, mPer, fName, fPer = tuple(map(lambda x: x.text, row.select('td')[1:]))
            maleNames[mName] = float(mPer[:-1])
            femaleNames[fName] = float(fPer[:-1])

        root[str(year)] = {"male":maleNames, "female":femaleNames}

    # print(root)
    with open("names.json", "w") as f:
        json.dump(root, f)
    return root



if __name__ == '__main__':
    nameDistribution(1880, 2021, 250, "p")

