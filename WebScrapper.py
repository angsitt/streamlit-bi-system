import requests
from bs4 import BeautifulSoup
import csv
import time
from DBConnection import DBConnection
from credentials import DB_USERNAME, DB_PASSWORD
from datetime import datetime

SERVER = 'localhost, 1433'
DATABASE = 'epam_reviews'

URL1 = 'https://www.careerbliss.com/epam-systems/reviews/'
FILE1 = 'reviews.csv'

URL2 = 'https://dreamjob.ru/employers/53815'
FILE2 = 'dreamjob_reviews.csv'

URL3 = 'https://career.habr.com/companies/epamanywhere/scores/2021'
FILE3 = 'habr_reviews.csv'

class WebScrapper:

    def __init__(self, url, file_name):
        self.url = url
        self.file_name = file_name
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 YaBrowser/20.9.0.928 Yowser/2.5 Safari/537.36',
            'accept': '*/*'
        }

    def get_html(self, params=None):
        req = requests.get(self.url, headers=self.headers, params=params)
        return req

    def get_pages(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        pagination = soup.find('div', class_='pagination-container')
        pages = pagination.find('ul', class_='pagination clearfix first-page-active').find_all('li')
        last_page = str(pages[-2].find('a').get('href'))
        pagination = int(last_page[-1:])
        return pagination

    def get_content(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('div', class_='company-reviews')
        reviews = []
        for item in items:
            try:
                job_title = item.find('a', class_='job-title header5 twocentChromeExt').get('data-jobtitle')
                comment = item.find('p', class_='comments foggy')
                if comment:
                    comment = comment.get_text(strip=True)
                else:
                    comment = None
                reviews.append({
                    'job_title': job_title,
                    'comment': comment,
                    'source': 'CareerBliss'
                })
            except:
                reviews.append({
                    'job_title': 'EXCEPTION',
                    'comment': 'EXCEPTION',
                    'source': 'CareerBliss'
                })
        return reviews

    def save_file(self, items):
        with open(self.file_name, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['job_title', 'comment', 'source'])
            for item in items:
                writer.writerow([item['job_title'], item['comment'], item['source']])
            print('Data is successfully written.')

    def parse(self):
        html = self.get_html()
        if html.status_code == 200:
            reviews = []
            pages_count = self.get_pages(html.text)
            for page in range(0, pages_count + 1):
                print(f'Scraping of the {page + 1}/{pages_count + 1} web-page...')
                html = self.get_html(params={'page': page})
                reviews.extend(self.get_content(html.text))
                time.sleep(3)
            self.save_file(reviews)
            print(f'There are {len(reviews)} reviews.')
        else:
            print('Error!')


class CareerBlissScrapper(WebScrapper):

    def __init__(self, url, file_name):
        super().__init__(url, file_name)

    def get_pages(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        pagination = soup.find('div', class_='pagination-container')
        pages = pagination.find('ul', class_='pagination clearfix first-page-active').find_all('li')
        last_page = str(pages[-2].find('a').get('href'))
        pagination = int(last_page[-1:])
        return pagination

    def get_content(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('div', class_='company-reviews')
        reviews = []
        for item in items:
            try:
                job_title = item.find('a', class_='job-title header5 twocentChromeExt').get('data-jobtitle')
                comments = item.find_all('p', class_='comments foggy')
                if comments:
                    comment = " ".join([comment.get_text(strip=True) for comment in comments])
                else:
                    comment = 'N/A'
                rating = item.find('div', class_='rating-container')
                location = item.find('span', class_='header13').find('a')
                if location:
                    location = location.get_text(strip=True)
                else:
                    location = 'N/A'
                rating_stars = rating.find('div', class_='rating large-star')
                if rating_stars:
                    score = 0
                    stars = rating_stars.find_all('span')
                    for star in stars:
                        star_score = star.get('class')[0]
                        if star_score == 'full':
                            score += 1
                        elif star_score == 'half':
                            score += 0.5
                        elif star_score == 'quarter':
                            score += 0.25
                        elif star_score == 'three-quarters':
                            score += 0.75
                else:
                    score = -1
                reviews.append({
                    'job_title': job_title,
                    'location': location,
                    'comment': comment,
                    'score': score,
                    'source': 'CareerBliss'
                })
            except:
                reviews.append({
                    'job_title': 'EXCEPTION',
                    'location': 'EXCEPTION',
                    'comment': 'EXCEPTION',
                    'score': -1,
                    'source': 'CareerBliss'
                })
        return reviews

    def save_file(self, items):
        with open(self.file_name, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['job_title', 'location', 'comment', 'score', 'source'])
            for item in items:
                writer.writerow([item['job_title'], item['location'], item['comment'], item['score'], item['source']])
            print('Data is successfully written.')

    def parse(self):
        html = self.get_html()
        if html.status_code == 200:
            reviews = []
            pages_count = self.get_pages(html.text)
            for page in range(0, pages_count + 1):
                print(f'Scraping of the {page + 1}/{pages_count + 1} web-page...')
                html = self.get_html(params={'page': page})
                reviews.extend(self.get_content(html.text))
                time.sleep(3)
            self.save_file(reviews)
            print(f'There are {len(reviews)} reviews.')
        else:
            print('Error!')


class DreemjobScrapper(WebScrapper):

    def __init__(self, url, file_name):
        super().__init__(url, file_name)

    def get_content(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('div', class_='review')
        reviews = []
        for item in items:
            try:
                job_title = item.find('h3', class_='review__header').get_text(strip=True)
                review_date = item.find('div', class_='review__date').get_text(strip=True)
                tags = item.find_all('div', class_='tags__item')
                current_employee = True if tags[0].get_text(strip=True) == 'Работаю в компании' else False
                work_experience = tags[2].get_text(strip=True).replace('Продолжительность работы: ', '')
                location = tags[3].get_text(strip=True)
                comments = item.find_all('div', class_='review__text')
                review = comments[0].get_text(strip=True)
                review += ". ".join([tag.get_text(strip=True) for tag in tags[4:]])
                improvement_idea = comments[1].get_text(strip=True)
                rating = item.find('div', class_='dj-rating').find('span', class_='dj-rating__value')
                score = rating.get_text(strip=True)
                reviews.append({
                    'job_title': job_title,
                    'location': location,
                    'current_employee': current_employee,
                    'work_experience': work_experience,
                    'review': review,
                    'improvement_idea': improvement_idea,
                    'score': score,
                    'review_date': review_date,
                    'source': 'Dreemjob'
                })
            except:
                reviews.append({
                    'job_title': 'EXCEPTION',
                    'location': 'EXCEPTION',
                    'current_employee': 'EXCEPTION',
                    'work_experience': 'EXCEPTION',
                    'review': 'EXCEPTION',
                    'improvement_idea': 'EXCEPTION',
                    'score': -1,
                    'review_date': 'EXCEPTION',
                    'source': 'Dreemjob'
                })
        return reviews

    def save_file(self, items):
        with open(self.file_name, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['job_title', 'location', 'current_employee', 'work_experience', 'review', 'improvement_idea', 'score', 'review_date', 'source'])
            for item in items:
                writer.writerow([item['job_title'], item['location'], item['current_employee'], item['work_experience'], item['review'], item['improvement_idea'], item['score'], item['review_date'], item['source']])
            print('Data is successfully written.')

    def parse(self):
        html = self.get_html()
        if html.status_code == 200:
            reviews = []
            reviews.extend(self.get_content(html.text))
            time.sleep(3)
            self.save_file(reviews)
            print(f'There are {len(reviews)} reviews.')
        else:
            print('Error!')


class HabrScrapper(WebScrapper):

    def __init__(self, url, file_name):
        super().__init__(url, file_name)

    def get_pages(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        pagination = soup.find('div', class_='pagination-container')
        pages = pagination.find('ul', class_='pagination clearfix first-page-active').find_all('li')
        last_page = str(pages[-2].find('a').get('href'))
        pagination = int(last_page[-1:])
        return pagination

    def get_content(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('div', class_='info users-about-items')
        reviews = []
        for item in items:
            employee_info = item.find('div', class_='meta').get_text(strip=True).split(". ")
            review_date = employee_info[0]
            current_employee = True if 'Текущий сотрудник' in employee_info[1] else False
            work_experience = employee_info[1].replace('Текущий сотрудник', '').replace('Бывший сотрудник', '').replace('Стаж ', '')
            if len(employee_info) == 2:
                location = 'N/A'
                job_title = 'N/A'
            elif len(employee_info) == 4:
                location = employee_info[2]
                job_title = employee_info[3]
            else:
                location = 'N/A'
                job_title = 'N/A'
            rating = item.find('div', class_='average')
            score = rating.find('span', class_='value').get_text(strip=True)
            comments = item.find_all('div', class_='row_info data')
            review = ''
            for comment in comments:
                review += str(comment.find_all('p'))
            print(employee_info, job_title, location, review_date, work_experience, current_employee)
        return reviews

    def save_file(self, items):
        with open(self.file_name, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['job_title', 'location', 'comment', 'score', 'source'])
            for item in items:
                writer.writerow([item['job_title'], item['location'], item['comment'], item['score'], item['source']])
            print('Data is successfully written.')

    def parse(self):
        html = self.get_html()
        if html.status_code == 200:
            reviews = []
            pages_count = self.get_pages(html.text)
            for page in range(0, pages_count + 1):
                print(f'Scraping of the {page + 1}/{pages_count + 1} web-page...')
                html = self.get_html(params={'page': page})
                reviews.extend(self.get_content(html.text))
                time.sleep(3)
            self.save_file(reviews)
            print(f'There are {len(reviews)} reviews.')
        else:
            print('Error!')

class IndeedScrapper(WebScrapper):

    def __init__(self):
        super().__init__('https://ca.indeed.com/cmp/Epam-Systems/reviews?fcountry=ALL', 'indeed_reviews.csv')

    def get_pages(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        pages = soup.find('ul', class_='css-7kt1ng e37uo190').find_all('li')
        pagination = int(pages[-2].find('a').get_text(strip=True))
        return pagination

    def get_content(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('div', class_='css-r0sr81 e37uo190')
        reviews = []
        for item in items:
            job_title = item.find('a', class_='css-1uzwpqi emf9s7v0')
            if job_title:
                job_title = job_title.get_text(strip=True)
            else:
                job_title = 'N/A'
            employee_desc = item.find('span', class_='css-xvmbeo e1wnkr790').get_text(strip=True)
            current_employee = '1' if 'Current Employee' in employee_desc else '0'
            review_date = employee_desc[employee_desc.rfind('-') + 1:]
            title = item.find('span', class_='css-82l4gy eu4oa1w0').get_text(strip=True)
            review_full = item.find_all('div', class_='css-rr5fiy eu4oa1w0')
            review_body = review_full[0].find_all('span', class_='css-82l4gy eu4oa1w0')
            review_list = [review.get_text(strip=True) for review in review_body]
            review = " ".join(review_list)
            if len(review_full) == 1:
                advantage = None
                disadvantage = None
            else:
                review_extra = review_full[1].find_all('span', class_='css-82l4gy eu4oa1w0')
                if len(review_extra) == 2:
                    advantage = review_extra[0].get_text(strip=True)
                    disadvantage = review_extra[1].get_text(strip=True)
                else:
                    advantage = None
                    disadvantage = None
            score = item.find('button', class_='css-1c33izo e1wnkr790').get_text(strip=True)
            reviews.append({
                'job_title': job_title,
                'location': None,
                'current_employee': current_employee,
                'work_experience': None,
                'title': title,
                'review': review,
                'advantage': advantage,
                'disadvantage': disadvantage,
                'score': score,
                'review_date': review_date,
                'source': 'Indeed'
            })
        return reviews


    def save_file(self, items):
        with open(self.file_name, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['job_title', 'location', 'current_employee', 'work_experience', 'title', 'review', 'advantage', 'disadvantage', 'score', 'review_date', 'source'])
            for item in items:
                writer.writerow(
                    [item['job_title'], item['location'], item['current_employee'], item['work_experience'], item['title'], item['review'], item['advantage'], item['disadvantage'], item['score'], item['review_date'], item['source']])
            print('Data is written to the file successfully!')

    def save_to_db(self, items):
        with DBConnection(SERVER, DATABASE, DB_USERNAME, DB_PASSWORD) as db:
            tables_to_clean = ['hr_brand.company_reviews', 'hr_brand.employees']
            for table in tables_to_clean:
                sql_query = f'DELETE FROM {table}'
                db.exec_command(sql_query)
            for item in items:
                sql_query = "INSERT INTO hr_brand.employees (job_title, is_active) VALUES (?, ?)"
                cursor = db.conn.cursor()
                cursor.execute(sql_query, item['job_title'], item['current_employee'])
                db.conn.commit()
                sql_query = 'SELECT max(id) FROM hr_brand.employees'
                id = db.exec_select(sql_query)[0][0]
                sql_query = "INSERT INTO hr_brand.company_reviews (title, review, advantage, disadvantage, score, review_date, source, employee_id) " \
                            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
                cursor.execute(sql_query, item['title'], item['review'], item['advantage'], item['disadvantage'], item['score'], datetime.strptime(item['review_date'], "%d %B %Y"), item['source'], id)
                db.conn.commit()
                cursor.close()
            print('Data is written to the database successfully!')

    def parse(self):
        html = self.get_html()
        if html.status_code == 200:
            reviews = []
            pages_count = 15
            start = 0
            for page in range(0, pages_count):
                print(f'Scrapping of the {page + 1}/{pages_count} web-page...')
                html = self.get_html(params={'start': start})
                reviews.extend(self.get_content(html.text))
                time.sleep(3)
                start += 20
            self.save_file(reviews)
            self.save_to_db(reviews)
            output = f'Web-scrapping of {pages_count} pages was executed successfully! There are {len(reviews)} reviews.'
        else:
            output = 'Error! Web-scrapping failure.'
        return output

if __name__ == '__main__':
    # careerBlissScrapper = CareerBlissScrapper(URL1, FILE1)
    # careerBlissScrapper.parse()
    # dreemjobScrapper = DreemjobScrapper(URL2, FILE2)
    # dreemjobScrapper.parse()
    # habrScrapper = HabrScrapper(URL3, FILE3)
    # habrScrapper.get_content(habrScrapper.get_html().text)
    indeedScrapper = IndeedScrapper()
    indeedScrapper.parse()