import re
import sys
import requests

import bs4
from termcolor import colored

# подменяем хедер пайтона на мозилу
BROWSER_HEADERS = headers = requests.utils.default_headers()
BROWSER_HEADERS.update({
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0'
})


input_url = str(input(colored("Enter url, exemple,  http://www.site.com\n",'green')))

print(colored(input_url, 'yellow'))


def enter_deep_parses_page() -> int:
    try:
        return int(input("Enter deep level parsing pages: 0 or 1 or 2 or 3 or more\n"))
    except ValueError:
        print(colored("Please enter number", 'red'))
        return enter_deep_parses_page()


result_emails = []  # имейлы отсортированные
chache_emails = []  # буфер имейлов
level_scan_links = {}  # уровневое хранилище ссылок

url_base = ["http", "https", "www."]  # начало урла
ignore_img = [".jpg", ".jpeg", ".bmp", ".svg", ".png", ".JPG", ".JPEG", ".BMP", ".SVG",".PNG"]# игнор ссылок с картинками
chache_urls_base = []  # буфер ссылок



def get_html_text(url: str) -> str:
    html = requests.get(url, headers=BROWSER_HEADERS).text
    return html


def get_href(url: str) -> list:
    soup = bs4.BeautifulSoup(get_html_text(url), "html.parser")
    links = soup.find_all("a", href=True)
    return links


def save_emails(url: str) -> None:
    try:
        emails = set(re.findall(r'[\w\.-]+@[\w\.-]+', get_html_text(url)))
        for email in emails:
            if len(email.split('@')[0]) >= 3 and len(email.split('@')[1]) >= 3 and (email.find(".")) >= 1:
                chache_emails.append(email)
            else:
                pass
    except:
        pass


def parsing_email_for_level_scan_link():
    print(colored("Start parsing @mail ", 'yellow'))
    for link in chache_urls_base:
        print(colored(link, 'green'))
        save_emails(link)
    print(colored("End parsing @mail ", 'yellow'))


def create_deep_scan_level():
    try:
        deep_level = enter_deep_parses_page()
        if deep_level == 0:
            # сохр. имейлы с нулевой страницы
            save_emails(input_url)
            result_emails = set(chache_emails)

        else:
            # сохр. ссылки с нулевой странице
            level_scan_links['link_level0'] = []
            for link in get_href(input_url):
                # проверяем ссылку на допустимые параметры
                if (link.get('href')[0:4] in url_base) == True or (link.get('href')[0:5] in url_base) == True \
                        and (link.get('href') in chache_urls_base) == False:
                    # проверяем ссылку на отсутствие картинок
                    if (link.get('href')[-4:] in ignore_img) == False and (link.get('href')[-5:] in ignore_img) == False \
                            and (link.get('href') in chache_urls_base) == False:
                        print(colored('Start create links level 0 :' + link.get('href'), 'blue'))
                        # записываем в буфер ссылку
                        chache_urls_base.append(link.get('href'))
                        #     записываем ссылку в уровневое хранилище
                        level_scan_links['link_level0'].append(link.get('href'))
                    else:
                        pass
                else:
                    pass

            # для ссылок из нулевой страницы
            for deep in range(1, deep_level + 1):
                #  создаем новый уровень ссылок
                level_scan_links['link_level' + str(deep)] = []
                for links in level_scan_links['link_level' + str(deep - 1)]:
                    # print(colored(links,'red'))
                    # достаем ссылку
                    for link in get_href(links):
                        # проверяем ссылку на допустимые параметры начала урла
                        if (link.get('href')[0:4] in url_base) == True or (link.get('href')[0:5] in url_base) == True \
                                and (link.get('href') in chache_urls_base) == False \
                                and (link.get('href')[-4:] in ignore_img) == False:
                            # проверяем ссылку на отсутствие картинок
                            if (link.get('href')[-4:] in ignore_img) == False and (
                                        link.get('href')[-5:] in ignore_img) == False \
                                    and (link.get('href') in chache_urls_base) == False:
                                print(colored('link_level ' + str(deep) + ' :' + link.get('href'), 'blue'))
                                # записываем в буфер ссылку
                                chache_urls_base.append(link.get('href'))
                                #     записываем ссылку в уровневое хранилище
                                level_scan_links['link_level' + str(deep)].append(link.get('href'))
                            else:
                                pass
                        else:
                            pass

    except:
        print(colored("Please enter number", 'red'))
        sys.exit()
        return create_deep_scan_level()


create_deep_scan_level()
parsing_email_for_level_scan_link()
result_emails = set(chache_emails)

print(colored('RESULT PARSING EMAILS', 'green'))
print("Find Emails: ", len(result_emails))
for email in result_emails:
    print(email)
print(colored("PARSING END", 'green'))
