import requests
import time

from bs4 import BeautifulSoup

from utils import insert_data


class CodeforcesParser:
    def __init__(
        self, 
        interval: int | None = 0,
        url: str | None = "",
        start_page_num: int | None = 1,
        end_page_num: int| None = 1,
        ) -> None:
    
        self.current_page = start_page_num
        self.end_page = end_page_num
        self.url = url if url else f"https://codeforces.com/problemset/page/{self.current_page}?order=BY_SOLVED_DESC" 


    def parse_problems(self):
        with requests.Session() as session:
            with session.get(self.url) as response:
                html = response.text
                soup = BeautifulSoup(html, "html.parser")
                problem_rows = soup.find("table", {"class": "problems"}).find_all("tr")[1:]

                parsed = False
                while True:
                    try:
                        self.parse_page(problem_rows) 
                        print("page parsed")
                    except AttributeError:
                        print("End of page")
                    finally:
                        #if self.current_page == self.end_page:
                        #    parsed = True
                        time.sleep(3600)
                        self.current_page += 1


    def parse_page(self, problem_rows):
        # loop through the rows and extract the required data
        for row in problem_rows:
            problem_data = self.parse_row(row)
            #print(problem_data)
            insert_data(problem_data)     


    def parse_row(self, row) -> dict:
        data = dict()
        all_a = row.find_all("a") # to extract links

        data['url'] = self.url
        # extract the problem number
        data['number'] = all_a[0].text.strip()

        # extract the problem name
        data['name'] = all_a[1].text.strip()

        # extract the problem difficulty
        data['difficulty'] = int(row.find("span", {"class": "ProblemRating"}).text.strip())

        # extract the problem tags and convert them into a list
        data['topics'] = [t.text.strip() for t in row.find_all("a", {"class": "notice"})]

        # extract the number of solutions
        data['solutions'] = int(all_a[-1].text.strip().replace("x",""))

        return data
       


if __name__ == "__main__":
    c = CodeforcesParser(start_page_num=1, end_page_num=1).parse_problems()